# fbl2024

システムデザイン工学先端ＦＢＬの授業において，ドローンをpythonで扱うためのプログラムになります．

## パッケージを一括でインストール
```
pip install -r requirements.txt
```

## プログラムを動かす前に
1. IPを変更する
   > line8: telloswarm = TelloSwarm.fromIps(['192.168.101.27'])
3. portを変更する
   > line17: tello.change_vs_udp(8881)
