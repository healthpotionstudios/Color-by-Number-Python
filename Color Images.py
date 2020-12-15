import cv2
import numpy as np
import random
import os

threshold = 0.85

#changed how many pixels are drawn at once
pixelsToShow = 100
#causes pixel fill to bloom outwards rather than scanlines. This is slower
randomizeStack = False

filename = "pic (5)"

img_rgb = cv2.imread("clean images/" + filename + ".png")
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

areas = []


def fill(data, original, sx, sy, fill_value):
    global pixelsToShow, randomizeStack
    ysize, xsize, col = data.shape
    
    stack = []
    stack.append((sx, sy))
    
    timer = pixelsToShow
    while stack:
        x = 0
        y = 0
        if randomizeStack:
            i = random.randint(0,len(stack)-1)
            x, y = stack[i]
            del stack[i]
        else:
            x, y = stack.pop()
        
        px = original[y, x]
        if px[0] > 50 and px[1] > 50 and px[2] > 50:
            
            data[y, x] = (fill_value[0] * (px[0]/255), 
                          fill_value[1] * (px[0]/255),
                          fill_value[2] * (px[0]/255))

            original[y,x] = (0,0,0)
            
            timer = timer - 1
            if (timer == 0):
                cv2.imshow("rgb", img_rgb)
                cv2.waitKey(1);
                timer = pixelsToShow
            
            if x > 0:
                stack.append((x - 1, y))
            if x < (xsize - 1):
                stack.append((x + 1, y))
            if y > 0:
                stack.append((x, y - 1))
            if y < (ysize - 1):
                stack.append((x, y + 1))
        
            
    return data


path, dirs, files = next(os.walk('clean images/numbers/' + filename + '/'))
numbersInFile = len(files) + 1
for i in range(1,numbersInFile):
    number = template = cv2.imread('clean images/numbers/' + filename + '/' + '(' + str(i) + ').png',0)
    w, h = template.shape[::-1]
    
    num = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    loc = np.where( num >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 1)
        areas.append((i, pt[0], pt[1]))
        #uncomment the 4 lines below to see it select one number from the image at a time
#    cv2.rectangle(img_rgb,(0,0),(50,40),0,-1)
#    img_rgb = cv2.putText(img_rgb, str(i), (20,25), cv2.FONT_HERSHEY_COMPLEX,  
#                   1, (0,0,255), 1, cv2.LINE_AA)
#    cv2.imshow("rgb", img_rgb)
#    cv2.waitKey();
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (255,255,255), -1)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)



random.shuffle(areas)
#print(areas)


colorfile = open('clean images/colors/' + filename +'.txt', 'r') 
lines = colorfile.readlines() 
colorArray = []
  
# Strips the newline character 
for i in range(1,len(lines)): 
    line = lines[i].strip().split(",")
    line = list(map(int, line))
    colorArray.append(line)

print(colorArray)


outlines = np.copy(img_rgb)
for i in range(len(areas)):
    print(i)
    color = colorArray[areas[i][0]-1]
    
    
    img_rgb = fill(img_rgb, outlines, areas[i][1]+5, areas[i][2]+5, color)
    




print("DONE")
cv2.imshow("rgb", img_rgb)
cv2.waitKey();
cv2.destroyAllWindows();

cv2.imwrite('output/' + filename +'.png', img_rgb)

