import cv2 as cv
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
import sys

img = cv.imread('image.jpeg',0)
img = cv.resize(img, (300, 300))
edges = cv.Canny(img,100,300)
plt.subplot(121),plt.imshow(img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
plt.show()


vertical = np.array([[0,1,0],[0,1,0],[0,1,0]])
hor = np.array([[0,0,0],[1,1,1],[0,0,0]])
for_slash = np.array([[0,0,1],[0,1,0],[1,0,0]])
back_slash = np.array([[1,0,0],[0,1,0],[0,0,1]])
point = np.array([[0,0,0],[0,1,0],[0,0,0]])

kernel_list = np.array([vertical, hor, for_slash, back_slash, point])
char_list = ["|", "-", "/", "\\", ".", " "]

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
                max_ind = 5
                for x in range(kernel_list.shape[0]):
                    conv_val = np.sum(np.multiply(mat, kernel_list[x]))
                    if(conv_val>max_val):
                        max_val = conv_val
                        max_ind = x

                convolve_vals.append(char_list[max_ind])
            else:
                continue
        convolved_chars.append(convolve_vals)
            
    return convolved_chars

conv_chars = convolve_and_place_char(edges, kernel_list)

sys.stdout = open(r"output.txt", "w+")
for x in conv_chars:
    # file1.write(''.join(x))
    print(''.join(x))

sys.stdout.close()