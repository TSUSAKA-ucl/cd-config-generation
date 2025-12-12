import trimesh
import sys

def convert_obj_to_stl(input_path, output_path):
    mesh = trimesh.load(input_path, force='mesh')
    if not isinstance(mesh, trimesh.Trimesh):
        raise ValueError("入力OBJが単一メッシュでない可能性があります。")

    # 座標系は変更しない
    mesh.export(output_path, file_type='stl')
    print(f"Saved: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python obj2stl.py input.obj output.stl")
        sys.exit(1)

    convert_obj_to_stl(sys.argv[1], sys.argv[2])
