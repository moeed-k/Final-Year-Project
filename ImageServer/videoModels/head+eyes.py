import numpy as np
import cv2
import mediapipe as mp
import math
import sys

RIGHT_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
LEFT_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
LEFT_IRIS = [469, 470, 471, 472]
RIGHT_IRIS = [474, 475, 476, 477]

def calDistance(x1,y1,x2,y2):
    distance = math.dist([x1, y1],[x2, y2])
    return distance

#We pass landmarks (470, 471), (475, 476)
def irisCentre(lm1, lm2, width, height):
    return int((lm1.x * width)), int((lm2.y * height))

def L_R_EyeTracking(frame, L_eyeWidth, R_eyeWidth, lm, rightIrisCenterX, leftIrisCenterX):
    # dividing the eyes into Three parts.
    L_div = int(L_eyeWidth/3)
    R_div = int(R_eyeWidth/3)

    L_leftPart = []
    L_centerPart = []
    L_rightPart = []
    R_leftPart = []
    R_centerPart = []
    R_rightPart = []
    

    R_x, R_y = int(lm[398].x * width), int(lm[398].y * height)
    L_x, L_y = int(lm[33].x * width), int(lm[33].y * height)

    #Left Part
    for i in range(int(1.4*L_div)):
        L_leftPart.append(L_x + i)
        if i <= L_div:
            L_centerPart.append(L_x+int(1.4*L_div)+i)
            L_rightPart.append(L_x+int(2*L_div)+i)

    #Right Part
    for i in range(int(1.4*R_div)):
        R_leftPart.append(R_x + i)
        if i <= R_div:
            R_centerPart.append(R_x+int(1.4*R_div)+i)
            R_rightPart.append(R_x+int(2*R_div)+i)


    if leftIrisCenterX in L_leftPart or rightIrisCenterX in R_leftPart:
        return 'left'
    elif rightIrisCenterX in R_rightPart or leftIrisCenterX in L_rightPart:
        return 'right'
    elif rightIrisCenterX in R_centerPart:
        return 'center'


def U_D_EyeTracking(frame, L_eyeHeight, R_eyeHeight, lm, rightIrisCenterY, leftIrisCenterY):
    # dividing the eyes into Three parts .
    L_div = int(L_eyeHeight/3)
    R_div = int(R_eyeHeight/3)
    L_topPart = []
    L_centerPart = []
    L_bottomPart = []
    R_topPart = []
    R_centerPart = []
    R_bottomPart = []
    

    R_x, R_y = int(lm[386].x * width), int(lm[386].y * height)
    L_x, L_y = int(lm[159].x * width), int(lm[159].y * height)

    #Left
    for i in range(int(1.45*L_div)):
        L_topPart.append(L_y + i)
        if i <= L_div:
            L_bottomPart.append(L_y+int((2/1.45)*L_div)+i)
        if i <= int(L_div*0.5):
            L_centerPart.append(L_y+int(1.45*L_div)+i)

    #Right
    for i in range(int(1.45*R_div)):
        R_topPart.append(R_y + i)
        if i <= R_div:
            R_bottomPart.append(R_y+int((2/1.45)*R_div)+i)
        if i <= int(R_div*0.5):
            R_centerPart.append(R_y+int(1.45*R_div)+i)

    if leftIrisCenterY in L_centerPart or rightIrisCenterY in R_centerPart:
        return 'center'
    elif leftIrisCenterY in L_bottomPart or rightIrisCenterY in R_bottomPart:
        return 'bottom'
    elif leftIrisCenterY in L_topPart or rightIrisCenterY in R_topPart:
        return 'top'

#Left and right shoulder points used to approximate coordinates of neck
def getNeckCoordinates(leftShoulder_LM, rightShoulder_LM):
    x1, y1 = int(leftShoulder_LM.x * width), int(leftShoulder_LM.y * height)
    x2 = int(rightShoulder_LM.x * width)
    x_coord = (x1+x2)/2
    y_coord = y1
    return(x_coord, y_coord)
    

#MAIN FUNCTION
mpFaceMesh = mp.solutions.face_mesh
mp_pose = mp.solutions.pose
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
_, fr = cap.read()
height, width, c = fr.shape
mp_drawing = mp.solutions.drawing_utils
count = 0
with mpFaceMesh.FaceMesh(max_num_faces=1, refine_landmarks=True, 
min_detection_confidence = 0.5, 
min_tracking_confidence = 0.5) as faceMesh,mp_pose.Pose(
    static_image_mode=True,
    model_complexity=2,
    enable_segmentation=True,
    min_detection_confidence=0.5) as pose:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = faceMesh.process(rgb)
        results2 = pose.process(rgb)
        if results.multi_face_landmarks:
            meshPoints = np.array([np.multiply([p.x, p.y], [width, height]).astype(int) for p in results.multi_face_landmarks[0].landmark])           
            iris_Lm = results.multi_face_landmarks[0].landmark
            lm = results.multi_face_landmarks[0].landmark
            lmpose = results2.pose_landmarks.landmark


            
        

        #Head Movement
            #Taking difference between the distance from left and right shoulders to the nose tip
            leftShoulderDist = calDistance(int(lmpose[12].x*width),int(lmpose[12].y*height), int((lm[0].x*width)), int((lm[0].y*height)))
            rightShoulderDist = calDistance(int(lmpose[11].x*width),int(lmpose[11].y*height), int((lm[0].x*width)), int((lm[0].y*height)))
            cv2.circle(frame, (int(lmpose[12].x*width),int(lmpose[12].y*height)), 1, (0,255,0), 1, cv2.LINE_AA)
            cv2.circle(frame, (int(lmpose[11].x*width),int(lmpose[11].y*height)), 1, (0,255,0), 1, cv2.LINE_AA)
            cv2.circle(frame, (int(lm[0].x*width),int(lm[0].y*height)), 1, (0,255,0), 1, cv2.LINE_AA)
            if abs(rightShoulderDist - leftShoulderDist) > 50:
                if leftShoulderDist > rightShoulderDist:
                    cv2.putText(frame, 'Head turned Right', (250,180), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
                else:
                    cv2.putText(frame, 'Head turned Left', (250,180), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)    
            else:
                #Eyes Movement
        #Right Eye
            #Left_Right
                x1, y1 = int(lm[466].x * width), int(lm[466].y * height)
                x2, y2 = int(lm[398].x * width), int(lm[398].y * height)
                R_eyeWidth = int(abs(x1-x2))
                #Up_Down
                x1, y1 = int(lm[386].x * width), int(lm[386].y * height)
                x2, y2 = int(lm[374].x * width), int(lm[374].y * height)

                R_eyeHeight = int(abs(y1-y2))

            #Left Eye
                #Left_Right
                x3, y3 = int(lm[33].x * width), int(lm[33].y * height)
                x4, y4 = int(lm[173].x * width), int(lm[173].y * height)
                L_eyeWidth = int(abs(x3-x4))
                #Up_Down
                x3, y3 = int(lm[159].x * width), int(lm[159].y * height)
                x4, y4 = int(lm[145].x * width), int(lm[145].y * height)
                L_eyeHeight = int(abs(y3-y4))
                rightIris_x, rightIris_y = irisCentre(lm[475], lm[476], width, height)
                leftIris_x, leftIris_y = irisCentre(lm[470], lm[471], width, height)
                posLR = ''
                posLR = L_R_EyeTracking(frame, L_eyeWidth, R_eyeWidth, lm, rightIris_x, leftIris_x)
                cv2.putText(frame, posLR, (250,180), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)

        cv2.imshow('video', frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            print(count)
            break
cap.release()
cv2.destroyAllWindows()