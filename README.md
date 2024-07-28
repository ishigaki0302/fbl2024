# fbl2024 and International Workshop

システムデザイン工学先端ＦＢＬの授業において，ドローンをpythonで扱うためのプログラムになります．
This program is designed for the Advanced FBL in System Design Engineering course and the international workshop, where we will be using Python to work with drones.


## パッケージを一括でインストール（Install all packages at once）
```
pip install -r requirements.txt
```

## drone_qr.py

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

書き換える場所
```
# 前に進む(0cm)
def forward():
        try:
            sent = sock.sendto('forward 0'.encode(encoding="utf-8"), TELLO_ADDRESS)
        except:
            pass
# 後に進む(0cm)
def back():
        try:
            sent = sock.sendto('back 0'.encode(encoding="utf-8"), TELLO_ADDRESS)
        except:
            pass
# 右に進む(0cm)
def right():
        try:
            sent = sock.sendto('right 0'.encode(encoding="utf-8"), TELLO_ADDRESS)
        except:
            pass
# 左に進む(0cm)
def left():
        try:
            sent = sock.sendto('left 0'.encode(encoding="utf-8"), TELLO_ADDRESS)
        except:
            pass
```

## drone_linetrace.py
コマンド一覧
- ESC : 終了
- 1 : ライントレース開始
- 2 : ライントレース終了
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

書き換える場所
```
# 前に進む(0cm)
def forward():
        try:
            sent = sock.sendto('forward 0'.encode(encoding="utf-8"), TELLO_ADDRESS)
        except:
            pass
# 後に進む(0cm)
def back():
        try:
            sent = sock.sendto('back 0'.encode(encoding="utf-8"), TELLO_ADDRESS)
        except:
            pass
# 右に進む(0cm)
def right():
        try:
            sent = sock.sendto('right 0'.encode(encoding="utf-8"), TELLO_ADDRESS)
        except:
            pass
# 左に進む(0cm)
def left():
        try:
            sent = sock.sendto('left 0'.encode(encoding="utf-8"), TELLO_ADDRESS)
        except:
            pass
```
```
# パラメータ変更部分（You may change following parameters.）
H_MIN, H_MAX = 0, 0
S_MIN, S_MAX = 0, 0
V_MIN, V_MAX = 0, 0
```
```
b = 0              # 前進の値を0に設定
```
