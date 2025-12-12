# `CdModule.CollisionDetection`の`addLinkShape`が使うshapeList(`shapes.json`)をどのように作成するか

## ここで使用するコマンド等
bash等の他にNode.jsとpythonを使用する
```
sudo apt install meshlab
sudo apt install assimp-utils
pip3 install assimp_py
pip3 install numpy-stl
```
他、ここでは使用しないがBlenderなど。

各種スクリプトは[nodejs](../nodejs/scripts/),
[python](../scripts/), [他](../Data/)にある

## Mathematica等で計算してconvex hullのCSVから作成する方法
0. ベンダー提供のSTLファイルからmeshlabでboundingboxを計算する
1. convex hullのvertexのlistのcsvファイルを手動で作成する
2. csvファイルをplyに変換する  
   ```
   ./csv2ply.sh *.csv
   ```
3. `shapelist.json`を作成する
4. PLYファイルと`shapeList.json`から`shapes.json`を作成する
   ```
   node ../nodejs/scripts/ply_loader.js
   mv output.json shapes.json
   ```

## STLからconvex hullを計算して作成する
0. STLを適当に凸分解する。CoACDなど。
0. CoACDの色付き.wrlをblender(ver.4は読めないので3.6 `split_by_material.py`)で別々のファイル(STL)にする
0. 頂点の数が多いので外接する頂点の少ない凸包に変換する(ソフトが世の中に無いので作る)
1. STLからconvex hullを計算する
   ```
   ./ply2stl.sh meshlabserver -s convexHull.mlx -i XXX/DOBOT_6Axis_ROS2_V3/dobot_rviz/meshes/nova2/Link2.STL -o nova2_link2_convex.stl

   ```
2. vertex情報のみ含むASCII形式のplyファイルを作る
   ```
   ln -s nova2_link2_convex.stl input.stl
   extract-vertices-only.py
   mv vertices.ply nova2_link2_convex.ply
   ```
3. `shapelist.json`作成以下同じ

## `CdModule`用に作成した点群のみplyから`robot_state_publisher`用のSTLファイルを作成する
	
```
./ply2stl.sh Link_2.ply
```
注意: 面情報が無いため凸包にする。`CdModule`用の点群はそのように扱われる(個々の塊の内部の点は事実上無視される)。ここではmeshlabで凸包にしている

## `CdModule`用に作成した凸包plyをA-Frameで表示可能にするためのglTFに変換する
1. plyをSTLに変換する(上記)
2. STLからglTFを作成する
   ```
   assimp export Link_1.STL Link_1.gltf
   ```
   デフォルトでgltf(json)とbinができる
3. gltfに色を付ける
   ```
   change-gltf-color.js Link_1.gltf '1,0.84,0,0.5'
   ```
   第2引数はRGBAカンマ区切り0から1

# `CdModule`(衝突検知)および`SlrmModule`(逆運動学,特異点対応)ようの`urdf.json`作成

(HTTP)のサーバーサイドの実行モジュール無しで、さらにフロントエンドの処理も容易にするため
ロボットの定義は、事前にjsonファイルを作成してサーバー上に置くことにしている。

## ロボットベンダー各社が提供しているROS2用のxacroから`urdf.json`を作成する手順

0. ros2をインストールし、さらに必要なロボットのxacroを含むパッケージをインストールする
1. URDF作成  
   ```
   source /opt/ros/jazzy/setup.bash
   cd `ros2 pkg prefix jaka_zu5_moveit_config`/share/jaka_zu5_moveit_config/config
   xacro jaka_zu5.urdf.xacro > /tmp/jaka_zu5.urdf
   ```
2. URDFからjson生成
   ```
   cd public/jaka_zu5
   ./extract-joint-tag.js /tmp/jaka_zu5.urdf
   ```
   これで、`urdf.json`と`
