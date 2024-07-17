#coding = utf-8
import cv2
import serial
from vision.vision_location_point import Vision_Location_Point as VL
from vision.vision_detction_coutour import Vision_Detection_Contour as VD
from general.tools import pre_process,select_point

def capture_image(cap):
    if cap == 'cap1':
        # 检查摄像头是否成功打开
        if not cap1.isOpened():
            print("无法打开摄像头")
            exit()

        # 读取一帧图像
        ret, frame = cap1.read()

        # 检查是否成功读取帧
        if not ret:
            print("无法获取帧")
            exit()
    elif cap == 'cap2':
        # 检查摄像头是否成功打开
        if not cap2.isOpened():
            print("无法打开摄像头")
            exit()

        # 读取一帧图像
        ret, frame = cap2.read()

        # 检查是否成功读取帧
        if not ret:
            print("无法获取帧")
            exit()
    else:
        print("Invalid camera")
        return None
    return frame

def send_list_over_serial(command, data_list):
    try:
        if ser.isOpen():
            # 将列表转换为字符串，使用逗号作为分隔符
            # 使用str()函数确保所有元素都被转换为字符串
            data_str = ','.join(map(str, data_list))
            
            # 将字符串编码为字节串
            data_bytes = (command + data_str + '\r\n').encode('utf-8')
            
            # 发送数据
            ser.write(data_bytes)
            
            print("数据发送成功")
    
    except Exception as e:
        print(f"发生错误: {e}")

def run():
    vl = VL(mode = mode)
    vd = VD(mode = mode)
    try:
        vs = VS(mode = mode)#mode：test会产生效果图；run不会产生效果图
        ax = AX()

        while True:
            image_line = capture_image(cap = 'cap1')
            if cap_mode == 'one':
                image_arrow = capture_image(cap = 'cap1')
            else:
                image_arrow = capture_image(cap = 'cap2')

            if image_line is None or image_arrow is None:
                print("Image is empty!")
                continue
            
            if mode == 'test':
                cv2.imshow("image_line", image_line)
                cv2.imshow("image_arrow", image_arrow)
                cv2.waitKey(10)

            processed_image_line = pre_process(image_line, scale_percent=1)
            processed_image_arrow = pre_process(image_arrow, scale_percent=1)
            # 调用函数找到车道中间位置
            vl.find_lane_middle(processed_image_line)
            vd.detect_largest_heptagon(processed_image_arrow)
            if vd.left_point == vd.vision_middle:
                send_list_over_serial('A', 'T')
            if ser.in_waiting > 0:
                # 读取一行数据
                line = ser.readline().decode('utf-8').strip()
                # 分割数据，假设命令在第一个位置
                parts = line.split()
                command = parts[0]
                data =parts[1:]
                #传入数据为后续部分

                # 根据命令调用相应的函数
                if command == "X":
                    if select_point(vl.line_middle) is None:
                        send_list_over_serial(command, 'N')
                    else:
                        send_list_over_serial(command, int(select_point(vl.line_middle)))
                else:
                    print(f"Invalid command{command}")
    except KeyboardInterrupt:
        ser.close()

        # 释放摄像头资源
        cap.release()

if __name__ == "__main__":
    # 初始化串口
    ser = serial.Serial('/dev/ttyTHS0', 9600) 
    mode = 'test'
    cap_mode = 'one'
    # 打开默认摄像头，通常索引为0
    if cap_mode == 'one':
        cap1 = cv2.VideoCapture(0)
    else:
        cap1 = cv2.VideoCapture(0)
        cap2 = cv2.VideoCapture(1)
    run(mode, cap_mode)