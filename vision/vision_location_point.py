import cv2
import math
import sys
import numpy as np
from scipy.optimize import least_squares

class Vision_Location_Point:
    """
    vision_location_point
    """
    def __init__(self, mode):
        self.line_middle = None
        self.vision_middle = None
        self.mode = mode
        self.line_threshold = 10
        self.flag = False
    def pre_process(self, image):
            # 在显示图像前进行缩放
        scale_percent = 0.5 # 缩放比例
        width = int(image.shape[1] * scale_percent)
        height = int(image.shape[0] * scale_percent)
        dim = (width, height)

        # 缩放图像
        resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
        return resized

    def fit_line(self, points):
        def error(p, *data):
            x, y = data
            a, b = p
            return y - (a*x + b)
        
        x = points[:, 0]
        y = points[:, 1]
        
        try:
            p_init = np.polyfit(x, y, 1)
        except Exception as e:
            # 处理拟合失败的情况
            return None
        
        # 使用最小二乘法优化直线参数
        result = least_squares(error, p_init, args=(x, y))
        return result.x

    def find_nearest_black_pixels(self, binary_image, H_persent):
        # 获取图像的宽度和高度
        height, width = binary_image.shape
        
        # 图像中心的横坐标
        center_x = width // 2
        H = int(height * H_persent)
        
        # 初始化左右两侧黑色像素的位置
        left_black_x = None
        right_black_x = None
        
        # 向左搜索
        for x in range(center_x - 1, -1, -1):
            if binary_image[H, x] == 0:
                left_black_x = x
                break
        
        # 向右搜索
        for x in range(center_x + 1, width):
            if binary_image[H, x] == 0:
                right_black_x = x
                break
        
        # 返回找到的黑色像素的位置
        return [(left_black_x, H),(right_black_x, H)]

    def find_lane_middle(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY)
        cv2.imshow("Binary Image", binary)
        right_lines = []
        left_lines = []

        line_points_1 = self.find_nearest_black_pixels(binary, 0.65)
        line_points_2 = self.find_nearest_black_pixels(binary, 0.6)
        if line_points_1[0] is None or line_points_1[1] is None or line_points_2[0] is None or line_points_2[1] is None:
            return None
        right_lines.append([line_points_1[1], line_points_2[1]])
        left_lines.append([line_points_1[0], line_points_2[0]])
        
        # 拟合车道线
        if len(left_lines) > 0:
            left_points = [point for line in left_lines for point in line]
            left_fit = self.fit_line(np.array(left_points))
            
            # 绘制左侧车道线
            if left_fit is not None:
                y_top = 0
                y_bottom = image.shape[0]
                left_x_top = int((y_top - left_fit[1]) / left_fit[0])
                left_x_bottom = int((y_bottom - left_fit[1]) / left_fit[0])
                if self.mode == 'test':
                    cv2.line(image, (left_x_top, y_top), (left_x_bottom, y_bottom), (255, 0, 0), 10)
                
        if len(right_lines) > 0:
            right_points = [point for line in right_lines for point in line]
            right_fit = self.fit_line(np.array(right_points))
            
            # 绘制右侧车道线
            if right_fit is not None:
                y_top = 0
                y_bottom = image.shape[0]
                right_x_top = int((y_top - right_fit[1]) / right_fit[0])
                right_x_bottom = int((y_bottom - right_fit[1]) / right_fit[0])
                if self.mode == 'test':
                    cv2.line(image, (right_x_top, y_top), (right_x_bottom, y_bottom), (0, 0, 255), 10)
                
        # 计算车道中间位置
        if left_fit is not None and right_fit is not None:
            y_bottom = image.shape[0]
            y_top = 0
            left_bx = int((y_bottom - left_fit[1]) / left_fit[0])
            left_tx = int((y_top - left_fit[1]) / left_fit[0])
            right_bx = int((y_bottom - right_fit[1]) / right_fit[0])
            right_tx = int((y_top - right_fit[1]) / right_fit[0])
            middle_bottom = int((left_bx + right_bx) / 2)
            middle_top = int((left_tx + right_tx) / 2)
            
            # 绘制车道中间位置
            if self.mode == 'test':
                cv2.line(image, (middle_top, 0), (middle_bottom, image.shape[0]), (0, 255, 0), 10)
            
            if self.flag is False and middle_bottom is not None: 
                self.line_middle = [0.0, 0.0, 0.0]               
                self.flag = True
            if self.line_middle is not None:
                if len(self.line_middle) >= self.line_threshold:
                    # 删除最旧的一组数据
                    self.line_middle.pop(0)

                # 添加新的坐标对
                self.line_middle.append(middle_bottom)
            self.vision_middle = image.shape[1]/2
        else:
            print("No lane found")
