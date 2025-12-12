0. x 現在のリポジトリをemscripten用に組み換え
1. 一気にWASMとNode.jsでテスト
   1. x in_house_jacobianを見て、in_house_fk作成
   2. Node.jsでplyモデルを読み込む
   3. JointModelFlatStructを参考に点群用structを作り、そのvectorをwasmに送る
3. jsでpairを読み込みwasm用に変換し送る
4. ジョイント角列をNode.jsで読み込んで
   1. wasmのfk&model座標変換に送る
   2. pairでC.D.を行う
   3. 結果を書く
