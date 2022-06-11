import time

import utils
import cv2
import numpy as np
import pyautogui
import config
import math

color_pic = [cv2.imread('img/red.png'),
             cv2.imread('img/green.png'),
             cv2.imread('img/blue.png'),
             cv2.imread('img/yellow.png')
             ]

#颜色RBG取值
# color = {
#     "blue": {"color_lower": np.array([100, 43, 46]), "color_upper": np.array([124, 255, 255])},
#     "red": {"color_lower": np.array([156, 43, 46]), "color_upper": np.array([180, 255, 255])},
#     "yellow": {"color_lower": np.array([26, 43, 46]), "color_upper": np.array([34, 255, 255])},
#     "green": {"color_lower": np.array([35, 43, 46]), "color_upper": np.array([77, 255, 255])},
#     "purple": {"color_lower": np.array([125, 43, 46]), "color_upper": np.array([155, 255, 255])},
#     "orange": {"color_lower": np.array([11, 43, 46]), "color_upper": np.array([25, 255, 255])}
#          }
color = {
    "blue": {"color_lower": np.array([100, 43, 106]), "color_upper": np.array([125, 180, 200])},
    "red": {"color_lower": np.array([156, 43, 46]), "color_upper": np.array([180, 255, 255])},
    "yellow": {"color_lower": np.array([21, 43, 46]), "color_upper": np.array([34, 100, 255])},
    "green": {"color_lower": np.array([35, 43, 46]), "color_upper": np.array([77, 255, 255])},
         }
time.sleep(1)


image = cv2.imread('D:/06-11-13-17-08.png')

def FlannBasedShowMatch(template,img):
    # 寻找关键点和描述符 
    orb = cv2.ORB_create()
    kp_img, des_img = orb.detectAndCompute(img, None)
    kp_temp, des_temp = orb.detectAndCompute(template, None)

    # FLANN 参数
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks=50)  
    # 使用FlannBasedMatcher 寻找最近邻近似匹配
    flann = cv2.FlannBasedMatcher(index_params,search_params)
    # 使用knnMatch匹配处理，并返回匹配matches
    matches = flann.knnMatch(des_temp, des_img, k=2)
    matches_mask=[[0,0]for i in range(len(matches))]
    for i,(m,n) in enumerate(matches):
        if m.distance<0.7*n.distance:
            matches_mask[i]=[1,0]
    
    draw_params=dict(matchColor=(0,255,0),singlePointColor=(255,0,0),matchesMask=matches_mask,flags=0)
    im_show=cv2.drawMatchesKnn(img,kp_img,template,kp_temp,matches,None,**draw_params)
    # plt.figure(figsize=(20,20))
    # plt.imshow(im_show,cmap='gray')
    # plt.show()
    utils.show_imag(im_show)
    pass


def content(color_name, imge):
    color = {
    "blue": {"color_lower": np.array([100, 43, 106]), "color_upper": np.array([125, 180, 200])},
    "red": {"color_lower": np.array([156, 43, 46]), "color_upper": np.array([180, 255, 255])},
    "yellow": {"color_lower": np.array([21, 43, 46]), "color_upper": np.array([34, 100, 255])},
    "green": {"color_lower": np.array([35, 43, 46]), "color_upper": np.array([77, 255, 255])},
         }
    img = cv2.cvtColor(imge, cv2.COLOR_BGR2HSV)         #转成HSV
    img = cv2.GaussianBlur(img, (5, 5), 0)              #高斯滤波降噪，模糊图片
    # img = cv2.threshold(img, 127,255, cv2.THRESH_BINARY)[1]
    color_img = cv2.inRange(img, color[color_name]["color_lower"], color[color_name]["color_upper"])#筛选出符合的颜色
    kernel = np.ones((3, 3), np.uint8)              #核定义
    color_img = cv2.erode(color_img, kernel, iterations=2)  #腐蚀除去相关性小的颜色
    color_img = cv2.GaussianBlur(color_img, (5, 5), 0)      #模糊图像
    cnts = cv2.findContours(color_img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0] #找出轮廓
    centers=[]
    for cnt in cnts:                #遍历所有符合的轮廓
        x, y, w, h = cv2.boundingRect(cnt)
        if w*h<15*20:
            continue
        cv2.rectangle(imge, (x, y), (x+w, y+h), (0, 0, 255), 2)
        centers.append([int((x+w)/2),int((y+h)/2)])
    return centers


content('green', image[  840: 840+ 180,714:714+900])
