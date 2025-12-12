const fs = require("fs");

const file = process.argv[2];
const color = process.argv[3]?.split(",").map(Number) || [1, 0, 0, 1]; // デフォルト赤

const gltf = JSON.parse(fs.readFileSync(file, "utf8"));

// materials[0] の色を変更
if (gltf.materials && gltf.materials.length > 0) {
  gltf.materials[0].pbrMetallicRoughness.baseColorFactor = color;
  gltf.materials.alphaMode = 'BLEND';
}

fs.writeFileSync(file, JSON.stringify(gltf, null, 2));
console.log(`Updated ${file} with baseColorFactor = ${color}`);
