#To detect landmarks of a given image

import cv2 as cv

def detect_landmarks(image,result, face_draw):
    image_height, image_width= image.shape[:2]
    values_mesh = [(int(point.x * image_width), int(point.y * image_height)) for point in result.multi_face_landmarks[0].landmark]
    if face_draw :
        [cv.circle(image, p, 2, (0,255,0), -1) for p in values_mesh]
    return values_mesh
