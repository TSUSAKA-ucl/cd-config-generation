# gjk_testcase_generator.py
# Generate test cases for GJK algorithm including edge-edge, face-face, and vertex-face contacts.
# Output: JSON file with test cases (vertices of shape A and B, expected collision result)

import json
import numpy as np


def create_box(center, size):
    cx, cy, cz = center
    sx, sy, sz = size
    dx = sx / 2
    dy = sy / 2
    dz = sz / 2
    return [
        [cx - dx, cy - dy, cz - dz],
        [cx + dx, cy - dy, cz - dz],
        [cx + dx, cy + dy, cz - dz],
        [cx - dx, cy + dy, cz - dz],
        [cx - dx, cy - dy, cz + dz],
        [cx + dx, cy - dy, cz + dz],
        [cx + dx, cy + dy, cz + dz],
        [cx - dx, cy + dy, cz + dz],
    ]


def generate_test_cases():
    cases = []

    # 1. Face-to-face contact (perfectly aligned)
    box1 = create_box([0, 0, 0], [2, 2, 2])
    box2 = create_box([0, 0, 2], [2, 2, 2])  # face-to-face contact on Z
    cases.append({"name": "face_to_face", "A": box1, "B": box2, "expect_collision": True})

    # 2. Edge-to-edge contact
    box1 = create_box([0, 0, 0], [2, 2, 2])
    box2 = create_box([2, 2, 0], [2, 2, 2])  # edges touch at (1,1,0)
    cases.append({"name": "edge_to_edge", "A": box1, "B": box2, "expect_collision": True})

    # 3. Vertex-to-face near miss
    box1 = create_box([0, 0, 0], [2, 2, 2])
    box2 = create_box([2.01, 2.01, 0], [2, 2, 2])  # barely no collision
    cases.append({"name": "vertex_near_miss", "A": box1, "B": box2, "expect_collision": False})

    # 4. Deep penetration
    box1 = create_box([0, 0, 0], [2, 2, 2])
    box2 = create_box([0.5, 0.5, 0.5], [2, 2, 2])
    cases.append({"name": "deep_penetration", "A": box1, "B": box2, "expect_collision": True})

    # 5. Separated shapes
    box1 = create_box([0, 0, 0], [2, 2, 2])
    box2 = create_box([10, 10, 10], [2, 2, 2])
    cases.append({"name": "no_contact", "A": box1, "B": box2, "expect_collision": False})

    return cases


if __name__ == "__main__":
    test_cases = generate_test_cases()
    with open("gjk_testcases.json", "w") as f:
        json.dump(test_cases, f, indent=2)
    print("Generated gjk_testcases.json with", len(test_cases), "test cases.")
