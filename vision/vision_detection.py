#coding = utf-8
import cv2
import numpy as np
import matplotlib.pyplot as plt

# 读取模板图像和测试图像
template_img = cv2.imread('arrow_template.jpg', 0)  # 灰度模式
test_img = cv2.imread('test_image.jpg', 0)          # 灰度模式

# 初始化SIFT特征检测器
sift = cv2.SIFT_create()

# 在模板图像和测试图像上找到关键点和描述符
keypoints_template, descriptors_template = sift.detectAndCompute(template_img, None)
keypoints_test, descriptors_test = sift.detectAndCompute(test_img, None)

# 创建BFMatcher对象
bf = cv2.BFMatcher()

# 匹配描述符
matches = bf.knnMatch(descriptors_template, descriptors_test, k=2)

# 应用比率测试
good_matches = []
for m,n in matches:
    if m.distance < 0.75*n.distance:
        good_matches.append([m])

# 如果有足够的匹配点，计算单应性矩阵
MIN_MATCH_COUNT = 10
if len(good_matches) > MIN_MATCH_COUNT:
    src_pts = np.float32([ keypoints_template[m.queryIdx].pt for m in good_matches[0] ]).reshape(-1,1,2)
    dst_pts = np.float32([ keypoints_test[m.trainIdx].pt for m in good_matches[0] ]).reshape(-1,1,2)

    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    matchesMask = mask.ravel().tolist()

    h,w = template_img.shape
    pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
    dst = cv2.perspectiveTransform(pts,M)

    test_img = cv2.polylines(test_img,[np.int32(dst)],True,255,3, cv2.LINE_AA)
else:
    print( "Not enough matches are found - {}/{}".format(len(good_matches), MIN_MATCH_COUNT) )
    matchesMask = None

draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                   singlePointColor = None,
                   matchesMask = matchesMask, # draw only inliers
                   flags = 2)

# 画出匹配
img3 = cv2.drawMatchesKnn(template_img,keypoints_template,test_img,keypoints_test,good_matches,None,**draw_params)

plt.imshow(img3,),plt.show()