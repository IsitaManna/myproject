import cv2
import numpy as np
import matplotlib.pyplot as plt
import sklearn
from skimage.color import rgb2gray
import pandas as pd
from PIL import Image
from PIL import Image, ImageDraw, ImageFont
import math
from scipy.spatial import distance
from django.conf import settings

def color_white(img, noise_removal_threshold=60, corners_threshold=0.1,
               room_closing_max_length=80, gap_in_wall_threshold=80):
    """

    :param img: grey scale image of rooms, already eroded and doors removed etc.
    :param noise_removal_threshold: Minimal area of blobs to be kept.
    :param corners_threshold: Threshold to allow corners. Higher removes more of the house.
    :param room_closing_max_length: Maximum line length to add to close off open doors.
    :param gap_in_wall_threshold: Minimum number of pixels to identify component as room instead of hole in the wall.
    :return: rooms: list of numpy arrays containing boolean masks for each detected room
             colored_house: A colored version of the input image, where each room has a random color.
    """
    assert 0 <= corners_threshold <= 1
    # Remove noise left from door removal
    img[img < 35] = 0
    img[img > 35] = 255
    contours, _ = cv2.findContours(~img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.zeros_like(img)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > noise_removal_threshold:
            cv2.fillPoly(mask, [contour], 255)
    # Detect corners (you can play with the parameters here)
    dst = cv2.cornerHarris(img ,2,3,0.04)
    dst = cv2.dilate(dst,None)
    corners = dst > corners_threshold * dst.max()
    # Draw lines to close the rooms off by adding a line between corners on the same x or y coordinate
    # This gets some false positives.
    # You could try to disallow drawing through other existing lines for example.
    for y,row in enumerate(corners):
        x_same_y = np.argwhere(row)
        for x1, x2 in zip(x_same_y[:-1], x_same_y[1:]):

            if x2[0] - x1[0] < room_closing_max_length:
                color = 0
                cv2.line(img, (x1, y), (x2, y), color, 1)

    for x,col in enumerate(corners.T):
        y_same_x = np.argwhere(col)
        for y1, y2 in zip(y_same_x[:-1], y_same_x[1:]):
            if y2[0] - y1[0] < room_closing_max_length:
                color = 0
                cv2.line(img, (x, y1), (x, y2), color, 1)
    # Mark the outside of the house as black
    contours, _ = cv2.findContours(~img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
    biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
    mask = np.zeros_like(mask)
    cv2.fillPoly(mask, [biggest_contour], 255)
    img[mask == 0] = 255
    # Find the connected components in the house
    ret, labels = cv2.connectedComponents(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    unique = np.unique(labels)
    rooms = []
    color_list = []
    for label in unique:
        component = labels == label
        if img[component].sum() == 0 or np.count_nonzero(component) < gap_in_wall_threshold:
            color = 0
        else:
            rooms.append(component)
            color = 255
        img[component] = color
    # print("rooms-->",(len(rooms)))
    return img

def find_rooms(img_orig,img,  noise_removal_threshold=60, corners_threshold=0.1,
               room_closing_max_length=80, gap_in_wall_threshold=80):
    """

    :param img: grey scale image of rooms, already eroded and doors removed etc.
    :param noise_removal_threshold: Minimal area of blobs to be kept.
    :param corners_threshold: Threshold to allow corners. Higher removes more of the house.
    :param room_closing_max_length: Maximum line length to add to close off open doors.
    :param gap_in_wall_threshold: Minimum number of pixels to identify component as room instead of hole in the wall.
    :return: rooms: list of numpy arrays containing boolean masks for each detected room
             colored_house: A colored version of the input image, where each room has a random color.
    """
    assert 0 <= corners_threshold <= 1
    # Remove noise left from door removal
    img[img < 35] = 0
    img[img > 35] = 255
    contours, _ = cv2.findContours(~img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.zeros_like(img)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > noise_removal_threshold:
            cv2.fillPoly(mask, [contour], 255)
    # Detect corners (you can play with the parameters here)
    dst = cv2.cornerHarris(img ,2,3,0.04)
    dst = cv2.dilate(dst,None)
    corners = dst > corners_threshold * dst.max()
    # Draw lines to close the rooms off by adding a line between corners on the same x or y coordinate
    # This gets some false positives.
    # You could try to disallow drawing through other existing lines for example.
    for y,row in enumerate(corners):
        x_same_y = np.argwhere(row)
        for x1, x2 in zip(x_same_y[:-1], x_same_y[1:]):

            if x2[0] - x1[0] < room_closing_max_length:
                color = 0
                cv2.line(img, (x1, y), (x2, y), color, 1)

    for x,col in enumerate(corners.T):
        y_same_x = np.argwhere(col)
        for y1, y2 in zip(y_same_x[:-1], y_same_x[1:]):
            if y2[0] - y1[0] < room_closing_max_length:
                color = 0
                cv2.line(img, (x, y1), (x, y2), color, 1)


    # Mark the outside of the house as black
    contours, _ = cv2.findContours(~img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
    biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
    mask = np.zeros_like(mask)
    cv2.fillPoly(mask, [biggest_contour], 255)
    img[mask == 0] = 255
    ret, labels = cv2.connectedComponents(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    unique = np.unique(labels)
    rooms = []
    color_list = []
    for label in unique:
        component = labels == label
        if img[component].sum() == 0 or np.count_nonzero(component) < gap_in_wall_threshold:
            color = 0
            img[component] = color
        else:
            rooms.append(component)
            ind = (len(img_orig[component]))/2
            color = img_orig[component][math.floor(ind)]
            img[component] = color
            color_list.append(color)
    # print("colors-->",(len(color_list)))
    return img, color_list

def get_coords(colored_house,color_list):
                
    plan_color = pd.DataFrame(settings.PLAN_COLOR_DICT)
    plan_color["R"]=plan_color["R"].astype(str)
    plan_color["G"]=plan_color["G"].astype(str)
    plan_color["B"]=plan_color["B"].astype(str)
    plan_color['color'] = plan_color["R"]+","+plan_color["G"]+","+plan_color["B"]
    colorsList = []
    for y in range(0,len(colored_house)):
        for x in range(0,len(colored_house[y])):
            colors = {}
            colors["color"] = colored_house[y][x]
            colors["x_coord"] = x
            colors["y_coord"] = y
            colorsList.append(colors)
    colors = pd.DataFrame(colorsList)
    colors['color'] = colors['color'].astype(str)
    colors['color'] = colors['color'].apply(lambda x:x[1:-1].strip())
    colors['r'] = colors['color'].apply(lambda x:x.split()[0].strip())
    colors['g'] = colors['color'].apply(lambda x:x.split()[1].strip())
    colors['b'] = colors['color'].apply(lambda x:x.split()[2].strip())
    coordList = []
    for color in color_list:
        coords = {}
        coords['color'] = color
        r = str(color[0])
        g = str(color[1])
        b = str(color[2])
        x = (colors[(colors['r']==r)&(colors['g']==g)&(colors['b']==b)]['x_coord']).max()-(colors[(colors['r']==r)&(colors['g']==g)&(colors['b']==b)]['x_coord']).min()
        y = (colors[(colors['r']==r)&(colors['g']==g)&(colors['b']==b)]['y_coord']).max()-(colors[(colors['r']==r)&(colors['g']==g)&(colors['b']==b)]['y_coord']).min()
        coords['area'] = x*y
        ind = len(colors[(colors['r']==r)&(colors['g']==g)&(colors['b']==b)].index)/3
        x_coord = colors[(colors['r']==r)&(colors['g']==g)&(colors['b']==b)].iloc[0]['x_coord']
        y_coord = colors[(colors['r']==r)&(colors['g']==g)&(colors['b']==b)].iloc[math.floor(ind)]['y_coord']
        coords['x_coord'] = x_coord
        coords['y_coord'] = y_coord
        print(coords)
        if coords['area']>10:
            coordList.append(coords)
    return coordList

def get_room_tags(coordList):
    plan_color = pd.DataFrame(settings.PLAN_COLOR_DICT)
    textcoordlist = []
    for item in coordList:
        tagCoord = {}
        tagCoord['x_coord'] = item["x_coord"]
        tagCoord['y_coord'] = item["y_coord"]
        colList = []
        dstlist = []
        itemcol = np.array(item['color'])
        for i in range(0,len(plan_color['R'])):
            plancol = np.array([plan_color['R'][i],plan_color['G'][i],plan_color['B'][i]])
            dst = distance.euclidean(itemcol, plancol)
            colList.append(plancol)
            dstlist.append(dst)
        min_dst = min(dstlist)
        colindex = dstlist.index(min_dst)
        color = str(colList[colindex])[1:-1].strip()
        r = int(color.split()[0])
        g = int(color.split()[1])
        b = int(color.split()[2])
        text = plan_color[(plan_color['R'] == r)&(plan_color['G'] == g)&(plan_color['B'] == b)]['Floor tags'].iloc[0]
        tagCoord['text'] = text
        textcoordlist.append(tagCoord)
    #removing duplicate entries for one component i.e having same y_coord
    list1 = []
    new_textcoordlist = []
    for item in textcoordlist:
        if (item['y_coord'] not in list1) & (item['y_coord']+1 not in list1) & (item['y_coord']-1 not in list1):
            list1.append(item['y_coord'])
            new_textcoordlist.append(item)
    return new_textcoordlist

def write_text(colored_house,textcoordlist):
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    fontScale              = 1
    fontColor              = (0,0,0)
    for item in textcoordlist:
        cv2.putText(colored_house,item["text"].upper(), 
            (item["x_coord"],item["y_coord"]), 
            font, 
            fontScale,
            fontColor)

def convert_result(img):
    img_orig = cv2.imread(img)
    RGB_img = cv2.cvtColor(img_orig, cv2.COLOR_BGR2RGB)
    img=cv2.cvtColor(RGB_img, cv2.COLOR_RGB2GRAY)
    colored_house, color_list = find_rooms(RGB_img,img.copy())
    coordList = get_coords(RGB_img, color_list)
    textcoordlist = get_room_tags(coordList)
    img1=cv2.cvtColor(RGB_img, cv2.COLOR_RGB2GRAY)
    plan=color_white(img1)
    write_text(plan,textcoordlist)
    # im1=Image.fromarray(plan)
    # im1.save("myfile_3.jpg")
    return plan,textcoordlist
