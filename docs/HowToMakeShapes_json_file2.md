# `CdModule.CollisionDetection`の`addLinkShape`が使うshapeList(`shapes.json`)をどのように作成するか.簡易版

1. ベンダーが提供している形状データを探す  
   `shapes.json`の座標系定義はURDFと同じなのでURDFに同梱されているSTL meshが良い
2. 形状データを人間が見て大まかな当たりをつける  
   STLには寸法絶対値が無いので、必要なら1が1メートル(SI)になるようにmeshlabのscaleなどで調整する(ROS用のmeshの場合は不要)
3. bounding boxを計算する(nova2やjakaはおおよそXYZ軸に沿っているので)  
   ```
   ../scripts/boundingBoxAll.sh
   ```
   個々のSTLファイルのbboxを作る場合は`boundingBoxAll.sh STLファイル名`
4. 必要に応じて.bboxファイルを編集する  
   `Mesh Bounding Box Size`行のうしろの値を編集して
   `Mesh Bounding Box crop`行を付ける。`crop`行の値は
	-1の場合はminの値固定、1の場合はmaxの値固定、0の場合は中点固定で
	`Size`に従ってmin/max変更される(上記の範囲外も可で自由に場所を移動可能)。
	さらに`Mesh Bounding Box scale`行で面取り可能。1で正方形が正八角形まで
	面取りされる。
5. bboxからSTLファイルとPLYファイルとgltfとbinを作成する  
   ```
   ../scripts/createBboxAll.sh
   ```
   個々のbboxを処理する場合は`createBbox.sh bboxファイル`  
   STL(bbox)には色が無いので、好みに応じて `../nodejs/scripts/set-gltf-color.mjs`
   で色とopacityを設定する
6. このcolliderで妥協できるか、人が見て検討する
   ```
   meshlab Link4.STL Link4.bbox.stl
   ```
   あるいは
   ```
   for n in 1 2 3 4 5 6; do CloudCompare Link$n.stl Link$n.bbox.stl; done
   ```
   のような感じ。**人が行う**。STLは色が無いが大体わかる。
   好みで`CloudCompare`も可。`meshlab`はプラグイン不要で原点と座標系が分かる。
7. 変更したければ(大抵ある) 4.に戻って編集して 5.を行う。6.の`meshlab`を見ながら
   `.bbox`を編集すると楽
8. 良ければ `ply_loader.py`が読み取って`shapes.json`を作るための
   インデックスである`shapelist.json`を作る。stubは以下のコマンドで出来る。
   ```
   ../scripts/create_shapelist.sh *.bbox.ply
   ```
9. `shapelist.json`(の中身の配列の順番)を編集する。さらにテーブル(baseと同一の
   配列に入れる)や、endEffector(後述のジョイント数+2)も追加する。
   最終出力物の`shapes.json`はプレーンオブジェクトでなく配列なので**順番が重要**。
   ジョイントの数+2の配列。ベースリンクからツールまで(endLinkとhandは位置関係固定
   だが追加の要素としてendLinkと別にする)順番に並べる。
   1個のリンクに複数のconvex colliderを着けたい場合は、配列にplyファイルを並べる
10. `shapes.json`作成  
	```
	../scripts/ply_loader.js shapelist.json
	```
	`output.json`ファイルができる。これをサーバーのロボット型名のディレクトリに
	名前を`shapes.json`と変えてコピーする。URDFをロードする時に`shapes.json`が
	存在すると collision	detectionが働く。
11. 確認  
	```
	../scripts/json-dimensions.py output.json
	```
	配列の階層を示す(普通にエディタで見ても良い)。
	`../scripts/json-dimensions.py output.json -d 2`と
	`../scripts/json-dimensions.py urdf.json -d 1`と見比べて、`output.json`
	の方が1個(ツールの分)だけrootの要素数が多くてdimension構造が想定とおりならば
	OK
12. 表示  
	上記の5.でgltfが出来ているので、サーバーのディレクトリの`update.json`の、
	link定義のvisualプロバティーの配列に追加する。  
	collider(`shapes.json`)に関してはvisualの要素のoriginプロパティーは考慮されない(そもそも`cd-worker`はURDFのlink情報は読まない)。URDFと矛盾無い
	ことが必須なため。colliderが、originなしで適切な位置に見えないと、正しく
	collision detectionできないので、colliderのbounding box(4)まで戻って
	作り直す必要がある
12. 表示 実行時  
	`robot-loader`を使ってロボットアームのA-Frame entityを作成していれば
	visualの要素毎にlinkとは別にa-entityが作成されている。
    `update.json`でcolliderのgltfも付与してあれば、そのa-entityのmaterialを
	変えることでcolliderを表示したり消したりできる。
