#!/usr/bin/env python3
import json
import sys

def describe_json(obj, path="root", depth=0, max_depth=None):
    """
    obj: JSONオブジェクト
    path: 階層表示用文字列
    depth: 現在の階層
    max_depth: 表示する最大階層（Noneで制限なし）
    """
    if max_depth is not None and depth > max_depth:
        print(f"{path} : ... (max depth reached)")
        return

    if isinstance(obj, dict):
        print(f"{path} : object {{ {len(obj)} keys }}")
        if max_depth is None or depth < max_depth:
            for k, v in obj.items():
                describe_json(v, f"{path}.{k}", depth + 1, max_depth)
    elif isinstance(obj, list):
        print(f"{path} : array [{len(obj)} elements]")
        if max_depth is None or depth < max_depth:
            for i, item in enumerate(obj):
                describe_json(item, f"{path}[{i}]", depth + 1, max_depth)
    else:
        print(f"{path} : value ({repr(obj)})")

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description="JSON階層と配列の要素数を表示")
    parser.add_argument("json_file", help="読み込むJSONファイル")
    parser.add_argument("-d", "--depth", type=int, default=None,
                        help="表示する最大階層 (デフォルト: 無制限)")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    try:
        with open(args.json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Failed to read JSON file '{args.json_file}': {e}")
        sys.exit(1)

    describe_json(data, max_depth=args.depth)
