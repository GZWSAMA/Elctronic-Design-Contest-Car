import cv2

def pre_process(image, scale_percent):
    # 在显示图像前进行缩放
        width = int(image.shape[1] * scale_percent)
        height = int(image.shape[0] * scale_percent)
        dim = (width, height)

        # 缩放图像
        resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
        return resized

def select_point(points):
        final_point = None
        if isinstance(points, list) and len(points) > 1:
            for i in range(len(points)):
                if points[len(points)-1 - i] != 0.0:
                    final_point = points[len(points)-1 - i]        
        else:
            final_point = points
        return final_point