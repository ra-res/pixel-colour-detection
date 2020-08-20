import argparse
import cv2
import pandas as pd
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help="Image Path")
args = vars(ap.parse_args())
img_path = args['image']

#Reading image with opencv
img = cv2.imread(img_path)

clicked = False
r = g = b = xpos = ypos = 0

index=["color","color_name","hex","R","G","B"]
csv = pd.read_csv('colors.csv', names=index, header=None)

def draw_function(event, x ,y , flags, param):
    """[Calculates RGB value of pixel that you double click.]

    Args:
        x ([int]): [x coord of mouse]
        y ([int]): [y coord of mouse]
    """
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, xpos, ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)

cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)

def getColorName(R,G,B):
    """[Fetches name of colour from file]

    Args:
        R ([int]): [red value]
        G ([int]): [green value]
        B ([int]): [blue value]

    Returns:
        [str]: [colour name from file]
    """
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            cname = f'{csv.loc[i,"color_name"]} {csv.loc[i,"hex"]}'     
    return cname

while(1):
    cv2.imshow("image",img)
    #exit message
    text = "Press ESC to exit"
    cv2.putText(img, text,(50,100),2,1,(255,255,255),2,cv2.LINE_AA)

    if (clicked):
        cv2.rectangle(img,(20,20), (750,60), (b,g,r), -1)
        text = getColorName(r,g,b) + ' R='+ str(r) + ' G='+ str(g) + ' B='+ str(b)
        cv2.putText(img, text,(50,50),2,0.8,(255,255,255),2,cv2.LINE_AA)
        #For very light colours we will display text in black colour
        if(r+g+b>=600):
            cv2.putText(img, text,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)
        clicked=False
    #Break the loop when user hits 'esc' key 
    if cv2.waitKey(20) & 0xFF == 27:
        break
cv2.destroyAllWindows()


