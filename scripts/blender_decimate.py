import bpy
import sys
import os
import math
import bmesh

# ------------------------------------------------------
# join を安全に呼び出す関数（これで poll error は起きない）
# ------------------------------------------------------
def safe_join(objs):
    if len(objs) <= 1:
        return objs[0] if objs else None

    # 3D View を検索（ops 実行には必須）
    override = None
    for area in bpy.context.window.screen.areas:
        if area.type == "VIEW_3D":
            for region in area.regions:
                if region.type == "WINDOW":
                    override = {
                        'window': bpy.context.window,
                        'screen': bpy.context.window.screen,
                        'area': area,
                        'region': region,
                        'scene': bpy.context.scene,
                        'view_layer': bpy.context.view_layer,
                        'active_object': objs[0],
                        'selected_objects': objs,
                        'selected_editable_objects': objs,
                    }
                    break
            break

    if override is None:
        raise RuntimeError("No VIEW_3D area available for join().")

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')

    for o in objs:
        o.select_set(True)

    bpy.context.view_layer.objects.active = objs[0]

    bpy.ops.object.join(override)

    return objs[0]

# ------------------------------------------------------
# 引数処理
# ------------------------------------------------------
def parse_args():
    argv = sys.argv
    if "--" not in argv:
        return None
    argv = argv[argv.index("--") + 1:]

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    return parser.parse_args(argv)

args = parse_args()
INPUT_PATH = os.path.abspath(args.input)
OUT_DIR = os.path.abspath(args.output)
if os.environ.get('BLENDER_VOXEL_SIZE'):
    VOXEL_SIZE = float(os.environ['BLENDER_VOXEL_SIZE'])
else:
    VOXEL_SIZE = 0.005
if os.environ.get('BLENDER_DECIMATE_RATIO'):    
    DECIMATE_RATIO = float(os.environ['BLENDER_DECIMATE_RATIO'])
else:
    DECIMATE_RATIO = 0.1
if os.environ.get('BLENDER_SMALL_VOL_THRESHOLD'):    
    SMALL_VOL_THRESHOLD = float(os.environ['BLENDER_SMALL_VOL_THRESHOLD'])
else:
    SMALL_VOL_THRESHOLD = 1e-5

os.makedirs(OUT_DIR, exist_ok=True)

# ------------------------------------------------------
# Blender を初期化
# ------------------------------------------------------
bpy.ops.wm.read_factory_settings(use_empty=True)

# ------------------------------------------------------
# インポート
# ------------------------------------------------------
ext = os.path.splitext(INPUT_PATH)[1].lower()

if ext == ".stl" or ext == ".STL":
    bpy.ops.import_mesh.stl(filepath=INPUT_PATH)
elif ext == ".step" or ext == ".stp":
    bpy.ops.import_scene.step(filepath=INPUT_PATH)
else:
    raise ValueError("Unsupported format")

obj = bpy.context.selected_objects[0]
obj.name = "source"

bpy.ops.export_mesh.stl(filepath=f"{OUT_DIR}/step00_original.stl")
print("Saved: step00_original.stl")

# ------------------------------------------------------
# 2. 小パーツ除去
# ------------------------------------------------------
bpy.ops.object.mode_set(mode='OBJECT')

# Loose Parts 分割
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.separate(type='LOOSE')
bpy.ops.object.mode_set(mode='OBJECT')

parts = list(bpy.context.selected_objects)

# 小パーツ削除
for p in parts:
    dims = p.dimensions
    vol = dims.x * dims.y * dims.z
    if vol < SMALL_VOL_THRESHOLD:
        bpy.data.objects.remove(p, do_unlink=True)

# 再 join（← ここを safe_join に変更）
objs = [o for o in bpy.data.objects if o.type == 'MESH']
obj = safe_join(objs)
obj.name = "cleaned"

bpy.ops.export_mesh.stl(filepath=f"{OUT_DIR}/step01_small_parts_removed.stl")
print("Saved: step01_small_parts_removed.stl")

# ------------------------------------------------------
# 3. Voxel Remesh
# ------------------------------------------------------
mod = obj.modifiers.new("remesh", "REMESH")
mod.mode = 'VOXEL'
mod.voxel_size = VOXEL_SIZE

bpy.ops.object.modifier_apply(modifier="remesh")

bpy.ops.export_mesh.stl(filepath=f"{OUT_DIR}/step02_voxel_remesh.stl")
print("Saved: step02_voxel_remesh.stl")

# ------------------------------------------------------
# 4. Decimate
# ------------------------------------------------------
dec = obj.modifiers.new("decimate", "DECIMATE")
dec.ratio = DECIMATE_RATIO
bpy.ops.object.modifier_apply(modifier="decimate")

bpy.ops.export_mesh.stl(filepath=f"{OUT_DIR}/step03_decimated.stl")
print("Saved: step03_decimated.stl")

print("All steps completed.")
