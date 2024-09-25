#Extracting eyes and estimating their position

#Extraction of eyes from the image

import cv2 as cv
import numpy as np

def eyesExtractor(image, right_eye_values, left_eye_values): 

    gray_img = cv.cvtColor(image, cv.COLOR_BGR2GRAY) 
    
    img_dim = gray_img.shape

    img_mask = np.zeros(img_dim, dtype=np.uint8)

    cv.fillPoly(img_mask, [np.array(right_eye_values, dtype=np.int32)], 255)
    cv.fillPoly(img_mask, [np.array(left_eye_values, dtype=np.int32)], 255)  
    
    eyes = cv.bitwise_and(gray_img, gray_img, mask=img_mask) 
    eyes[img_mask==0]=155  

    r_x_max = (max(right_eye_values, key=lambda ele: ele[0]))[0]
    r_x_min = (min(right_eye_values, key=lambda ele: ele[0]))[0]
    r_y_max = (max(right_eye_values, key=lambda ele: ele[1]))[1]
    r_y_min = (min(right_eye_values, key=lambda ele: ele[1]))[1]

    l_x_max = (max(left_eye_values, key=lambda ele: ele[0]))[0]
    l_x_min = (min(left_eye_values, key=lambda ele: ele[0]))[0]
    l_y_max = (max(left_eye_values, key=lambda ele: ele[1]))[1]
    l_y_min = (min(left_eye_values, key=lambda ele: ele[1]))[1]

    crop_right = eyes[r_y_min: r_y_max, r_x_min: r_x_max]
    crop_left = eyes[l_y_min: l_y_max, l_x_min: l_x_max]

    return crop_right, crop_left

# Counting the pixels from given image
def count_pixel(r_piece, c_piece, l_piece):

    # counting black pixel in each part  (0 represents black )
    r_part = np.sum(r_piece==0)   
    c_part = np.sum(c_piece==0)
    l_part=  np.sum(l_piece==0)

    eye_parts = [r_part, c_part,l_part]

    # Finding the part in which max black pixel is present
    max_part = eye_parts.index(max(eye_parts))
    if max_part==0:
        pos="RIGHT"
    elif max_part==2:
        pos= "LEFT"
    elif max_part==1:
        pos="CENTER"
    else:
        pos="CLOSED"

    return pos


# Estimating the position of eye
def estimate_pos(crop_eye):
    
    h, w =crop_eye.shape 
    gauss_blur = cv.GaussianBlur(crop_eye, (9,9),0)
    med_blur = cv.medianBlur(gauss_blur, 3)   
    ret, thresh_eye = cv.threshold(crop_eye, 130, 255, cv.THRESH_BINARY) 

    #Divide the eye with respect to width (3 equal parts)
    piece = int(w/3)

    r_piece = thresh_eye[0:h, 0:piece]
    c_piece = thresh_eye[0:h, piece: piece+piece]
    l_piece=  thresh_eye[0:h, piece+piece:w]
    
    # calling pixel counter function
    eye_pos = count_pixel(r_piece, c_piece,l_piece)

    return eye_pos
