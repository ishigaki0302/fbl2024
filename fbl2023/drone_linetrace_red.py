import socket
import threading
import cv2
import time
import numpy as np
# データ受け取り用の関数
def udp_receiver():
        global battery_text
        global time_text
        global status_text
        while True:
            try:
                data, server = sock.recvfrom(1518)
                resp = data.decode(encoding="utf-8").strip()
                # レスポンスが数字だけならバッテリー残量
                if resp.isdecimal():
                    battery_text = "Battery:" + resp + "%"
                # 最後の文字がsなら飛行時間
                elif resp[-1:] == "s":
                    time_text = "Time:" + resp
                else:
                    status_text = "Status:" + resp
            except:
                pass
# 問い合わせ
def ask():
    while True:
        try:
            sent = sock.sendto('battery?'.encode(encoding="utf-8"), TELLO_ADDRESS)
        except:
            pass
        time.sleep(0.5)
        try:
            sent = sock.sendto('time?'.encode(encoding="utf-8"), TELLO_ADDRESS)
        except:
            pass
        time.sleep(0.5)
# 離陸
def takeoff():
        print("-----")
        try:
            print("ok")
            sent = sock.sendto('takeoff'.encode(encoding="utf-8"), TELLO_ADDRESS)
        except:
            print("error")
            pass
# 着陸
def land():
        try:
            sent = sock.sendto('land'.encode(encoding="utf-8"), TELLO_ADDRESS)
        except:
            pass
# 上昇(20cm)
def up():
        try:
            sent = sock.sendto('up 20'.encode(encoding="utf-8"), TELLO_ADDRESS)
        except:
            pass
# 下降(20cm)
def down():
        try:
            sent = sock.sendto('down 20'.encode(encoding="utf-8"), TELLO_ADDRESS)
        except:
            pass
# 前に進む(20cm)
def forward():
        try:
            sent = sock.sendto('forward 0'.encode(encoding="utf-8"), TELLO_ADDRESS)
        except:
            pass
# 後に進む(20cm)
def back():
        try:
            sent = sock.sendto('back 0'.encode(encoding="utf-8"), TELLO_ADDRESS)
        except:
            pass
# 右に進む(20cm)
def right():
        try:
            sent = sock.sendto('right 0'.encode(encoding="utf-8"), TELLO_ADDRESS)
        except:
            pass
# 左に進む(20cm)
def left():
        try:
            sent = sock.sendto('left 0'.encode(encoding="utf-8"), TELLO_ADDRESS)
        except:
            pass
# 右回りに回転(90 deg)
def cw():
        try:
            sent = sock.sendto('cw 90'.encode(encoding="utf-8"), TELLO_ADDRESS)
        except:
            pass
# 左回りに回転(90 deg)
def ccw():
        try:
            sent = sock.sendto('ccw 90'.encode(encoding="utf-8"), TELLO_ADDRESS)
        except:
            pass
# 速度変更(例：速度40cm/sec, 0 < speed < 100)
def set_speed(n=40):
        try:
            sent = sock.sendto(f'speed {n}'.encode(encoding="utf-8"), TELLO_ADDRESS)
        except:
            pass

            
# Tello側のローカルIPアドレス(デフォルト)、宛先ポート番号(コマンドモード用)
TELLO_IP = '192.168.10.1'
TELLO_PORT = 8889
TELLO_ADDRESS = (TELLO_IP, TELLO_PORT)
# Telloからの映像受信用のローカルIPアドレス、宛先ポート番号
TELLO_CAMERA_ADDRESS = 'udp://@0.0.0.0:11111?overrun_nonfatal=1&fifo_size=50000000'
command_text = "None"
battery_text = "Battery:"
time_text = "Time:"
status_text = "Status:"
# キャプチャ用のオブジェクト
cap = None
# データ受信用のオブジェクト備
response = None
# 通信用のソケットを作成
# ※アドレスファミリ：AF_INET（IPv4）、ソケットタイプ：SOCK_DGRAM（UDP）
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 自ホストで使用するIPアドレスとポート番号を設定
sock.bind(('', TELLO_PORT))
# 問い合わせスレッド起動
ask_thread = threading.Thread(target=ask)
ask_thread.setDaemon(True)
ask_thread.start()
# 受信用スレッドの作成
recv_thread = threading.Thread(target=udp_receiver, args=())
recv_thread.daemon = True
recv_thread.start()
# コマンドモード
sock.sendto('command'.encode('utf-8'), TELLO_ADDRESS)
time.sleep(2)
# カメラ映像のストリーミング開始
sock.sendto('streamon'.encode('utf-8'), TELLO_ADDRESS)
time.sleep(2)
if cap is None:
    cap = cv2.VideoCapture(TELLO_CAMERA_ADDRESS)
if not cap.isOpened():
    cap.open(TELLO_CAMERA_ADDRESS)
# cap = cv2.VideoCapture(0)
time.sleep(2)
count = 0
sent = sock.sendto('setfps low'.encode(encoding="utf-8"), TELLO_ADDRESS)
# Telloクラスを使って，droneというインスタンス(実体)を作る
current_time = time.time()  # 現在時刻の保存変数
pre_time = current_time     # 5秒ごとの'command'送信のための時刻変数
time.sleep(0.5)     # 通信が安定するまでちょっと待つ
# ウィンドウのタイトル
window_title = "OpenCV Window"
out_image = 0
# トラックバーを作るため，まず最初にウィンドウを生成
cv2.namedWindow(window_title, cv2.WINDOW_NORMAL)
# トラックバーのコールバック関数は何もしない空の関数
# コールバック関数（トラックバーが変更されたときに呼ばれる関数）
def on_trackbar(val):
    global out_image
    if out_image is not None:
        # 二値化
        ret, dst = cv2.threshold(out_image, val, 255, cv2.THRESH_BINARY)
        # 画像の表示
        cv2.imshow(window_title, dst)

#############################################

# パラメータ変更部分（You may change following parameters.）
H_MIN, H_MAX = 0, 0
S_MIN, S_MAX = 0, 0
V_MIN, V_MAX = 0, 0

#############################################


# トラックバーの生成
cv2.createTrackbar("H_min", window_title, H_MIN, 179, on_trackbar)
cv2.createTrackbar("H_max", window_title, H_MAX, 179, on_trackbar)     # Hueの最大値は179
cv2.createTrackbar("S_min", window_title, S_MIN, 255, on_trackbar)
cv2.createTrackbar("S_max", window_title, S_MAX, 255, on_trackbar)
cv2.createTrackbar("V_min", window_title, V_MIN, 255, on_trackbar)
cv2.createTrackbar("V_max", window_title, V_MAX, 255, on_trackbar)
a = b = c = d = 0   # rcコマンドの初期値を入力
b = 0              # 前進の値を0に設定
flag = 0

# 繰り返し実行
try:
    while True:
        # (A)画像取得
        ret, frame = cap.read()  # 映像を1フレーム取得
        if frame is None or frame.size == 0:    # 中身がおかしかったら無視
            continue
        image = frame
        # (B)ここから画像処理
        # image = cv2.imread("IMG_7614.jpg")
        # image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)      # OpenCV用のカラー並びに変換する（既にBGRなので現状必要なし）
        small_image = cv2.resize(image, dsize=(480,360) )   # 画像サイズを半分に変更
        bgr_image = small_image[250:359,0:479]              # 注目する領域(ROI)を(0,250)-(479,359)で切り取る
        # cv2.imshow('test Window', bgr_image)
        hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)  # BGR画像 -> HSV画像
        # hsv_image = bgr_image
        # cv2.imshow('test Window', hsv_image)
        # トラックバーの値を取る
        h_min = cv2.getTrackbarPos("H_min", window_title)
        h_max = cv2.getTrackbarPos("H_max", window_title)
        s_min = cv2.getTrackbarPos("S_min", window_title)
        s_max = cv2.getTrackbarPos("S_max", window_title)
        v_min = cv2.getTrackbarPos("V_min", window_title)
        v_max = cv2.getTrackbarPos("V_max", window_title)
        on_trackbar(h_min)
        on_trackbar(h_max)
        on_trackbar(s_min)
        on_trackbar(s_max)
        on_trackbar(v_min)
        on_trackbar(v_max)
        # inRange関数で範囲指定２値化
        bin_image = cv2.inRange(hsv_image, (h_min, s_min, v_min), (h_max, s_max, v_max)) # HSV画像なのでタプルもHSV並び
        kernel = np.ones((15,15),np.uint8)  # 15x15で膨張させる
        dilation_image = cv2.dilate(bin_image,kernel,iterations = 1)    # 膨張して虎ロープをつなげる
        #erosion_image = cv2.erode(dilation_image,kernel,iterations = 1)    # 収縮
        # bitwise_andで元画像にマスクをかける -> マスクされた部分の色だけ残る
        masked_image = cv2.bitwise_and(hsv_image, hsv_image, mask=dilation_image)
        # ラベリング結果書き出し用に画像を準備
        out_image = masked_image
        # 面積・重心計算付きのラベリング処理を行う
        num_labels, label_image, stats, center = cv2.connectedComponentsWithStats(dilation_image)
        # 最大のラベルは画面全体を覆う黒なので不要．データを削除
        num_labels = num_labels - 1
        stats = np.delete(stats, 0, 0)
        center = np.delete(center, 0, 0)
        if num_labels >= 1:
            # 面積最大のインデックスを取得
            max_index = np.argmax(stats[:,4])
            #print max_index
            # 面積最大のラベルのx,y,w,h,面積s,重心位置mx,myを得る
            x = stats[max_index][0]
            y = stats[max_index][1]
            w = stats[max_index][2]
            h = stats[max_index][3]
            s = stats[max_index][4]
            mx = int(center[max_index][0])
            my = int(center[max_index][1])
            print("(x,y)=%d,%d (w,h)=%d,%d s=%d (mx,my)=%d,%d"%(x, y, w, h, s, mx, my) )
            # ラベルを囲うバウンディングボックスを描画
            cv2.rectangle(out_image, (x, y), (x+w, y+h), (255, 0, 255))
            # 重心位置の座標を表示
            # cv2.putText(out_image, "%d,%d"%(mx,my), (x-15, y+h+15), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0))
            cv2.putText(out_image, "%d"%(s), (x, y+h+15), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0))
            # a：左右，b：前後，c：上下，d：ヨー角
            if flag == 1:
                # a=c=d=0，　b=40が基本．
                # 左右旋回のdだけが変化する．
                # 前進速度のbはキー入力で変える．
                dx = 1.0 * (240 - mx)       # 画面中心との差分
                # 旋回方向の不感帯を設定
                d = 0.0 if abs(dx) < 50.0 else dx   # ±50未満ならゼロにする
                d = -d
                # 旋回方向のソフトウェアリミッタ(±70を超えないように)
                d =  70 if d >  70.0 else d
                d = -70 if d < -70.0 else d
                print('dx=%f'%(dx) )
                sock.sendto(('rc %s %s %s %s'%(int(a), int(b), int(c), int(d))).encode(encoding="utf-8"), TELLO_ADDRESS )
        # (X)ウィンドウに表示
        out_image = masked_image
        cv2.imshow('OpenCV Window', out_image)  # ウィンドウに表示するイメージを変えれば色々表示できる
        # (Y)OpenCVウィンドウでキー入力を1ms待つ
        key = cv2.waitKey(1)

        # escキーで終了
        if key == 27:
            break
        # wキーで前進
        elif key == ord('w'):
            forward()
            command_text = "Forward"
        # sキーで後進
        elif key == ord('s'):
            back()
            command_text = "Back"
        # aキーで左進
        elif key == ord('a'):
            left()
            command_text = "Left"
        # dキーで右進
        elif key == ord('d'):
            right()
            command_text = "Right"
        # tキーで離陸
        elif key == ord('t'):
            takeoff()
            command_text = "Take off"
        # lキーで着陸
        elif key == ord('l'):
            land()
            command_text = "Land"
        # rキーで上昇
        elif key == ord('r'):
            up()
            command_text = "Up"
        # cキーで下降
        elif key == ord('c'):
            down()
            command_text = "Down"
        # qキーで左回りに回転
        elif key == ord('q'):
            ccw()
            command_text = "Ccw"
        # eキーで右回りに回転
        elif key == ord('e'):
            cw()
            command_text = "Cw"
        # 追跡モードをON
        elif key == ord('1'):
            flag = 1
        # 追跡モードをOFF
        elif key == ord('2'):
            flag = 0
            sock.sendto('rc 0 0 0 0'.encode(encoding="utf-8"), TELLO_ADDRESS )
        elif key == ord('y'):           # 前進速度をキー入力で可変
            b = b + 10
            if b > 100:
                b = 100
        elif key == ord('h'):
            b = b - 10
            if b < 0:
                b = 0
        # (Z)5秒おきに'command'を送って、死活チェックを通す
        current_time = time.time()  # 現在時刻を取得
        if current_time - pre_time > 5.0 :  # 前回時刻から5秒以上経過しているか？
            sock.sendto('command'.encode(encoding="utf-8"), TELLO_ADDRESS)   # 'command'送信
            pre_time = current_time         # 前回時刻を更新
except( KeyboardInterrupt, SystemExit):    # Ctrl+cが押されたら離脱
    print( "SIGINTを検知" )
# cap.release()
cv2.destroyAllWindows()
# ビデオストリーミング停止
sock.sendto('streamoff'.encode('utf-8'), TELLO_ADDRESS)