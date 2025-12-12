import fs from 'fs';

const buffer = fs.readFileSync('output.json');
const data = JSON.parse(buffer.toString());
console.log(data);
console.log(data[0]); // 最初の点の座標を表示
console.log(typeof data[0]); // 最初の点の型を表示
console.log(typeof data[0][0]); // 最初の点のx座標の型を表示
