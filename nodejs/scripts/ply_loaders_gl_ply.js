import { load } from '@loaders.gl/core';
import { PLYLoader } from '@loaders.gl/ply';

// ************************
// メイン関数
function main() {
  // ファイルパスを指定
  if (process.argv.length < 3) {
    console.error('使用法: node ply_loader.js <ファイルパス>');
    process.exit(1);
  }
  // リンク形状定義の入力のファイルパス
  const inputPath = process.argv[2] || './shape.ply';
  console.log(inputPath)
  load(inputPath, PLYLoader).then(data => {
    console.log('PLYファイルの読み込みに成功しました。');
    // 読み込んだデータをコンソールに出力
    console.log(data);
  } ).catch(error => {
    console.error('PLYファイルの読み込みに失敗しました:', error);
    process.exit(1);
  });
}

main();
