#!/usr/bin/env node

/**
 * Usage:
 *   node set-gltf-color.js model.gltf --color "#ff0000" --opacity 0.5
 *
 * color: CSS形式の16進 (#rrggbb) または rgb(255,0,0)
 * opacity: 0.0〜1.0
 */

const fs = require("fs");
const path = require("path");
const yargs = require("yargs/yargs");
const { hideBin } = require("yargs/helpers");

// 引数パース
const argv = yargs(hideBin(process.argv))
  .usage("Usage: $0 <gltf_file> --color <hex> --opacity <0-1>")
  .option("color", {
    alias: "c",
    describe: "Base color in hex (#rrggbb)",
    type: "string",
    demandOption: true,
  })
  .option("opacity", {
    alias: "o",
    describe: "Opacity (0.0-1.0)",
    type: "number",
    default: 1.0,
  })
  .demandCommand(1, "You must provide a glTF file")
  .help()
  .argv;

const gltfPath = argv._[0];

// 色文字列 -> [r, g, b] (0〜1)
function parseHexColor(hex) {
  if (hex.startsWith("#")) hex = hex.slice(1);
  if (hex.length !== 6) throw new Error("Color must be 6-digit hex");
  const r = parseInt(hex.slice(0, 2), 16) / 255;
  const g = parseInt(hex.slice(2, 4), 16) / 255;
  const b = parseInt(hex.slice(4, 6), 16) / 255;
  return [r, g, b];
}

// glTF 読み込み
let gltf;
try {
  const text = fs.readFileSync(gltfPath, "utf-8");
  gltf = JSON.parse(text);
} catch (err) {
  console.error("Failed to read glTF file:", err.message);
  process.exit(1);
}

// materials が無ければ作る
if (!gltf.materials) gltf.materials = [];

const baseColor = parseHexColor(argv.color);
const alpha = argv.opacity;

gltf.materials.forEach((mat) => {
  if (!mat.pbrMetallicRoughness) mat.pbrMetallicRoughness = {};
  mat.pbrMetallicRoughness.baseColorFactor = [baseColor[0], baseColor[1], baseColor[2], alpha];

  // 透明度を有効にするため、alphaMode を "BLEND" に
  mat.alphaMode = "BLEND";
});

// 上書き保存
try {
  fs.writeFileSync(gltfPath, JSON.stringify(gltf, null, 2), "utf-8");
  console.log(`Updated materials in ${gltfPath}`);
} catch (err) {
  console.error("Failed to write glTF file:", err.message);
  process.exit(1);
}
