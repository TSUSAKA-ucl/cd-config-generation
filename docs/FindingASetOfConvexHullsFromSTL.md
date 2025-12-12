# リンクの順番 (the order of Unitree G1 arm's links)
0. `torso_link.STL`
1. `right_shoulder_pitch_link.STL`
2. `right_shoulder_roll_link.STL`
3. `right_shoulder_yaw_link.STL`
4. `right_elbow_link.STL`
5. `right_wrist_roll_link.STL`
6. `right_wrist_pitch_link.STL`
7. `right_wrist_yaw_link.STL`

# 処理の手順(steps for convex decomposition)
## 処理の順番(the orde of general convex decomposition process)
1. decimate
   ```
   blender -b -P blender_decimate.py -- --input right_elbow_link.STL --output right_elbow_link
   ```
2. convex decomposition
   ```
   coacd_decomp.sh right_elbow_link
   ```
3. combining multiple convex hulls to reduce vertices
   ```
   cd right_elbow_link/output_parts/
   blender -b -P blender_convex_hull_multi.py  -- convex_001.ply convex_002.ply convex_003.ply convex_005.ply convex_001to5.stl
   ```
4. inflating of the convex hull
   ```
   python3 inflate_ply.py  convex_001to5.ply convex_001to5-exp.ply 1.05
   ```

## 処理のパラメータ
1. `blender_decimate.py`  
   * step1: small parts removal  
     `SMALL_VOL_THRESHOLD = 1e-5` in m^3
   * step2: voxel remesh
     `VOXEL_SIZE = 0.005` in m
   * step3: decimation
     `DECIMATE_RATIO = 0.1` ratio of number of faces, reduced to 1/10

2. `CoACD/main`

## approximating to an octagonal prism (further vertex reduction)
see [`HowToMakeShapes_json_file2.md`](./HowToMakeShapes_json_file2.md)

### processing order
1. create a bounding box file template
   ```
   boundingBox.sh Link1.STL Link2.STL
   ```
2. edit .bbox files. 
   ```
   vi Link1.bbox
   ```
   modify and/or add following three lines
   ```
   Mesh Bounding Box Size 0.120186  0.120186  0.135449
   Mesh Bounding Box crop 0 0 0
   Mesh Bounding Box scale 0.8 0.8 0.2
   ```
3. create a chamfered octagonal prism convex hull
   ```
   createBbox.sh Link1.bbox
   ```
   .bbox.ply, .bbox.stl, .bbox.gltf, .bbox.bin files are generated
4. visually check and correct .bbox files
   ```
   meshlab Link1.STL Link1.bbox.stl
   ```
   goto 2.
