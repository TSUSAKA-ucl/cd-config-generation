#!/usr/bin/env node
// shapelist.jsonに従ってPLYファイルを読み込み、各頂点の座標を抽出し
// 配列にして1個のJSON形式で保存するスクリプト。ブラウザのworkerに送信するためのもの。
import path from 'path';
import fs from 'fs';
import { load } from '@loaders.gl/core';
import { PLYLoader } from '@loaders.gl/ply';
import { Euler, Vector3, Matrix4 } from "three";

async function loadPLY(fileName) {
  const buffer = fs.readFileSync(fileName); // バッファを読み込み
  const data = await load(buffer, PLYLoader);
  // console.log(data);

  const positions = data.attributes.POSITION.value;
  const points = [];

  for (let i = 0; i < positions.length; i += 3) {
    points.push([positions[i], positions[i + 1], positions[i + 2]]);
  }
  return points;
}

function loadJson(path, defVal) {
  try {
    return JSON.parse(fs.readFileSync(path, "utf8"));
  } catch (e) {
    if (e.code === "ENOENT") {
      return defVal;
    }
    throw e;          // それ以外のエラーは再スロー
  }
}

// 形状のリストの定義ファイルのパス
if (process.argv.length < 3) {
  console.error(`使用法: node ${path.basename(__filename)} <shapelist> <linkmap>`);
  process.exit(1);
}
// /console.log(process.argv)
const inputPath = process.argv[2] || './shapelist.json';
const linkPath = process.argv[3] || './linkmap.json';
const dirname = path.dirname(inputPath);
const list = loadJson(inputPath, [[]]);
const link = loadJson(linkPath, {});
const shapeOrigins  = {};
let output = [];
for (const convex of list) {
  const convexList = [];
  for (const shape of convex) {
    const points = await loadPLY(path.join(dirname, shape));
    const tf = new Matrix4();
    const shapeName = shape.replace(/\.[^/.]+$/, '').replace(/\.bbox[0-9]*/,'');
    const transformPoints = (visual) => {
      if (visual?.geometry) {
	const urdfName = visual.geometry?.mesh?.$?.filename;
	const baseName = urdfName.replace(/^([^/]*\/)*/,'').replace(/\.[^/.]+$/, '');
	if (baseName === shapeName) {
	  shapeOrigins[shape] = visual?.origin?.$;
	  // console.log(`Found link for shape ${shape}:`, shapeOrigins[shape]);
	  const rpy = shapeOrigins[shape]?.rpy || [0,0,0];
	  const xyz = shapeOrigins[shape]?.xyz || [0,0,0];
	  const euler = new Euler(rpy[0], rpy[1], rpy[2], 'XYZ');
	  tf.makeRotationFromEuler(euler);
	  tf.setPosition(xyz[0], xyz[1], xyz[2]);
	  points.forEach((point) => {
	    const v = new Vector3(point[0], point[1], point[2]);
	    v.applyMatrix4(tf);
	    point[0] = v.x;
	    point[1] = v.y;
	    point[2] = v.z;
	  });
	}
      }
    };	
    Object.entries(link).forEach(([key, value]) => {
      if (Array.isArray(value.visual)) {
	value.visual.forEach((visual) => transformPoints(visual));
      } else {
	transformPoints(value.visual);
      }
    });
    convexList.push(points);
  }
  output.push(convexList);
}
const outputFile = 'output.json';
fs.writeFileSync(outputFile, JSON.stringify(output, null, 2), 'utf8');
console.log(`PLYファイルのデータを ${outputFile} に書き込みました。`);
console.log('形状の座標変換情報:', shapeOrigins);
