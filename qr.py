import threading, queue, logging, time
import cv2
from djitellopy import Tello, TelloSwarm
import numpy as np

IP = '192.168.0.12'
PORT = 8887

# TelloSwarmの設定
# ------------------------------------
telloswarm = TelloSwarm.fromIps([IP])
tello = telloswarm.tellos[0]
tello.LOGGER.setLevel(logging.ERROR)
tello.connect()
print(f'Tello Battery : {tello.get_battery()}')
# ------------------------------------

# ビデオ設定
# ------------------------------------
tello.change_vs_udp(PORT)
tello.set_video_resolution(Tello.RESOLUTION_480P)
tello.set_video_bitrate(Tello.BITRATE_1MBPS)
# ------------------------------------

# QRコードの認識と表示
# ------------------------------------
def function_qrdec_cv2(img_bgr):
    qrd = cv2.QRCodeDetector()
    retval, decoded_info, points, straight_qrcode = qrd.detectAndDecodeMulti(img_bgr)
    if retval:
        points = points.astype(np.int32)
        for dec_inf, point in zip(decoded_info, points):
            if dec_inf == '':
                continue
            # QRコード座標取得
            x = point[0][0]
            y = point[0][1]
            # QRコードデータ
            print('QR Code detected:', dec_inf)
            # バウンディングボックス
            img_bgr = cv2.polylines(img_bgr, [point], True, (0, 255, 0), 1, cv2.LINE_AA)
    return img_bgr
# ------------------------------------

# QRスレッド
# ------------------------------------
def qr_code_detection():
    global current_frame
    while running:
        frame = tello.get_frame_read().frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        with frame_lock:
            current_frame = function_qrdec_cv2(frame)
# ------------------------------------

# ドローン操作スレッド
# ------------------------------------
def tello_control(command_queue):
    while running:
        if not command_queue.empty():
            command = command_queue.get()
            if command == "t":
                tello.takeoff()
            elif command == "l":
                tello.land()
            elif command == 'w':
                tello.move_forward(20)
            elif command == 's':
                tello.move_back(20)
            elif command == 'a':
                tello.move_left(20)
            elif command == 'd':
                tello.move_right(20)
            elif command == 'r':
                tello.move_up(20)
            elif command == 'c':
                tello.move_down(20)
            elif command == 'e':
                tello.rotate_counter_clockwise(20)
            elif command == 'q':
                tello.rotate_clockwise(20)
# ------------------------------------

# Telloストリームの開始
# ------------------------------------
tello.streamon()
# ------------------------------------

# 変数の定義
# ------------------------------------
frame_lock = threading.Lock()
current_frame = None
running = True
command_queue = queue.Queue()
# ------------------------------------

# スレッドの設定と開始
# ------------------------------------
qr_thread = threading.Thread(target=qr_code_detection)
control_thread = threading.Thread(target=tello_control, args=(command_queue,))
qr_thread.start()
control_thread.start()
# ------------------------------------

# メインループ
# ------------------------------------
while True:
    with frame_lock:
        if current_frame is not None:
            cv2.imshow(f'Tello', current_frame)
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESCキーのコード
        break
    else:
        command_queue.put(chr(key))
# ------------------------------------

# スレッドの終了待ち
# ------------------------------------
running = False
qr_thread.join()
control_thread.join()
# ------------------------------------

# Telloのストリームを終了
# ------------------------------------
tello.streamoff()
telloswarm.end()
cv2.destroyAllWindows()
# ------------------------------------