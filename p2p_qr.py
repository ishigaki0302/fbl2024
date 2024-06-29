import threading, queue, logging, time
import cv2
from djitellopy import Tello
import numpy as np

XY_SPEED = 20
Z_SPEED = 20
ROTATION_SPEED = 20

# TelloSwarmの設定
# ------------------------------------
tello = Tello()
tello.connect()
print(f'Tello Battery : {tello.get_battery()}')
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
                tello.move_forward(XY_SPEED)
            elif command == 's':
                tello.move_back(XY_SPEED)
            elif command == 'a':
                tello.move_left(XY_SPEED)
            elif command == 'd':
                tello.move_right(XY_SPEED)
            elif command == 'r':
                tello.move_up(Z_SPEED)
            elif command == 'c':
                tello.move_down(Z_SPEED)
            elif command == 'q':
                tello.rotate_counter_clockwise(ROTATION_SPEED)
            elif command == 'e':
                tello.rotate_clockwise(ROTATION_SPEED)
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
cv2.destroyAllWindows()
# ------------------------------------