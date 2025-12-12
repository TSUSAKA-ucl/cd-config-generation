import bpy
import bmesh
import mathutils

def make_convex_hull(obj, merge_dist=1e-5, quantize=1e-5):
    """
    Blender 3.6 用
    入力オブジェクトの凸包を作成し、量子化誤差や近接点を除去
    
    Parameters
    ----------
    obj : bpy.types.Object
        凸包を作りたいメッシュオブジェクト
    merge_dist : float
        remove_doubles による統合距離
    quantize : float
        座標丸めの単位
    """
    # オブジェクトをアクティブにして object mode
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # BMesh 作成
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    
    # 1. 座標を量子化（丸め）
    for v in bm.verts:
        v.co = mathutils.Vector((
            round(v.co.x / quantize) * quantize,
            round(v.co.y / quantize) * quantize,
            round(v.co.z / quantize) * quantize
        ))
    
    # 2. 近接点統合
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=merge_dist)
    
    # 3. 凸包作成
    result = bmesh.ops.convex_hull(bm, input=bm.verts)
    
    # BMesh をメッシュに反映
    bm.to_mesh(obj.data)
    bm.free()
    
    return obj

# ----------------------------
# 使用例
# ----------------------------
# 既存の選択オブジェクトに対して凸包作成
obj = bpy.context.active_object  # 選択中のオブジェクトを使用
make_convex_hull(obj, merge_dist=1e-5, quantize=1e-5)

# 結果を確認後、必要であればエクスポート
bpy.ops.export_mesh.stl(filepath="/tmp/convex_hull.stl")
print("Convex hull created and exported.")
