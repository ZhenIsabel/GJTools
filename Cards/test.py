import time

from Cards import utils
import cv2
import numpy as np
import pyautogui
from Cards import config
import math

color_pic = [cv2.imread('img/red.png'),
             cv2.imread('img/green.png'),
             cv2.imread('img/blue.png'),
             cv2.imread('img/yellow.png')
             ]

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

time.sleep(1)
def test(fun,*args):
    fun(*args)

def inside(x,y):
    print(str(x)+','+str(y))

test(inside,1,0)