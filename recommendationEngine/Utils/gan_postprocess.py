import cv2
import os
import pandas as pd
import numpy as np
import math

def get_tag(center, tag_file):
    dist, color = [], []
    for i in range(len(tag_file)):
        c = tag_file.loc[i,['B','G','R']]
        dist.append(math.sqrt(sum([(a - b) ** 2 for a, b in zip(center, c)])))
    min_i = dist.index(min(dist))
    tag = tag_file['Floor tags'].iloc[min_i]
    return tag


def cluster_image(img):
    Z = img.reshape((-1,3))
    Z = np.float32(Z)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    K = 30
    ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    res = center[label.flatten()]
    res = res.reshape((img.shape))
    return res, center


def black_white(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 75, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 30, maxLineGap=10)
    edges = cv2.bitwise_not(edges)
    gray2 = gray.copy()
    gray2[gray2 >35] =255
    gray2[gray2<35] = 0
    dst = cv2.addWeighted(gray2, 0.5, edges, 0.5, 0.0)
    dst[dst<200] =0
    dst[dst>200] =255
    return dst



def place_text(img,clust, centers, tag_file):
    contours, _ = cv2.findContours(img.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_L1)
    i = 1
    legends = []
    areas = [cv2.contourArea(c) for c in contours if cv2.contourArea(c) < 1000000]
    max_contarea = max(areas)
    print(max_contarea)
    for c in contours:
        cont_area = cv2.contourArea(c)
        if cont_area < 100:
            continue
        elif cont_area > 1000000:
            continue
        else:
            grain = np.int0(cv2.boxPoints(cv2.minAreaRect(c))) 
            centroid =( grain[2][0]-(grain[2][0]-grain[0][0])//2, grain[2][1]-(grain[2][1]-grain[0][1])//2) 
            color = clust[centroid]
            color_list = color.tolist()
            leg={}
            min_rect = cv2.minAreaRect(c)
            if color_list in centers.tolist() and min(min_rect[1][1], min_rect[1][0]) > 20:
                tag = get_tag(color, tag_file)
                cv2.putText(img, str(i),  centroid, cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 0))
                leg['room']=str(i)
                leg['area_perc']=str({'tag': tag, 'area': round((cont_area/max_contarea)*100, 2) })
                legends.append(leg)
                # legends.update({"room":str(i), "area_perc": str({'tag': tag, 'area': round((cont_area/max_contarea)*100, 2) })})
                i+=1
    return img, legends


def gan_convert(img, tag_file):
    cluster_img, centers = cluster_image(img.copy())
    blkwht_img = black_white(cluster_img.copy())
    final_img, legends = place_text(blkwht_img, cluster_img, centers, tag_file)
    return final_img, legends