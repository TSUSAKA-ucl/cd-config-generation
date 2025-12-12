# 細かいSTL, step等のデータをdecimateしてcovex decompositionする

ベンダー提供データのboundingBoxでは粗すぎる場合の対応  
Unitree G1のtorsoとarmのexample

1. ベンダー提供の(表示に使用している)STLをざっくりと頂点数を減らす  
   `blender_decimate.py`: voxel化してremeshすることで細かい凹凸を消し(step02)、
   decimateで頂点数を削減する(step03)
   ```
   blender --background --python "$ScriptDir"/bender_decimate.py -- --input exampleLink.STL --output exampleLink.out/
   ```
   blenderでスクリプトを実行すると`exampleLink.out`ディレクトリに、`step03_decimated.stl`ま
   でできる。
   必要に応じて`VOXEL_SIZE = 0.005`, `DECIMATE_RATIO = 0.1`, `SMALL_VOL_THRESHOLD = 1e-5`
   これらを変更する。`VOXEL_SIZE`はSTLの単位でrosデータの場合はメートル。`DECIMATE_RATIO`は
   小さいほど粗くなる  
   torsoのような不要な凹が存在するだけの形状の場合は、step03のconvex hullを作成して使用できる
   可能性がある(vertexが数10個ならば)。
2. 形状に無視できないあるいは凸包にすると不要に大きくなる凸形状が有る場合は凸分解する  
   CoACDのサンプルの`main`を用いる。`main`の入力はobjを要求するためstlから変換して入力する
   ```
   meshlabserver -i step03_decimated.stl -o step03_decimated.obj
   CoACD/.../main -i step03_decimated.obj -o step03_decimated.wrl
   ```
   出力はwrlにパーツ分け色分けされて出力されるため、それを別々のstlに分解する
   ```
   blender -b --python "$ScriptDir"/split_CoACD_wrl.py
   ```
   current directory下の`output_parts/`に分解されたstlができる。小さいサイズのものは
   大抵無視すれば良い。meshlabserverでASCII plyに変換すれば頂点と面の数はすぐわかるので
   確認しても良い。
   ```
   meshlabserver -i output_parts/convex_004.stl -o output_parts/convex_004.ply -m sa
   ```
   realtime collider用にvertexの数が十分少なく構成しているconvex hullが
   小さすぎなければ、そのままplyに変換して`"$ScriptDir"/ply_loader.js`の入力に使用しても
   良いが、パーツごとに`HowToMakeShapes_json_file2.md`を行えば32点に減らすことができる
3. 凸分解不要で一つの凸包にして良い部分は、再度まとめて一つの凸包にする
   ```
   blender -b -P "$ThisDir"/blender_convex_hull_multi.py -- convex_004.ply convex_009.ply convex_010.ply convex_013.ply  convex_004-9all.stl
   ```
4. colliderは元の形状より大きい(元を中に含む)必要があるため凸包を膨らませる
	   
