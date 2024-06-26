# fbl2024

システムデザイン工学先端ＦＢＬの授業において，ドローンをpythonで扱うためのプログラムになります．

## パッケージを一括でインストール
```
pip install -r requirements.txt
```

## プログラムを動かす前に
1. IPを変更する
   > line6: IP = '192.168.101.27'
3. portを変更する
   > line7: PORT = 8881

## コマンド一覧
qrプログラムでは，以下のコマンドでドローンを操作できます．
line traceプログラムでは，終了コマンドと離陸コマンドのみ使用可能です．
- ESC : 終了
- t : 離陸
- l : 着陸
- w : 前へ
- s : 後ろへ
- a : 左へ
- d : 右へ
- r : 上へ
- c : 下へ
- e : 右回り
- q : 左回り
