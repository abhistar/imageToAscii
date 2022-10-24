import cv2 as cv
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
import sys
import turtle

IMAGE_LOC = "diya.jpeg"
IMG_SIZE = 350
CANNY_PARA_1 = 100
CANNY_PARA_2 = 300
FONT_SIZE = 8
SCREEN_BG = "black"
PEN_COLOR = "white"
FONT = "Courier"
FONT_STYLE = "normal"

img = cv.imread(IMAGE_LOC,0)
img = cv.resize(img, (IMG_SIZE, IMG_SIZE))
edges = cv.Canny(img, CANNY_PARA_1, CANNY_PARA_2)

vertical = np.array([[[1,0,0],[1,0,0],[1,0,0]], [[0,1,0],[0,1,0],[0,1,0]], [[0,0,1],[0,0,1],[0,0,1]]])
hor = np.array([[[1,1,1],[0,0,0],[0,0,0]], [[0,0,0],[1,1,1],[0,0,0]], [[0,0,0],[0,0,0],[1,1,1]]])
for_slash = np.array([[[0,1,0],[1,0,0],[0,0,0]], [[0,0,1],[0,1,0],[1,0,0]], [[0,0,0],[0,0,1],[0,1,0]]])
back_slash = np.array([[[0,1,0],[0,0,1],[0,0,0]], [[1,0,0],[0,1,0],[0,0,1]], [[0,0,0],[1,0,0],[0,1,0]]])
plus = np.array([[[1,1,1],[1,0,0],[1,0,0]],[[0,1,0],[1,1,1],[0,1,0]],[[0,0,1],[0,0,1],[1,1,1]]])
cross = np.array([[[1,1,0],[1,1,0],[0,0,1]],[[1,0,1],[0,1,0],[1,0,1]],[[1,0,0],[0,1,1],[0,1,1]]])

kernel_list = np.array([vertical, hor, for_slash, back_slash, plus, cross])
char_list = ["|", "-", "/", "\\", "+", "x", " "]

def convolve_and_place_char(img: np.array, kernel_list: np.array) -> list:
    k = kernel_list[0].shape[0]
    k_ = 3
    
    convolved_chars = [] 
    
    for i in range(0,img.shape[0],k_):
        convolve_vals = []
        for j in range(0,img.shape[0],k_):
            if((img.shape[0]-i)>=k and (img.shape[0]-j)>=k):
                mat = img[i:i+k, j:j+k]

                max_val = 0
                max_ind = len(char_list)-1
                for x in range(kernel_list.shape[0]):
                    for y in range(3):
                        conv_val = np.sum(np.multiply(mat, kernel_list[x,y]))
                    if(conv_val>max_val):
                        max_val = conv_val
                        max_ind = x

                convolve_vals.append(char_list[max_ind])
            else:
                continue
        convolved_chars.append(convolve_vals)
            
    return convolved_chars

conv_chars = convolve_and_place_char(edges, kernel_list)

method = sys.argv[1]

if method=="turtle":
    turtle.Screen().setup(width = 1.0, height = 1.0)
    turtle.Screen().bgcolor("black")
    turtle.pencolor("white")
    turtle.penup()
    turtle.setpos((-1*IMG_SIZE,int(1.325*IMG_SIZE)))
    turtle.speed(1)
    for x in conv_chars:
        line = ''.join(x)
        turtle.pendown()
        turtle.write(line, font=(FONT, FONT_SIZE, FONT_STYLE))
        turtle.penup()
        turtle.goto(-1*IMG_SIZE, turtle.ycor() - FONT_SIZE)
    turtle.done()
    
elif method=="text":
    plt.subplot(121),plt.imshow(img,cmap = 'gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(edges,cmap = 'gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
    plt.show()
    sys.stdout = open("output.txt", "w+")
    for x in conv_chars:
        print(''.join(x))
    sys.stdout.close()