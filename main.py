#main

#libraries and functions
import cv2 as cv
import mediapipe as mp
import numpy as np
import os

from landmark import detect_landmarks
from eye_position import eyesExtractor,estimate_pos
from head_position import head_pose
from warnings_emails import warning_message, send_mail

#Indices of both left and right eyes from 468 point facial landmarks
RIGHT_EYE=[ 33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161 , 246 ]
LEFT_EYE =[ 362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385,384, 398 ]

map_face_mesh=mp.solutions.face_mesh
count=0
breach=0
mail=0
camera = cv.VideoCapture(0)

with map_face_mesh.FaceMesh(min_detection_confidence =0.5, min_tracking_confidence=0.5) as face_mesh:

    while True:
        success, frame = camera.read() # getting frame from camera 
        if not success: 
            break 
        frame=cv.cvtColor(cv.flip(frame,1),cv.COLOR_BGR2RGB) #Flip the image as a selfie view
        frame.flags.writeable= False    
        result=face_mesh.process(frame) 
        frame.flags.writeable= True
        frame=cv.cvtColor(frame,cv.COLOR_RGB2BGR)
        #Used for head position
        img_h, img_w, img_c =frame.shape   
        face_3d = [] 
        face_2d = []
        if result.multi_face_landmarks:
            for face_landmarks in result.multi_face_landmarks:
                mesh_values = detect_landmarks(frame, result, False)
                r_eye = [mesh_values[p] for p in RIGHT_EYE]
                l_eye = [mesh_values[p] for p in LEFT_EYE]
                crop_r, crop_l = eyesExtractor(frame, r_eye ,l_eye)
                eye_pos_r= estimate_pos(crop_r)
                eye_pos_l = estimate_pos(crop_l)

         
                EL=eye_pos_l
                ER=eye_pos_r
                for lm in (face_landmarks.landmark):
                    x, y = int(lm.x * img_w), int(lm.y * img_h)
                    face_2d.append([x, y])
                    face_3d.append([x, y, lm.z])   
                h_pos=head_pose(face_2d,face_3d,img_w,img_h)
                Final=""

            if h_pos=="Looking Right":
                if EL==ER:
                    if ER=="CENTER":
                        Final="Looking Center"
                    elif ER=="LEFT":
                        Final="Top Right"
                else:
                     if EL=="LEFT":
                         Final="May be Center"
                     else:
                         Final="Looking Right"
            elif h_pos=="Looking Left":
                if ER==EL:
                    if ER=="CENTER":
                        Final="Looking Center"
                    elif ER=="RIGHT":
                        Final="Looking Left"
                    else:
                        Final="Looking Left"

                else:
                    if ER=="RIGHT":
                         Final="May be Center"
                    else:
                         Final="Looking Left"
            elif h_pos=="Forward":
                if EL==ER:
                     if EL=="RIGHT":
                         Final="Looking Right"
                     elif EL=="LEFT":
                         Final="Looking Left"
                     elif EL=="CENTER":
                         Final="Looking Center"
                else:
                     if EL=="CENTER" or ER=="CENTER":
                         Final="Looking Center"
                     else:
                         Final="Looking Top"
            elif h_pos=="Looking Down":
                Final="Looking Down"
            else:
                cv.putText(frame,"Blink/Closed", (20, 20), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            if Final=="Looking Center":
                cv.putText(frame,"Looking Center", (20, 20), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            elif Final=="Looking Down":
                cv.putText(frame,"Looking Down", (20, 20), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255,0), 2)
            elif Final=="May be Center":
                cv.putText(frame,"May be Center", (20, 20), cv.FONT_HERSHEY_SIMPLEX, 1, (128, 0, 128), 2)
            else:
                cv.putText(frame,"DO NOT LOOK AWAY", (20, 20), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                count=count+1

            
          
           
#three warnings followed by two mails when person is looking away

        if count==115:
            if breach==-1:
                breach=5
            elif breach>=0 and breach<3:
                breach=breach+1
                warning_message()
            elif breach==3:
                breach=breach+1
            else:
                breach=-2
            count=0
        if breach==4:
            path = r"--include the path where snpshot has to be downloaded"
            cv.imwrite(os.path.join(path , '--name of snap'),frame)
            print("Send Mail")
            mail=1
            breach=-1

        if breach==5:
            path = r"--include the path where snpshot has to be downloaded"
            cv.imwrite(os.path.join(path , ''),frame)
            print("Send Mail")
            mail=2
            breach=-2

        key = cv.waitKey(1) 
        cv.imshow('Final Output', frame)
        if key==ord('e') or key ==ord('E'): 
            break

    
    cv.destroyAllWindows()
    camera.release()
if mail==1:
    send_mail("--insert snap name",1)
if mail==2:
    send_mail("--insert snap name",1)
    send_mail("--insert snap name",2)