import cv2
import math
import numpy as np
from scipy.optimize import least_squares

def fit_line(points):
    def error(p, *data):
        x, y = data
        a, b = p
        return y - (a*x + b)
    
    x = points[:, 0]
    y = points[:, 1]
    
    # 初始猜测
    p_init = np.polyfit(x, y, 1)
    
    # 使用最小二乘法优化直线参数
    result = least_squares(error, p_init, args=(x, y))
    return result.x

def find_lane_middle(image,mode = 'test'):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY)
    edges = cv2.Canny(binary, 10, 200, apertureSize=3)
    cv2.imshow('Canny Edge', edges)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, minLineLength=250, maxLineGap=10)
    left_fit = None  # 添加默认值
    right_fit = None  # 添加默认值

    if lines is not None:
        left_lines = []
        right_lines = []
        
        for i, line in enumerate(lines):
            x1, y1, x2, y2 = line[0]
            slope = (y2 - y1) / (x2 - x1)

            if mode == 'test':
                print(f"{i}slope: {slope}")
                # 在图像上绘制点
                cv2.circle(image, (x1, y1), 10, (255, 0, 0), -1)  # 画一个蓝色的点
                cv2.circle(image, (x2, y2), 10, (255, 0, 0), -1)  # 画一个蓝色的点
                
                # 在点旁边添加文本标签
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 1
                font_color = (255, 0, 0)  # 白色字体
                font_thickness = 2
                
                # 标签位置设定在点的正下方
                text_pos_y1 = y1 + 20
                text_pos_y2 = y2 + 20
                
                cv2.putText(image, str(i), (x1, text_pos_y1), font, font_scale, font_color, font_thickness)
                cv2.putText(image, str(i), (x2, text_pos_y2), font, font_scale, font_color, font_thickness)   
            
            if abs(slope) > 3:
                print(f"{i}points: ({x1},{y1}),({x2},{y2})")
                if slope > 0:
                    right_lines.append([(x1, y1), (x2, y2)])
                elif slope < 0:
                    left_lines.append([(x1, y1), (x2, y2)])
                
        # 拟合车道线
        if len(left_lines) > 0:
            left_points = [point for line in left_lines for point in line]
            left_fit = fit_line(np.array(left_points))
            
            # 绘制左侧车道线
            if left_fit is not None:
                y_top = 0
                y_bottom = image.shape[0]
                left_x_top = int((y_top - left_fit[1]) / left_fit[0])
                left_x_bottom = int((y_bottom - left_fit[1]) / left_fit[0])
                cv2.line(image, (left_x_top, y_top), (left_x_bottom, y_bottom), (255, 0, 0), 10)
                
        if len(right_lines) > 0:
            right_points = [point for line in right_lines for point in line]
            right_fit = fit_line(np.array(right_points))
            
            # 绘制右侧车道线
            if right_fit is not None:
                y_top = 0
                y_bottom = image.shape[0]
                right_x_top = int((y_top - right_fit[1]) / right_fit[0])
                right_x_bottom = int((y_bottom - right_fit[1]) / right_fit[0])
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
            cv2.line(image, (middle_top, 0), (middle_bottom, image.shape[0]), (0, 255, 0), 10)
            
            return [middle_bottom, middle_top]
        else:
            return None
    else:
        return None

# 加载图像或视频帧
image = cv2.imread('./datas/line2.jpg')
# 在显示图像前进行缩放
scale_percent = 50  # 缩放比例
width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
dim = (width, height)

# 缩放图像
resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

height, width, _ = resized.shape

# 计算中间30%区域的坐标
cut_persent = 0.5
start_height = int(height * (1-cut_persent)/2)
end_height = int(height * 1-(1-cut_persent)/2)
start_width = 0
end_width = width
cropped_image = resized[start_height:end_height, start_width:end_width]
# 调用函数找到车道中间位置
middle = find_lane_middle(cropped_image)
if middle is not None:
    print(f"Lane Middle: {middle[1]}")
else:
    print("Lane Middle: Not Found")
print(f"Img Midlle: {cropped_image.shape[1]/2}")

# 显示结果
# 显示缩放后的图像
cv2.imshow('Lane Middle', cropped_image)
cv2.waitKey(0)
cv2.destroyAllWindows()