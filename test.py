import cv2
import numpy as np
from vision.vision_location_point import Vision_Location_Point as VL
from vision.vision_detction_coutour import Vision_Detection_Contour as VD
from general.preprocess import pre_process

def capture_image():
    # 检查摄像头是否成功打开
    if not cap.isOpened():
        print("无法打开摄像头")
        exit()

    # 读取一帧图像
    ret, frame = cap.read()

    # 检查是否成功读取帧
    if not ret:
        print("无法获取帧")
        exit()

    return frame

def run():
    mode = 'test'
    vl = VL(mode = mode)
    vd = VD(mode = mode)
    while True:
        # 加载图像或视频帧
        # image_line = cv2.imread('./datas/line2.jpg')
        # image_arrow = cv2.imread('./datas/detection_test.jpg')
        image_line = capture_image()
        image_arrow = capture_image()

        if image_line is None or image_arrow is None:
            print("Image is empty!")
            continue
        cv2.imshow("image_line", image_line)
        cv2.imshow("image_arrow", image_arrow)
        cv2.waitKey(10)

        processed_image_line = pre_process(image_line, scale_percent=1)
        processed_image_arrow = pre_process(image_arrow, scale_percent=1)
        # 调用函数找到车道中间位置
        vl.find_lane_middle(processed_image_line)
        vd.detect_largest_heptagon(processed_image_arrow)
        if vl.line_middle is not None:
            print(f"Lane Middle: {vl.line_middle}")
        else:
            print("Lane Middle: Not Found")
        print(f"Img Midlle: {vl.vision_middle}")

        if vd.left_point is not None:
            print(f"Left Point: {vd.left_point}")
        else:
            print("Left Point: Not Found")

        # 显示结果
        # 显示缩放后的图像
        if mode == 'test':
            cv2.imshow('Lane Middle', processed_image_line)
            cv2.waitKey(10)
            cv2.destroyAllWindows()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    # 打开默认摄像头，通常索引为0
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, 30)
    run()