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

x1, x2, y1, y2 = 0, 100, 10, 1000
points = np.array([[x1, y1], [x2, y2]])
result = fit_line(points)
print(result)