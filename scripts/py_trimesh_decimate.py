import bpy
import os
import math
import bmesh

# ------------------------------------------------------
# 設定
# ------------------------------------------------------
INPUT_PATH = "/path/to/input.stl"   # 入力 STL または STEP
OUT_DIR    = "/path/to/output_dir"  # ステップごとの出力先
VOXEL_SIZE = 1.5                    # voxel remesh 解像度(mm)
DECIMATE_RATIO = 0.3                # 面を 30% に削減
SMALL_VOL_THRESHOLD = 1e-5          # 小パーツ除去の閾値
# ------------------------------------------------------

os.makedirs(OUT_DIR, exist_ok=True)

# クリア
bpy.ops.wm.read_factory_settings(use_empty=True)

# ------------------------------------------------------
# 1. インポート
# ------------------------------------------------------
ext = os.path.splitext(INPUT_PATH)[1].lower()

if ext == ".stl":
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
# 2. 小パーツ削除（Connected Components）
# ------------------------------------------------------
bpy.ops.object.mode_set(mode='EDIT')
bm = bmesh.from_edit_mesh(obj.data)
bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.is_valid], context='VERTS')  # ダミー
bpy.ops.object.mode_set(mode='OBJECT')

# Blender では厳密な体積判定を行う場合は modifier 経由の方が確実
bpy.ops.object.modifier_add(type='WELD')
bpy.ops.object.modifier_apply(modifier="Weld")

# “Loose Parts” に分割
bpy.ops.mesh.separate(type='LOOSE')
parts = bpy.context.selected_objects

# フィルタリング
for p in parts:
    bpy.context.view_layer.objects.active = p
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    if p.dimensions.x * p.dimensions.y * p.dimensions.z < SMALL_VOL_THRESHOLD:
        bpy.data.objects.remove(p, do_unlink=True)

# merge back
bpy.ops.object.select_all(action='DESELECT')
for p in bpy.data.objects:
    p.select_set(True)
bpy.ops.object.join()

obj = bpy.context.active_object
obj.name = "cleaned"

bpy.ops.export_mesh.stl(filepath=f"{OUT_DIR}/step01_small_parts_removed.stl")
print("Saved: step01_small_parts_removed.stl")

# ------------------------------------------------------
# 3. Voxel Remesh（内部構造除去）
# ------------------------------------------------------
mod = obj.modifiers.new("remesh", "REMESH")
mod.mode = 'VOXEL'
mod.voxel_size = VOXEL_SIZE
mod.adaptivity = 0.0

bpy.ops.object.modifier_apply(modifier="remesh")

bpy.ops.export_mesh.stl(filepath=f"{OUT_DIR}/step02_voxel_remesh.stl")
print("Saved: step02_voxel_remesh.stl")

# ------------------------------------------------------
# 4. Decimate（面削減）
# ------------------------------------------------------
dec = obj.modifiers.new("decimate", "DECIMATE")
dec.ratio = DECIMATE_RATIO
bpy.ops.object.modifier_apply(modifier="decimate")

bpy.ops.export_mesh.stl(filepath=f"{OUT_DIR}/step03_decimated.stl")
print("Saved: step03_decimated.stl")

print("All steps completed.")
