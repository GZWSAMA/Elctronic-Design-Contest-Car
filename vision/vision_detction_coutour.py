import cv2
import numpy as np

def pre_process(image):
        # 在显示图像前进行缩放
    scale_percent = 10  # 缩放比例
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)

    # 缩放图像
    resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    return resized

def detect_largest_heptagon(image_path):
    # 读取图像
    img = cv2.imread(image_path)
    img = pre_process(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 边缘检测
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    
    # 查找轮廓
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    max_area = 0
    largest_heptagon = None
    
    # 遍历所有轮廓
    for cnt in contours:
        # 近似轮廓
        epsilon = 0.02 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        
        # 检查近似轮廓是否为七边形
        if len(approx) == 7:
            area = cv2.contourArea(approx)
            if area > max_area:
                max_area = area
                largest_heptagon = approx
    
    # 如果找到了七边形
    if largest_heptagon is not None:
        # 绘制最大面积的七边形
        cv2.drawContours(img, [largest_heptagon], 0, (0, 255, 0), 3)
        
                # 找到最左边的点
        leftmost_point = largest_heptagon[largest_heptagon[:,:,0].argmin()][0]
        
        # 打印最左边点的坐标
        print("Leftmost Point of the Largest Heptagon:", leftmost_point)
    
    # 显示结果
    cv2.imshow('Largest Heptagon Detection', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 调用函数
detect_largest_heptagon('./datas/detection_test.jpg')