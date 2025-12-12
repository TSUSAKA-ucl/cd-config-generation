import bpy, bmesh, sys, os
import mathutils

quantize = 1e-5
merge_dist = quantize

argv = sys.argv
argv = argv[argv.index("--") + 1:] if "--" in argv else []

# argv example:
# blender --background --python convex_all.py -- input1.ply input2.ply input3.ply output.stl
input_files = argv[:-1]
output_path  = argv[-1]

print("Input files:", input_files)
print("Output     :", output_path)

# シーン初期化
bpy.ops.wm.read_factory_settings(use_empty=True)

# すべての頂点を格納
all_verts = []

for filepath in input_files:
    print(f"Importing: {filepath}")
    bpy.ops.import_mesh.ply(filepath=filepath)
    obj = bpy.context.selected_objects[0]
    for v in obj.data.vertices:
        all_verts.append(v.co.copy())
    # シーンを軽くするため削除
    bpy.data.objects.remove(obj, do_unlink=True)

print(f"Total vertices loaded: {len(all_verts)}")

# 新しいメッシュ作成
mesh = bpy.data.meshes.new("ConvexHullMesh")
obj = bpy.data.objects.new("ConvexHullObj", mesh)
bpy.context.collection.objects.link(obj)

# bmesh で統合凸包作成
bm = bmesh.new()

for v in all_verts:
    vq = mathutils.Vector((
        round(v.x / quantize) * quantize,
        round(v.y / quantize) * quantize,
        round(v.z / quantize) * quantize
    ))
    bm.verts.new(vq)

bm.verts.ensure_lookup_table()

# 近接点統合（量子化後のダブり削除）
bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=merge_dist)

# 凸包生成
bmesh.ops.convex_hull(bm, input=bm.verts)
bm.to_mesh(mesh)
bm.free()

# 出力
bpy.ops.object.select_all(action='DESELECT')
obj.select_set(True)
bpy.context.view_layer.objects.active = obj
bpy.ops.export_mesh.stl(filepath=output_path, use_selection=True)

print("Convex hull export complete:", output_path)
