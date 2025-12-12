import bpy
import os
import sys

# --- 引数の処理 ---
argv = sys.argv
argv = argv[argv.index("--") + 1:] if "--" in argv else []
if len(argv) < 2:
    print("Usage: blender --background --python split_by_material.py -- input.wrl output_dir")
    sys.exit(1)

input_path = os.path.abspath(argv[0])
output_dir = os.path.abspath(argv[1])
os.makedirs(output_dir, exist_ok=True)

# --- X3D/VRML importer を有効化 ---
bpy.ops.preferences.addon_enable(module="io_scene_x3d")

# --- シーン初期化 ---
bpy.ops.wm.read_factory_settings(use_empty=True)

# --- VRMLファイルを読み込み ---
bpy.ops.import_scene.x3d(filepath=input_path)

# --- オブジェクト単位で処理 ---
for obj in bpy.context.scene.objects:
    if obj.type != 'MESH':
        continue

    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.separate(type='MATERIAL')
    bpy.ops.object.mode_set(mode='OBJECT')

# --- 分割された各メッシュを個別にエクスポート ---
for obj in bpy.context.scene.objects:
    if obj.type != 'MESH':
        continue
    mat_name = obj.active_material.name if obj.active_material else obj.name
    safe_name = "".join(c if c.isalnum() else "_" for c in mat_name)
    out_path = os.path.join(output_dir, f"{safe_name}.stl")
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.ops.export_mesh.stl(filepath=out_path, use_selection=True)
    print(f"Exported {out_path}")

print("Done.")
