import threading, queue, logging
import cv2
from djitellopy import Tello, TelloSwarm
import numpy as np

IP = '192.168.101.27'
PORT = 8881

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

# ライントレース用の画像処理関数
# ------------------------------------
def process_frame_for_line_trace(img_bgr):
    hsv_image = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    # HSVのしきい値
    h_min, h_max = 0, 179
    s_min, s_max = 0, 255
    v_min, v_max = 0, 255
    # トラックバーの値を取得（仮の値、必要に応じて調整）
    h_min = cv2.getTrackbarPos("H_min", "Trackbars")
    h_max = cv2.getTrackbarPos("H_max", "Trackbars")
    s_min = cv2.getTrackbarPos("S_min", "Trackbars")
    s_max = cv2.getTrackbarPos("S_max", "Trackbars")
    v_min = cv2.getTrackbarPos("V_min", "Trackbars")
    v_max = cv2.getTrackbarPos("V_max", "Trackbars")
    # 指定した範囲でHSV画像を二値化
    mask = cv2.inRange(hsv_image, (h_min, s_min, v_min), (h_max, s_max, v_max))
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=2)
    mask = cv2.dilate(mask, kernel, iterations=2)
    # 重心計算
    moments = cv2.moments(mask, False)
    try:
        cx = int(moments["m10"] / moments["m00"])
        cy = int(moments["m01"] / moments["m00"])
        cv2.circle(img_bgr, (cx, cy), 10, (0, 0, 255), -1)
    except ZeroDivisionError:
        cx, cy = img_bgr.shape[1] // 2, img_bgr.shape[0] // 2
    return img_bgr, cx
# ------------------------------------

# ライン追跡スレッド
# ------------------------------------
def line_trace():
    global current_frame
    while running:
        frame = tello.get_frame_read().frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        with frame_lock:
            processed_frame, cx = process_frame_for_line_trace(frame)
            current_frame = processed_frame
            control_drone(cx, frame.shape[1] // 2)
# ドローンの制御関数
def control_drone(cx, frame_center):
    if cx < frame_center - 20:
        tello.move_left(20)
    elif cx > frame_center + 20:
        tello.move_right(20)
    else:
        tello.move_forward(20)
# ------------------------------------

# Telloストリームの開始と離陸
# ------------------------------------
tello.streamon()
tello.takeoff()
# ------------------------------------

# 変数の定義
# ------------------------------------
frame_lock = threading.Lock()
current_frame = None
running = True
# ------------------------------------

# スレッドの設定と開始
# ------------------------------------
line_trace_thread = threading.Thread(target=line_trace)
line_trace_thread.start()
# ------------------------------------

# メインループ
# ------------------------------------
cv2.namedWindow("Trackbars")
cv2.createTrackbar("H_min", "Trackbars", 0, 179, lambda x: None)
cv2.createTrackbar("H_max", "Trackbars", 179, 179, lambda x: None)
cv2.createTrackbar("S_min", "Trackbars", 0, 255, lambda x: None)
cv2.createTrackbar("S_max", "Trackbars", 255, 255, lambda x: None)
cv2.createTrackbar("V_min", "Trackbars", 0, 255, lambda x: None)
cv2.createTrackbar("V_max", "Trackbars", 255, 255, lambda x: None)
while True:
    with frame_lock:
        if current_frame is not None:
            cv2.imshow('Tello Line Trace', current_frame)
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESCキーのコード
        break
# ------------------------------------

# スレッドの終了待ち
# ------------------------------------
running = False
line_trace_thread.join()
# ------------------------------------

# Telloのストリームを終了し、着陸
# ------------------------------------
tello.streamoff()
tello.land()
telloswarm.end()
cv2.destroyAllWindows()
# ------------------------------------
