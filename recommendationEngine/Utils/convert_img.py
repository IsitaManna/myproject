import cv2
import numpy as np
# import matplotlib.pyplot as plt
import sklearn
from skimage.color import rgb2gray
import pandas as pd
from PIL import Image
from PIL import Image, ImageDraw, ImageFont
# from PIL import Image
import math
from scipy.spatial import distance
from recommendationEngine.Utils.find_rooms import find_rooms_test_img
from django.conf import settings

def convert_test_img(name,rootdir):
    img_orig = cv2.imread(rootdir+"{}.png".format(name))
    RGB_img = cv2.cvtColor(img_orig, cv2.COLOR_BGR2RGB)
    img = cv2.imread(rootdir+"{}.png".format(name),0)
    rooms, colored_house, color_list = find_rooms_test_img(RGB_img,img.copy(), name)
    coordList = get_coords(colored_house,color_list)
    textcoordlist = get_room_tags(coordList)
    write_text(colored_house,textcoordlist)
    return colored_house,textcoordlist

def get_coords(colored_house,color_list):
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
        x_coord = colors[(colors['r']==r)&(colors['g']==g)&(colors['b']==b)].iloc[5]['x_coord']
        y_coord = colors[(colors['r']==r)&(colors['g']==g)&(colors['b']==b)].iloc[math.floor(ind)]['y_coord']
        coords['x_coord'] = x_coord
        coords['y_coord'] = y_coord
        if coords['area']>40:
            coordList.append(coords)
    return coordList

def get_room_tags(coordList):
    plan_color = pd.DataFrame(settings.PLAN_COLOR_DICT)
    textcoordlist = []
    for item in coordList:
        tagCoord = {}
        tagCoord['x_coord'] = item["x_coord"]
        tagCoord['y_coord'] = item["y_coord"]
        tagCoord['area'] =  item["area"]
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
        text = plan_color[(plan_color['R'] == r)&(plan_color['G'] == g)&(plan_color['B'] == b)]['Floor tags']
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
    fontScale              = 0.5
    fontColor              = (255,255,255)
    for item in textcoordlist:
        cv2.putText(colored_house,item["text"].iloc[0], 
            (item["x_coord"],item["y_coord"]), 
            font, 
            fontScale,
            fontColor)
