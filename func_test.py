import cv2
from vision.vision_detction_coutour import Vision_Detection_Contour as VD

vd = VD('test')

image_arrow = cv2.imread('./datas/4.png')
gray = cv2.cvtColor(image_arrow, cv2.COLOR_BGR2GRAY)


# 应用高斯模糊减少噪声
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
# 边缘检测
edges = cv2.Canny(blurred, 50, 150, apertureSize=3)

# 查找轮廓
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

max_area = 0
largest_heptagon = None

# 遍历所有轮廓
for cnt in contours:
    # 近似轮廓
    epsilon = 0.02 * cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, epsilon, True)
    cv2.drawContours(image_arrow, [cnt], 0, (0, 255, 0), 3)
    
    # 检查近似轮廓是否为七边形
    if len(approx) == 7 and cv2.contourArea(approx) > 1000:
        area = cv2.contourArea(approx)
        if area > max_area:
            max_area = area
            largest_heptagon = approx

# 如果找到了七边形
if largest_heptagon is not None:
    # 绘制最大面积的七边形
    cv2.drawContours(image_arrow, [largest_heptagon], 0, (0, 0, 255), 3)
cv2.imshow("image_arrow", image_arrow)
cv2.waitKey(0)