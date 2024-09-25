#Estimating the head position

import numpy as np
import cv2 as cv


def head_pose(face_2d,face_3d,img_w,img_h):    
            
      face_2d = np.array(face_2d, dtype=np.float64)
      face_3d = np.array(face_3d, dtype=np.float64)

      focal_len = 1 * img_h
      cam_matrix = np.array([ [focal_len, 0, img_w / 2],[0, focal_len, img_h / 2],[0, 0, 1]])
      dist_matrix = np.zeros((4, 1), dtype=np.float64)
      success, rot_vec, trans_vec = cv.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)
      rmat, jac = cv.Rodrigues(rot_vec)
      angles, mtxR, mtxQ, Qx, Qy, Qz = cv.RQDecomp3x3(rmat) 

      x = angles[0] * 360
      y = angles[1] * 360


     # Estimating the head posiiton based on y value
      if y < -10:
           text = "Looking Left"
      elif y > 10:
           text = "Looking Right"
      elif x < -10:
           text = "Looking Down"
      else:
          text = "Forward"

      return (text)