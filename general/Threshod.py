import cv2
import numpy as np

def capture_image(cap):
    if cap == 'cap1':
        ret, frame = cap1.read()
    elif cap == 'cap2':
        ret, frame = cap2.read()
    else:
        print("Invalid camera")
        return None
    return frame if ret else None

def update_threshold(gray, val):
    _, binary = cv2.threshold(gray, val, 255, cv2.THRESH_BINARY)
    cv2.imshow('Binary Image', binary)

cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)  # Initialize cap2 even if it's not used

cv2.namedWindow('Binary Image')

# 由于cv2.createTrackbar的限制，我们使用lambda函数来包装update_threshold，
# 这样可以传递额外的参数gray
current_gray = None  # 定义一个全局变量来存储当前的gray图像

def set_current_gray(gray):
    global current_gray
    current_gray = gray

cv2.createTrackbar('Threshold', 'Binary Image', 0, 255, lambda val: update_threshold(current_gray, val) if current_gray is not None else None)
cv2.setTrackbarPos('Threshold', 'Binary Image', 127)

while True:
    image = capture_image('cap1')
    if image is None:
        break
    
    scale_percent = 50
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    cv2.imshow('gray Image', gray)
    
    # 更新全局变量current_gray
    set_current_gray(gray)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap1.release()
cap2.release()
cv2.destroyAllWindows()