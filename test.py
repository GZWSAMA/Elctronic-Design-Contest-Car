import cv2
import numpy as np
from vision.vision_location_point import Vision_Location_Point as VL
from vision.vision_detction_coutour import Vision_Detection_Contour as VD
from general.preprocess import pre_process

mode = 'test'
vl = VL(mode = mode)
vd = VD(mode = mode)
# 加载图像或视频帧
image_line = cv2.imread('./datas/line2.jpg')
image_arrow = cv2.imread('./datas/detection_test.jpg')
processed_image_line = pre_process(image_line, scale_percent=0.5)
processed_image_arrow = pre_process(image_arrow, scale_percent=0.1)
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
    cv2.waitKey(0)
    cv2.destroyAllWindows()