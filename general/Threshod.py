import cv2
import numpy as np

def update_threshold(val):
    # 获取当前滑动条的值作为阈值
    threshold = val
    
    # 应用阈值处理
    _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    
    # 显示二值化图像
    cv2.imshow('Binary Image', binary)

# 加载图像
image = cv2.imread('./datas/line2.jpg')
scale_percent = 50  # 缩放比例
width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
dim = (width, height)

# 缩放图像
resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

# 将图像转换为灰度图
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
cv2.imshow('gray Image', gray)

# 创建窗口并命名
cv2.namedWindow('Binary Image')

# 创建滑动条并绑定到窗口
cv2.createTrackbar('Threshold', 'Binary Image', 0, 255, update_threshold)

# 设置滑动条的默认值
cv2.setTrackbarPos('Threshold', 'Binary Image', 127)

# 初始显示
update_threshold(127)

# 主循环
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# 清理
cv2.destroyAllWindows()