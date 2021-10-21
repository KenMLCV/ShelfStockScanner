# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 03:31:09 2021

@author: Kenyon
"""
import stat
import glob
import os
import re
import random
import datetime
import math
import numpy as np
import cv2

def find_boxes(filename, src_path='cereal_box_images_dst/', dst_path='cereal_box_images_hough/'):
    src_path =src_path+ filename
    dst_path =dst_path+ filename
    src_img = cv2.imread(src_path)
    img = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)
    img = cv2.Canny(img, 50, 200, None, 3)
    thresh = 70
    lines = cv2.HoughLines(img, 1, np.pi / 180, thresh, None, 0, 0)
    while len(lines) > 20:
        thresh = thresh + 5
        lines = cv2.HoughLines(img, 1, np.pi / 180, thresh, None, 0, 0)
        
    # Draw the lines
    if lines is not None:
        try:
            for i in range(0, len(lines)):
                rho = lines[i][0][0]
                theta = lines[i][0][1]
                a = math.cos(theta)
                b = math.sin(theta)
                x0 = a * rho
                y0 = b * rho
                pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
                pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
                slope = abs((pt2[1] - pt1[1])/(pt2[0] - pt1[0]))
                #slope = 5.0
                #print(str((pt2[1] - pt1[1])/(pt2[0] - pt1[0])))
                if(slope > 2.0 or slope < 0.5):
                    #print(slope)
                    cv2.line(src_img, pt1, pt2, (0,0,255), 3, cv2.LINE_AA)
        except:
            pass
    cv2.imwrite(dst_path, src_img)
def generate_product(storage_name):
    
    timestamp = str(int(datetime.datetime.now().timestamp()))
    
    store_idx = random.randrange(3)
    store_names = ['Kroger', 'Whole Foods', 'Publix', 'Aldi']
    store_name = store_names[store_idx]
    
    camera_id = str(random.randrange(3))
    
    barcode_information = []
    for i in range(0,13):
        barcode_information.append(str(random.randrange(9)))
    barcode_information = ''.join(barcode_information)
         
    storage_name = re.sub('[^A-Za-z0-9.]+', '', storage_name)
    return [storage_name, timestamp, store_name, camera_id, barcode_information]
def clean_file_names(path):
    for count, filename in enumerate(os.listdir(path)):
        #dst ="Hostel" + str(count) + ".jpg"
        src =path+ filename
        dst =path+ re.sub('[^A-Za-z0-9.]+', '',filename)
          
        # rename() function will
        # rename all the files
        os.rename(src, dst)
def clear_directory(path):
    files = glob.glob('{}*'.format(path))
    for f in files:
        os.chmod(f, stat.S_IWRITE)
        os.remove(f)