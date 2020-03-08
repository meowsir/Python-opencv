import cv2
import numpy as np
from matplotlib import pyplot as plt
import os
import math
import time

filename = 'jump.jpg'

while True:
    os.system('adb shell /system/bin/screencap -p /sdcard/jump.png')
    os.system('adb pull /sdcard/jump.png C:/Users/13285/OneDrive/学习/代码/python/opencv/jump.jpg')
    img = cv2.imread(filename, 0)
    template = cv2.imread('p.jpg', 0)
    h, w = template.shape[:2]  # rows->h, cols->w
    h0, w0 = img.shape[:2] 

    # 相关系数匹配方法：cv2.TM_CCOEFF
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    left_top = max_loc  # 左上角
    right_bottom = (left_top[0] + w, left_top[1] + h)  # 右下角
    play_loc = (int(left_top[0] + w / 2), left_top[1] + h)  # 小人的中心

    img_blur = cv2.GaussianBlur(img, (5, 5), 0)  # 高斯模糊
    canny_img = cv2.Canny(img, 20, 30)
    # cv2.namedWindow('img', 0)
    # cv2.imshow("img", canny_img)
    # cv2.waitKey(0)

    for y in range(max_loc[1] - 10, max_loc[1] + h + 10):
        for x in range(max_loc[0] - 10, max_loc[0] + w + 10):
            canny_img[y][x] = 0
    # cv2.namedWindow('img', 0)
    # cv2.imshow("img", canny_img)
    # cv2.waitKey(0)

    height, width = canny_img.shape
    crop_img = canny_img[800:int(height/2), 0:width]
    cv2.namedWindow('img', 0)
    cv2.imshow("img", crop_img)
    cv2.waitKey(1000)

    crop_h, crop_w = crop_img.shape
    center_x, center_y = 0, 0

    max_x = 0
    if play_loc[0] < w0 / 2:  
        print('left')
        for y in range(crop_h):
            for x in range(crop_w):
                if crop_img[y, x] == 255:
                    if center_x == 0:
                        center_x = x
                    if x > max_x:
                        center_y = y
                        max_x = x
        center_y += 800
    else:
        print('right')
        for y in range(crop_h):
            for x in range(crop_w):
                min_x = 99999
                ymin = 0
                if crop_img[y, x] == 255:
                    if center_x == 0:
                        center_x = x
                        ymin = y
                    if x < min_x:
                        center_y = y
                        min_x = x
        center_y -= 100
        # center_y -= int((center_y - ymin) * 2 / 5)
        center_y += 800

    # 重新加载图片 标点 
    img = cv2.imread(filename, 0)

    play_loc = (int(left_top[0] + w / 2), left_top[1] + h - 10)  # 小人的中心
    cv2.circle(img, play_loc, 10, 255, -1)
    cv2.circle(img, (center_x, center_y), 10, (0, 255, 255), -1)  # 要去的中心
    cv2.namedWindow('img', 0)
    cv2.imshow("img", img)

    # cv2.waitKey(0)

    p1 = np.array([play_loc[0], play_loc[1]])
    p2 = np.array([center_x, center_y])
    p3 = p2-p1
    p4 = math.hypot(p3[0], p3[1])
    print(p4)

    dis = str(int(p4 * 1.36))
    com = 'adb shell input swipe 500 500 500 500 ' + dis
    os.system(com)

    time.sleep(1)
    # print('第' + str(i) + '次')
