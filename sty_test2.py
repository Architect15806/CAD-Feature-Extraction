import os
import numpy as np
import cv2
import sys

im_path = "annotation_mask/01.png"
im = cv2.imread(im_path, 0)


ret, im = cv2.threshold(im, 127, 255, cv2.THRESH_BINARY)
element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))

skel = np.zeros(im.shape, np.uint8)
temp = np.zeros(im.shape, np.uint8)

i = 0
while True:
    # cv2.imshow('im %d' % (i), im)
    # 取开运算过程中消失的像素，这些像素便是skeleton的一部分
    temp = cv2.morphologyEx(im, cv2.MORPH_OPEN, element)
    temp = cv2.bitwise_not(temp)
    temp = cv2.bitwise_and(im, temp)
    # cv2.imshow('skeleton part %d' % (i,), temp)

    # 将删除的像素添加skeleton图中
    skel = cv2.bitwise_or(skel, temp)
    # 再次腐蚀原图，为进一步寻找skeleton做准备
    im = cv2.erode(im, element)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(im)
    # print min_val, max_val, min_loc, max_loc
    if max_val == .0:
        break
    i += 1

import imageio

imageio.imwrite('annotation_mask/out.jpeg', skel)

cv2.imshow('Skeleton', skel)
cv2.waitKey()