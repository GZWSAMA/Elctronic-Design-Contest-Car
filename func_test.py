import cv2
import numpy as np

def find_nearest_black_pixels(binary_image):
    # 获取图像的宽度和高度
    height, width = binary_image.shape
    
    # 图像中心的横坐标
    center_x = width // 2
    
    # 初始化左右两侧黑色像素的位置
    left_black_x = None
    right_black_x = None
    
    # 向左搜索
    for x in range(center_x - 1, -1, -1):
        if binary_image[height // 2, x] == 0:
            left_black_x = x
            break
    
    # 向右搜索
    for x in range(center_x + 1, width):
        if binary_image[height // 2, x] == 0:
            right_black_x = x
            break
    
    # 返回找到的黑色像素的位置
    return left_black_x, right_black_x

# 示例：读取二值化图像
image = cv2.imread('./datas/line2.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, binary_image = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY)

# 调用函数
left_black_x, right_black_x = find_nearest_black_pixels(binary_image)

# 输出结果
print(f"Nearest black pixel to the left of center is at x={left_black_x}")
print(f"Nearest black pixel to the right of center is at x={right_black_x}")

# 可选：在图像上标记找到的像素点
height, _ = binary_image.shape
if left_black_x is not None:
    cv2.circle(binary_image, (left_black_x, height // 2), 5, (255), -1)
if right_black_x is not None:
    cv2.circle(binary_image, (right_black_x, height // 2), 5, (255), -1)

# 显示图像
cv2.imshow('Binary Image with Marked Pixels', binary_image)
cv2.waitKey(0)
cv2.destroyAllWindows()