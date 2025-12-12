import bpy
import os
import math

# ======== 設定 ========
WRL_PATH = "./step03_decimated.wrl"
OUT_DIR = "output_parts"
os.makedirs(OUT_DIR, exist_ok=True)
# ======================

# 全オブジェクト削除
bpy.ops.wm.read_factory_settings(use_empty=True)

# VRML インポート
bpy.ops.import_scene.x3d(filepath=WRL_PATH)

# blenderは、VRML(.wrl)では座標系がY-upであるとして
# インポート時に自動でrpy={Pi/2, 0, Pi} の回転補正が行われるため、それを戻す
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        # print('rotation_euler (before):', obj.rotation_euler)
        # rotation_eulerは {Pi/2, 0, Pi}なので、0にする
        obj.rotation_euler[0] = 0  # X 回転を戻す
        obj.rotation_euler[1] = 0  # Y 回転を戻す
        obj.rotation_euler[2] = 0  # Z 回転を戻す

# すべて選択解除
bpy.ops.object.select_all(action='DESELECT')

# シーン内のすべてのメッシュを収集
parts = [obj for obj in bpy.data.objects if obj.type == 'MESH']

for i, obj in enumerate(parts):
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    # 位置・回転・スケールを適用（必要なら）
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    # 書き出し
    output_path = os.path.join(OUT_DIR, f"convex_{i:03d}.stl")
    bpy.ops.export_mesh.stl(filepath=output_path, use_selection=True)
    obj.select_set(False)

    print(f"Exported: {output_path}")

print("All convex parts exported.")
