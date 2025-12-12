'use strict';
// const fs = require('fs');
// const path = require('path');
import fs from 'fs';
import path from 'path';

// Emscriptenで生成した初期化関数。これを呼んでCdModuleを生成する。
// const CdModuleFactory = require('../../dist/cd_module.js');
import CdModuleFactory from '../../dist/cd_module.js';

// CdModuleを閉じ込めて、その関連オブジェクトを生成するhelper関数群
function createHelpers(module) {
  function makeConvexShape(xyzArray) {
    // console.log("module", module);
    const vec = new module.ConvexShape();
    for (let i = 0; i < xyzArray.length; ++i) {
      const xyz = xyzArray[i];
      vec.push_back({x: xyz[0], y: xyz[1], z: xyz[2]});
    }
    return vec;
  }
  function makeDoubleVector(jsArray) {
    const vec = new module.DoubleVector();
    for (let i = 0; i < jsArray.length; ++i) {
      vec.push_back(jsArray[i]);
    }
    return vec;
  }
  function makeJointModelVector(jsArray) {
    const vec = new module.JointModelFlatStructVector();
    for (let i = 0; i < jsArray.length; ++i) {
      vec.push_back(jsArray[i]);
    }
    return vec;
  }
  // 他のヘルパー関数もここに追加できる
  // }

  // 他にも必要な関数を追加できる
  return {
    makeDoubleVector,
    makeJointModelVector,
    makeConvexShape,
    // ... more helpers
  };
}

// ************************
// メイン関数
function main() {
  // ファイルパスを指定
  if (process.argv.length < 3) {
    console.error('使用法: node read_json.js <ジョイント定義> <形状定義>');
    process.exit(1);
  }
  // リンク構造定義の入力のファイルパス
  const inputPath = process.argv[2] || './links.json';
  const linkShapePath = process.argv[3] || './link_shapes.json';
  // 入力ファイルが存在するか確認
  if (!fs.existsSync(inputPath)) {
    console.error(`入力ファイルが存在しません: ${inputPath}`);
    process.exit(1);
  }
  if (!fs.existsSync(linkShapePath)) {
    console.error(`リンク形状定義ファイルが存在しません: ${linkShapePath}`);
    process.exit(1);
  }
  // WASMのモジュールを生成する。モジュール初期化が完了してからアクセスするためthenを使う。
  CdModuleFactory().then((CdModule) => { 
    const { makeDoubleVector,
	    makeJointModelVector, 
	    makeConvexShape } = createHelpers(CdModule);
    let cd = null;
    // リンク定義のJSONファイル(extract-joint-tag.jsでURDF XMLから生成)読み込み 
    fs.readFile(inputPath, 'utf8', (errJnt, jointModel) => {
      if (errJnt) {
	console.error('ファイル読み込みエラー:', errJnt);
	return;
      }
      try {
	const allObjects = JSON.parse(jointModel);
	// console.log('読み込んだリンク定義:', allObjects);
	// "type" が "revolute" の要素だけ抽出
	const revolutes = allObjects.filter(obj => obj.$.type === 'revolute');
	// 各行をJointModuleFlatStructに
	const linkModel = revolutes.map(obj => {
	  // const name = obj.$.name ?? '';
	  const xyz_in = obj.origin.$.xyz ?? [NaN, NaN, NaN];
	  const xyz = makeDoubleVector(Array.isArray(xyz_in) && xyz_in.length === 3
				       ? xyz_in : [NaN, NaN, NaN]);
	  const rpy_in = obj.origin.$.rpy ?? [NaN, NaN, NaN];
	  const rpy = makeDoubleVector(Array.isArray(rpy_in) && rpy_in.length === 3
				       ? rpy_in : [NaN, NaN, NaN]);
	  const axis_in = obj.axis.$.xyz ?? [NaN, NaN, NaN];
	  const axis = makeDoubleVector(Array.isArray(axis_in) && axis_in.length === 3
					? axis_in : [NaN, NaN, NaN]);
	  // 各値をオブジェクトに変換
	  const j = new CdModule.JointModelFlatStruct(axis, xyz, rpy);
	  axis.delete();
	  xyz.delete();
	  rpy.delete();
	  return j;
	});
	console.log('抽出されたリンクパラメータ:', linkModel);
	const jointModelVector = makeJointModelVector(linkModel);
	console.log('JointModelFlatStructVector:', jointModelVector);
	// CmdVelGenerator のインスタンスを生成
	const basePosition = makeDoubleVector([0.0, 0.0, 0.0]);
	const baseOrientation = makeDoubleVector([1.0, 0.0, 0.0, 0.0]);
	cd = new CdModule.CollisionDetection(jointModelVector,
					     basePosition,
					     baseOrientation);
	basePosition.delete();
	baseOrientation.delete();
	jointModelVector.delete();

	fs.readFile(linkShapePath, 'utf8', (errShapes, linkShapesData) => {
	  if (errShapes) {
	    console.error('リンク形状定義ファイルの読み込みエラー:', errShapes);
	    return;
	  }
	  try {
	    const linkShapes = JSON.parse(linkShapesData);
	    if (linkShapes.length !== linkModel.length + 2) { // +2はbaseとend_effectorの分
	      console.error('リンク形状定義の数がリンクモデルの数(+2)と一致しません。');
	      return;
	    }
	    console.log('linkShapes.length: ', linkShapes.length);
	    for (let i = 0; i < linkShapes.length; ++i) {
	      console.log(`リンク番号${i} のvector生成`);
	      const shapeWasm = new CdModule.ConvexShapeVector();
	      for (const convex of linkShapes[i]) {
		const convexWasm = makeConvexShape(convex);
		console.log('size of convex js: ', convex.length);
		shapeWasm.push_back(convexWasm);
		convexWasm.delete();
	      }
	      cd.addLinkShape(i, shapeWasm);
	      shapeWasm.delete();
	    }
	    console.log('setting up of link shapes is finished');
	    cd.infoLinkShapes();

	    const testPairs = [[0,2],[0,3],[0,4],[0,5],[0,6],[0,7],
			       [1,3],[1,4],[1,5],[1,6],[1,7],
			       [2,4],[2,5],[2,6],[2,7],
			       [3,5],[3,6],[3,7]
			      ];
	    cd.clearTestPairs();
	    for (const pair of testPairs) {
	      // console.log("add ", pair[0], ", ", pair[1]);
	      cd.addTestPair(pair[0],pair[1]);
	    }
	    const testJointPositions = [[0.0, 1.0, -1.0, 0.0, -1.570, 0.0],
					[0.0, 1.0, -1.25, 0.0, -1.570, 0.0],
					[0.0, 1.0, -1.5, 0.0, -1.570, 0.0],
					[0.0, 1.0, -1.75, 0.0, -1.570, 0.0],
					[0.0, 1.0, -2.0, 0.0, -1.570, 0.0],
					[0.0, 1.0, -2.25, 0.0, -1.570, 0.0],
					[0.0, 1.0, -2.5, 0.0, -1.570, 0.0],
					[0.0, 1.0, -2.75, 0.0, -1.570, 0.0],
					[0.0, 1.0, -3.0, 0.0, -1.570, 0.0],
					[0.0, 1.0, -3.25, 0.0, -1.570, 0.0],
					[0.0, 1.0, -3.5, 0.0, -1.570, 0.0],
					[0.0, 1.0, -3.75, 0.0, -1.570, 0.0]];
	    

	    for (let i = 0; i < testJointPositions.length; ++i) {
	      const jointPositions = makeDoubleVector(testJointPositions[i]);
	      cd.calcFk(jointPositions);
	      jointPositions.delete();
	      let collisionPairs = [];
	      for (let j = 0; j < testPairs.length; ++j) {
		if (cd.testLinksPair(testPairs[j][0], testPairs[j][1])) {
		  collisionPairs.push(testPairs[j]);
		}
	      }
	      if (collisionPairs.length > 0) {
		console.log(`関節位置 ${i} の衝突ペア:`, collisionPairs);
	      }
	      // 
	      const resultPairs = cd.testCollisionPairs();
	      // console.log("type of resultPairs is ", typeof resultPairs)
	      // console.log("resultPairs: ", resultPairs);
	      console.log("resultPairs.size(): ", resultPairs.size());
	      let res = [];
	      for (let j=0; j<resultPairs.size(); ++j) {
		const pair = resultPairs.get(j);
		// console.log("get(", j, "): ", pair)
		// console.log(`[${pair.first}, ${pair.second}]`);
		res.push(pair);
	      }
	      console.log("res: ", res);
	      resultPairs.delete();
	    }
	  } catch (e) {
	    console.error('リンク形状定義のJSONパースエラー:', e);
	  }
	});
      } catch (e) {
	console.error('ジョイントモデルのJSONパースエラー:', e);
      }
    });
  }).catch(err => {
    console.error('WASMモジュールの初期化エラー:', err);
  });
}	   

// ESモジュール版「直接実行」チェック
if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}
