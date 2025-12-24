#!/bin/bash
if [ "$Blender" = "" ]
then Blender=~/Downloads/blender-3.6.23-linux-x64/blender
fi
BlenderPy=`mktemp --suffix=.py` || exit 1
cat >"$BlenderPy" <<EOF
import bpy, bmesh, sys, os
import mathutils

argv = sys.argv
argv = argv[argv.index("--") + 1:] if "--" in argv else []
input_path = argv[0]
output_path = argv[1]

# シーン初期化
bpy.ops.wm.read_factory_settings(use_empty=True)

# PLY読み込み
bpy.ops.import_mesh.ply(filepath=input_path)

# 全頂点を取得
verts = [v.co.copy() for v in bpy.context.active_object.data.vertices]

# 新しいメッシュ作成
mesh = bpy.data.meshes.new("ConvexHullMesh")
obj = bpy.data.objects.new("ConvexHullObj", mesh)
bpy.context.collection.objects.link(obj)

# bmeshで凸包作成
bm = bmesh.new()
for v in verts:
    bm.verts.new(v)
bm.verts.ensure_lookup_table()
bmesh.ops.convex_hull(bm, input=bm.verts)
bm.to_mesh(mesh)
bm.free()

# STL 出力
bpy.ops.object.select_all(action='DESELECT')
obj.select_set(True)
bpy.context.view_layer.objects.active = obj
bpy.ops.export_mesh.stl(filepath=output_path, use_selection=True)
EOF
while [ $# -ge 1 ]
do  OutFile=`echo "$1"|sed -e 's/\.[pP][lL][yY]$/.stl/;t;d'`
    [ "$OutFile" = "" ] && echo Error in "$1". 1>&2 && exit 1
    "$Blender" --background --python "$BlenderPy" --\
	       "$1" "$OutFile" || exit 1
    shift
done
command rm "$BlenderPy"
