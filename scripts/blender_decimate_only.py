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
elif ext == ".ply":
    bpy.ops.import_scene.ply(filepath=INPUT_PATH)
else:
    raise ValueError("Unsupported format")

obj = bpy.context.selected_objects[0]
obj.name = "source"

# ------------------------------------------------------
# 4. Decimate
# ------------------------------------------------------
dec = obj.modifiers.new("decimate", "DECIMATE")
dec.ratio = DECIMATE_RATIO
bpy.ops.object.modifier_apply(modifier="decimate")

bpy.ops.export_mesh.stl(filepath=f"{OUT_DIR}/step0x_decimated.stl")
print("Saved: step03_decimated.stl")

print("All steps completed.")
