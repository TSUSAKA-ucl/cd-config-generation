import trimesh
import sys

def convert_stl_to_obj(input_path, output_path):
    mesh = trimesh.load(input_path, force='mesh')
    if not isinstance(mesh, trimesh.Trimesh):
        raise ValueError("入力STLが単一メッシュでない可能性があります。")

    # 座標変換なしでそのままOBJへ
    mesh.export(output_path, file_type='obj')
    print(f"Saved: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python stl2obj.py input.stl output.obj")
        sys.exit(1)

    convert_stl_to_obj(sys.argv[1], sys.argv[2])
