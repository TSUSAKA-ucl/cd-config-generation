#!/bin/bash
BBOX_MLX=`mktemp`
cat >"$BBOX_MLX" <<EOF
<!DOCTYPE FilterScript>
<FilterScript>
  <filter name="Compute Geometric Measures"/>
</FilterScript>
EOF
[ $# -lt 1 ] && echo "usage:$0 file" 1>&2 && exit 1
while [ $# -ge 1 ]
do  OutFile=`echo "$1"|sed -e 's/\.[a-zA-Z]\+$/.bbox/;t;d'`
    [ "$OutFile" = "" ] && echo Error in "$1". 1>&2 && exit 1
    meshlabserver -i "$1" -o /dev/null -s "$BBOX_MLX" 2>&1 | \
	grep '^Mesh ' > "$OutFile"
    shift
done
rm "$BBOX_MLX"
#
# when use pymeshlab
# import pymeshlab

# ms = pymeshlab.MeshSet()
# ms.load_new_mesh('input_model.dae')

# # 1. スケーリングを実行 (引数名を最新仕様に合わせ、uniformflagを有効化)
# # axisx, axisy, axisz を指定します
# ms.apply_filter('compute_matrix_from_scaling_or_normalization', 
#                 axisx=0.001, 
#                 uniformflag=True)

# # 2. 行列をフリーズ（頂点座標に反映）させる
# # これにより、変換行列がリセットされ、頂点データそのものが 1/1000 になります
# ms.apply_filter('apply_matrix_freeze')

# # バウンディングボックスの表示
# m = ms.current_mesh()
# bbox = m.bounding_box()
# print(f"Size: {bbox.dim_x()}, {bbox.dim_y()}, {bbox.dim_z()}")

