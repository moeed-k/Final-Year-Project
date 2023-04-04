import numpy as np
import cv2
import mediapipe as mp
import math
import sys

LEFT_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
RIGHT_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
# RIGHT_IRIS = [469, 470]
# LEFT_IRIS = [474, 475]
LEFT_IRIS = [469, 470, 471, 472]
RIGHT_IRIS = [474, 475, 476, 477]

def calDistance(x1,y1,x2,y2):
    distance = math.dist([x1, y1],[x2, y2])
    return distance

#We pass landmarks (470, 471), (475, 476)
def irisCentre(lm1, lm2, width, height):
    return int((lm1.x * width)), int((lm2.y * height))


# def Position(ValuesList):
#     maxIndex = ValuesList.index(max(ValuesList))
#     print(maxIndex)
#     posEye = ''
#     if maxIndex == 0:
#         posEye = "Right"
#     elif maxIndex == 1:
#         posEye = "Center"
#     elif maxIndex == 2:
#         posEye = "Left"
#     else:
#         posEye = "Eye Closed"
#     return posEye

#Main
mpFaceMesh = mp.solutions.face_mesh
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
_, fr = cap.read()
height, width, c = fr.shape
mp_drawing = mp.solutions.drawing_utils
count = 0
with mpFaceMesh.FaceMesh(max_num_faces=1, refine_landmarks=True, 
min_detection_confidence = 0.5, 
min_tracking_confidence = 0.5) as faceMesh:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = faceMesh.process(rgb)
        if results.multi_face_landmarks:
            meshPoints = np.array([np.multiply([p.x, p.y], [width, height]).astype(int) for p in results.multi_face_landmarks[0].landmark])
            # cv2.polylines(frame, [meshPoints[LEFT_IRIS]], True, (0,255,0), 1, cv2.LINE_AA)
            # cv2.polylines(frame, [meshPoints[RIGHT_IRIS]], True, (0,255,0), 1, cv2.LINE_AA)

            
            iris_Lm = results.multi_face_landmarks[0].landmark
            lm = results.multi_face_landmarks[0].landmark
            x, y = int(lm[476].x * width), int(lm[476].y * height)
            leftIris_x, leftIris_y = irisCentre(iris_Lm[470], iris_Lm[471], width, height)
            rightIris_x, rightIris_y = irisCentre(iris_Lm[475], iris_Lm[476], width, height)
            # cv2.circle(frame, (leftIris_x,leftIris_y), 2, (100,100,0), -1)
            # cv2.circle(frame, (rightIris_x,rightIris_y), 2, (100,100,0), -1)
            leftEyeDist = calDistance(leftIris_x,leftIris_y, int((lm[1].x*width)), int((lm[1].y*height)))
            rightEyeDist = calDistance(rightIris_x,rightIris_y, int((lm[1].x*width)), int((lm[1].y*height)))
            cv2.putText(frame, str(leftEyeDist), (250,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
            cv2.putText(frame, str(rightEyeDist), (250,140), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
            if abs(rightEyeDist - leftEyeDist) > 8:
                if leftEyeDist > rightEyeDist:
                    cv2.putText(frame, 'Head turned Right', (250,180), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
                else:
                    cv2.putText(frame, 'Head turned Left', (250,180), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)    
            else:
                cv2.putText(frame, 'Center', (250,180), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
            #New Lines
            #New Lines
            # print(len(meshPoints))
            # for w in range(len(meshPoints)):
            #     xcoord = int(lm[w].x*width)
            #     ycoord = int(lm[w].y*height)
            #     cv2.circle(frame, (xcoord, ycoord), 2, (100,100,0), -1)
        else:
            print('No Face Detected')








        cv2.imshow('video', frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            print(count)
            break
cap.release()
cv2.destroyAllWindows()

