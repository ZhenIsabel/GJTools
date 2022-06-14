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

def show_every_check_region():
    image = cv2.cvtColor(np.asarray(
        pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
    bottom_right = (config.config['my_card_region'][0]+config.config['my_card_region'][2], config.config['my_card_region'][1]+config.config['my_card_region'][3])
    cv2.rectangle(image, config.config['my_card_region'][:2], bottom_right, 255, 2)
    bottom_right = (config.config['score_region'][0]+config.config['score_region'][2], config.config['score_region'][1]+config.config['score_region'][3])
    cv2.rectangle(image, config.config['score_region'][:2], bottom_right, 255, 2)
    bottom_right = (config.config['card_pool_region'][0]+config.config['card_pool_region'][2], config.config['card_pool_region'][1]+config.config['card_pool_region'][3])
    cv2.rectangle(image, config.config['card_pool_region'][:2], bottom_right, 255, 2)
    bottom_right = (config.config['first_card_loc_in_pool'][0]+20, config.config['first_card_loc_in_pool'][1]+20)
    cv2.rectangle(image, config.config['first_card_loc_in_pool'][:2], bottom_right, 255, 2)
    bottom_right = (config.config['opponent_count_region'][0]+config.config['opponent_count_region'][2], config.config['opponent_count_region'][1]+config.config['opponent_count_region'][3])
    cv2.rectangle(image, config.config['opponent_count_region'][:2], bottom_right, 255, 2)
    
    utils.show_imag(image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

time.sleep(1)
config.init_config()
show_every_check_region()
