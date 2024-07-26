# fbl2024 and International Workshop

システムデザイン工学先端ＦＢＬの授業において，ドローンをpythonで扱うためのプログラムになります．
This program is designed for the Advanced FBL in System Design Engineering course and the international workshop, where we will be using Python to work with drones.


## パッケージを一括でインストール（Install all packages at once）
```
pip install -r requirements.txt
```

## プログラムを動かす前に
1. IPを変更する
   > line6: IP = '192.168.101.27'
   - drone01_ip = '192.168.0.11'
   - drone02_ip = '192.168.0.12'
   - drone03_ip = '192.168.0.13'
   - drone04_ip = '192.168.0.14'
   - drone05_ip = '192.168.0.15'
   - drone06_ip = '192.168.0.16'
   - drone07_ip = '192.168.0.17'
   - drone08_ip = '192.168.0.18'
   - drone09_ip = '192.168.0.19'
   - drone10_ip = '192.168.0.20'

3. portを変更する
   > line7: PORT = 8881
   - drone01_port = 10001
   - drone02_port  = 10002
   - drone03_port  = 10003
   - drone04_port  = 10004
   - drone05_port  = 10005
   - drone06_port  = 10006
   - drone07_port  = 10007
   - drone08_port  = 10008
   - drone09_port  = 10009
   - drone10_port  = 10010

## qr.py
カメラにQRコードを写すとコマンドライン上に内容が表示されます．

コマンド一覧
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

## line_trace.py
コマンド一覧
- ESC : 終了
- p : ライントレース開始
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
