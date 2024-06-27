import threading, queue, logging, time
import cv2
from djitellopy import Tello, TelloSwarm
import numpy as np

IP = '192.168.0.12'
PORT = 10002

H_MIN, H_MAX = 1, 10
S_MIN, S_MAX = 36, 255
V_MIN, V_MAX = 50, 200

FORWARD_SPEED = 30
ROTATION_SPEED = 40

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

# ライトレースの処理
# ------------------------------------
def process_light_trace(img_bgr):
    global start_flag
    small_image = cv2.resize(img_bgr, dsize=(480, 360))
    bgr_image = small_image[250:359, 0:479]
    hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)
    # ハードコーディングされたトラックバーの値
    h_min, h_max = H_MIN, H_MAX
    s_min, s_max = S_MIN, S_MAX
    v_min, v_max = V_MIN, V_MAX
    bin_image = cv2.inRange(hsv_image, (h_min, s_min, v_min), (h_max, s_max, v_max))
    kernel = np.ones((15, 15), np.uint8)
    dilation_image = cv2.dilate(bin_image, kernel, iterations=1)
    masked_image = cv2.bitwise_and(hsv_image, hsv_image, mask=dilation_image)
    num_labels, label_image, stats, center = cv2.connectedComponentsWithStats(dilation_image)
    num_labels -= 1
    if num_labels > 0:
        stats = np.delete(stats, 0, 0)
        center = np.delete(center, 0, 0)
        max_index = np.argmax(stats[:, 4])
        x = stats[max_index][0]
        y = stats[max_index][1]
        w = stats[max_index][2]
        h = stats[max_index][3]
        mx = int(center[max_index][0])
        my = int(center[max_index][1])
        cv2.rectangle(masked_image, (x, y), (x + w, y + h), (255, 0, 255))
        cv2.putText(masked_image, "%d" % stats[max_index][4], (x, y + h + 15), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0))
        # dx と dy は、画面中心と検出したオブジェクトの中心との差分を計算することで，ライントレースを実現する
        dx = 1.0 * (240 - mx)  # 画面中心との差分
        dy = 1.0 * (180 - my)  # 画面中心との差分
        a, b, c, d = 0, FORWARD_SPEED, 0, 0  # 初期値
        if abs(dx) > 50:
            d = -dx
            d = ROTATION_SPEED if d > ROTATION_SPEED else d
            d = (ROTATION_SPEED * -1) if d < (ROTATION_SPEED * -1) else d
        if abs(dy) > 50:
            b = FORWARD_SPEED if dy > 0 else (FORWARD_SPEED * -1)
        if start_flag:
            command_queue.put((a, b, c, d))
    return masked_image
# ------------------------------------

# ドローン操作スレッド
# ------------------------------------
def tello_control(command_queue):
    global start_flag
    while running:
        if not command_queue.empty():
            command = command_queue.get()
            if len(command) == 1:
                if command == "p":
                    start_flag = True
                elif command == "t":
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
            else:
                # a: 左右の動き（右が正、左が負）
                # b: 前後の動き（前が正、後が負）
                # c: 上下の動き（上が正、下が負）
                # d: 回転の動き（時計回りが正、反時計回りが負）
                a, b, c, d = command
                tello.send_rc_control(int(a), int(b), int(c), int(d))
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
start_flag = False
# ------------------------------------

# スレッドの設定と開始
# ------------------------------------
def video_stream():
    global current_frame
    while running:
        frame = tello.get_frame_read().frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        with frame_lock:
            current_frame = process_light_trace(frame)
stream_thread = threading.Thread(target=video_stream)
control_thread = threading.Thread(target=tello_control, args=(command_queue,))
stream_thread.start()
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
stream_thread.join()
control_thread.join()
# ------------------------------------

# Telloのストリームを終了
# ------------------------------------
tello.streamoff()
telloswarm.end()
cv2.destroyAllWindows()
# ------------------------------------