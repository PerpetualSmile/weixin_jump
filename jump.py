import subprocess
import os
import time
import cv2
import numpy as np

template_img = cv2.imread('template.png', 0)

# 获取人物的位置
def getPosition1(img):
    res = cv2.matchTemplate(img, template_img, 5)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    x, y = max_loc
    return (x + template_img.shape[1]/2, y + template_img.shape[0] - 20)

# 获取下一个目标物体的中心点位置
def getPosition2(img, position1):
    # 截取人物上方的图片，排除下方干扰
    img = img[0:int(position1[1]), :]
    template = np.zeros(200, dtype=np.uint8) + 245
    template.resize(10, 20)
    res = cv2.matchTemplate(img, template, 0)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    x, y = min_loc
    return (x + template.shape[1]/2, y + template.shape[0]/2)

def calDelay(count):
    img = cv2.imread('screenshots/' + str(count) + '.png', 0)
    position1 = getPosition1(img)
    position2 = getPosition2(img, position1)
    distance = np.sqrt((position1[0] - position2[0])**2 +(position1[1] - position2[1])**2)
    delay = distance * 1.345
    return int(delay)

if __name__ == '__main__':
    path = os.path.abspath(os.getcwd() + "/screenshots")
    if not os.path.isdir(path):
        os.makedirs(path)
    count = 0
    while count <= 20:
        time.sleep(2)
        sub=subprocess.Popen("adb shell screencap -p /sdcard/1.png", shell=True, stdout=subprocess.PIPE)
        sub.wait()
        sub=subprocess.Popen("adb pull /sdcard/1.png " + os.path.abspath(path + "/" + str(count) + ".png"), shell=True, stdout=subprocess.PIPE)
        sub.wait()
        sub=subprocess.Popen("adb shell rm /sdcard/1.png", shell=True, stdout=subprocess.PIPE)
        sub.wait()
        delay = calDelay(count)
        sub=subprocess.Popen("adb shell input swipe 100 100 200 200 " + str(delay), shell=True, stdout=subprocess.PIPE)
        sub.wait()
        count += 1