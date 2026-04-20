# 細かいSTL, step等のデータをdecimateしてcovex decompositionする

ベンダー提供データのboundingBoxでは粗すぎる場合の対応  
Unitree G1のtorsoとarmのexample

1. DECIMATION:  
   ベンダー提供の(表示に使用している)STLをざっくりと頂点数を減らす  
   `blender_decimate.py`: voxel化してremeshすることで細かい凹凸を消し(step02)、
   decimateで頂点数を削減する(step03)
   ```
   blender --background --python "$ScriptDir"/bender_decimate.py -- --input exampleLink.STL --output exampleLink.out/
   ```
   blenderでスクリプトを実行すると`exampleLink.out`ディレクトリに、`step03_decimated.stl`ま
   でできる。
   必要に応じて
   ```
   BLENDER_VOXEL_SIZE=0.005
   BLENDER_DECIMATE_RATIO=0.1
   BLENDER_SMALL_VOL_THRESHOLD=1e-5
   ```
   これらを変更する。`VOXEL_SIZE`はSTLの単位でrosデータの場合はメートル。`DECIMATE_RATIO`は
   小さいほど粗くなる  
   torsoのような不要な凹が存在するだけの形状の場合は、step03のconvex hullを作成して使用できる
   可能性がある(vertexが数10個ならば)。
2. CONVEX DECOMPOSITION:  
   形状に無視できないあるいは凸包にすると不要に大きくなる凸形状が有る場合は凸分解する  
   ```
   cd exampleLink.out/
   ../../../s/coacd_decomp.sh
   ```
   上記コマンドで、stlからCoACD main入力用objに変換し、凸分解して、
   パーツ分け色分けされたWRLをばらばらのplyファイルにする  
   current directory下の`output_parts/`に分解されたstlができる。小さいサイズのものは
   大抵無視すれば良い。meshlabserverでASCII plyに変換すれば頂点と面の数はすぐわかるので
   確認しても良い。
   ```
   meshlabserver -i output_parts/convex_004.stl -o output_parts/convex_004.ply -m sa
   ```
   realtime collider用にvertexの数が十分少なく構成しているconvex hullが
   小さすぎなければ、そのままplyに変換して`"$ScriptDir"/ply_loader.js`の入力に使用しても
   良いが、パーツごとに`HowToMakeShapes_json_file2.md`を行えば32点に減らすことができる
3. PARTS SELECTION:  
   凸分解の結果を一つの凸包にして良い部分は、再度まとめて一つの凸包にする。
   ここは**自動化できない**ため人が目で見ながら設定する。
   ```
   cd output_parts
   meshlab convex_*.ply
   ```
   GUIで、必要なパーツを選択して`Save Project As...`で名前を付けて保存する。
   例えば`set1`と
   すると`set1.mlp`ができる。
   ```
   ../../../../s/meshlab2convex.sh set1.mlp
   ```
   これで、まとめた凸包の`set1.ply`ができる。これを`shapelist.json`に書く
4. INFLATION:  
   colliderは元の形状より大きい(元を中に含む)必要があるため必要に応じて凸包を膨らませる
   ```
   ../../..../s/inflate_ply.py set1.ply set1inflated.ply 1.02
   ```
   手先のように多少接触しても構わないパーツはこの作業は不要。
5. JSON GENERATION:  
   `shapelist.json`で使用するPLYファイルを定義して`ply_loader.py`で
   `shapes.json`を作成する。`HowToMakeShapes_json_file2.md`参照
	以下の例では各ファイルの名前は適当にかえる
   ```
   cd ../../ # meshesディレクトリ
   ln -s exampleLink.out/output_parts/set1.ply exampleLink-set1.bbox.ply
   ln -s exampleLink.out/output_parts/set2.ply exampleLink-set2.bbox.ply
   ln -s example2Link.out/output_parts/set1.ply example2Link-set1.bbox.ply
   ```
   ロボット全体のリンクのbbox.plyを集めたら
   ```
   ../../s/create_shapelist.sh *.bbox.ply > shapeList.json
   vi shapeList.json
   ../../s/ply_loader.js shapeList.json ../linkmap.json
   ```
6. OPTIONAL glTF GENERATION:  
   ```
   ../../a/convert-to-gltf.sh *bbox.ply
   ```
7. ASSETS COPY:  
   ```
   ../../copy-assets.sh . ../g1-right-pkg/public/g1-right-thumb/
   ```
