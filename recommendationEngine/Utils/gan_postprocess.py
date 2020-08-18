import cv2
import os
import pandas as pd
import numpy as np
import math
from scipy.spatial import distance

def get_tag(center, tag_file):
    dist, color = [], []
    for i in range(len(tag_file)):
        c = tag_file.loc[i,['B','G','R']]
        # dist.append(math.sqrt(sum([(a - b) ** 2 for a, b in zip(center, c)])))
        dist.append(distance.euclidean(center, c))
    min_i = dist.index(min(dist))
    tag = tag_file['Floor tags'].iloc[min_i]
    # print(tag)
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



def place_text(img,clust, centers, tag_file,length,width,bedrooms):
    contours, _ = cv2.findContours(img.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_L1)
    i = 1
    legends = []
    areas = [cv2.contourArea(c) for c in contours if cv2.contourArea(c) < 1000000]
    
    max_contarea=sum(areas)
    total_area=int(length)*int(width)
    areali=[]
    a=[]
    puttextlabels=[]
    tags=[]
    centroids=[]
    bedcount=0
    tagli=[]
    numli=[]
    cen=[]
    for c in contours:
        cont_area = cv2.contourArea(c)
        if cont_area < 100:
            continue
        elif cont_area > 1000000:
            continue
        else:
            grain = np.int0(cv2.boxPoints(cv2.minAreaRect(c))) 
            centroid =( grain[2][0]-(grain[2][0]-grain[0][0])//3, grain[2][1]-(grain[2][1]-grain[0][1])//3) 
            color = clust[centroid]
            color_list = color.tolist()
            leg={}
            
            min_rect = cv2.minAreaRect(c)
            if color_list in centers.tolist() and min(min_rect[1][1], min_rect[1][0]) > 10:
                area_perc=round((cont_area/max_contarea)*100, 2)
                tag = get_tag(color, tag_file)
                leg['room']=str(i)
                leg['area_perc']=tag+"-"+str(area_perc)
                if tag!='stair':
                    if area_perc>5:
                        
                        if tag=="bedroom":
                            bedcount+=1
                            if bedcount<=bedrooms:
                                puttextlabels.append({str(i):[centroid,tag,area_perc]})
                                tags.append(tag)
                        else:
                            if tag not in tags:
                                if tag!='clos':
                                    puttextlabels.append({str(i):[centroid,tag,area_perc]})
                                    tags.append(tag)
                                else:
                                    areali.append(area_perc)
                                    centroids.append(centroid)
                            else:
                                areali.append(area_perc)
                                centroids.append(centroid)
                    i+=1 
                else:
                    areali.append(area_perc)
                    centroids.append(centroid)  
                
            else:
                area_perc=round((cont_area/max_contarea)*100, 2)
                areali.append(area_perc)
                centroids.append(centroid)  
                
    desc_area=areali
    desc_area.sort(reverse=True)
    if "living/ dining" in tags :
        roomnames=['kitchen','bath']
    elif  "kitchen/ dining" in tags:
        roomnames=['living','dining','bath']
    else:
        roomnames=['living','dining','kitchen','bath']
    tot_rooms=len(roomnames)+bedrooms
    for j in range(0,len(roomnames)):
        if (roomnames[j] not in tags) and (j<len(desc_area)):
            
            tags.append(roomnames[j])
            puttextlabels.append({str(i):[centroids[areali.index(desc_area[j])],roomnames[j],desc_area[j]]})
            i+=1
    print("end for loop")
    while (bedrooms-bedcount)!=0:
        print("inside while")
        if j <len(desc_area):
            print("inside while if")
            tags.append("bedroom")
            puttextlabels.append({str(i):[centroids[areali.index(desc_area[j])],"bedroom",desc_area[j]]})
            j+=1
            i+=1
            print(i,j,bedcount,bedrooms)
        bedcount+=1
        print(bedrooms-bedcount)
        # else:
        #     bedcount+=1
    area=[]
    for p in puttextlabels:
        area.append(list(p.values())[0][2])
    area.sort(reverse=True)
    # print(puttextlabels)
    final_legends=[]
    done=[]
    for a in area:
        for p in puttextlabels:
            if list(p.values())[0][2] == a:
                name=str(list(p.values())[0][1])
                areaperc=list(p.values())[0][2]
                centroid=list(p.values())[0][0]
                
                if areaperc not in done:
                    done.append(areaperc)
                    cv2.putText(img, list(p.keys())[0],  centroid, cv2.FONT_HERSHEY_SIMPLEX,1.5, (109, 111, 115),thickness=3)
                    
                    final_legends.append({"room":list(p.keys())[0],"area_perc":name+"-"+str(areaperc)})

    used_area_perc=0
    for l in final_legends:
        used_area_perc+=float(l['area_perc'].split('-')[-1])
    unplanned_openspace=100-used_area_perc
    leg={}
    i+=1
    leg['room']=str(i)
    leg['area_perc']="open_space"+"-"+str(round(unplanned_openspace),2)
    final_legends.append(leg)
    leg={}
    i+=1
    leg['room']=str(i)
    leg['area_perc']="planned_floor_area"+"-"+str(round(used_area_perc),2)
    final_legends.append(leg)
    print("**********************")
    print(puttextlabels)
    print(final_legends)
    print("*******************************")
    return img, final_legends


def gan_convert(img, tag_file,length,width,bedrooms):
    cluster_img, centers = cluster_image(img.copy())
    blkwht_img = black_white(cluster_img.copy())
    final_img, legends = place_text(blkwht_img, cluster_img, centers, tag_file,length,width,bedrooms)
    return final_img, legends

