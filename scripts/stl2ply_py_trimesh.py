import trimesh
import sys
import os

def convert_stl_to_ply_ascii(input_path, output_path):
    # メッシュを読み込み (自動でバイナリ/ASCII STLの区別を処理)
    mesh = trimesh.load(input_path, force='mesh')

    if mesh.is_empty:
        raise ValueError("Loaded mesh is empty or invalid")

    # 出力ディレクトリ作成
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # ASCII PLY で書き出し
    # trimesh.export で ply はデフォルトASCII形式
    mesh.export(output_path, file_type='ply')

    print(f"Converted: {input_path} -> {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python stl_to_ply.py input.stl output.ply")
        sys.exit(1)

    convert_stl_to_ply_ascii(sys.argv[1], sys.argv[2])
