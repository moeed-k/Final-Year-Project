import mediapipe as mp
import cv2
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array




def load_Model(path):
    return tf.keras.models.load_model(path)

mp_drawing = mp.solutions.drawing_utils
mp_face_detection = mp.solutions.face_detection
model=load_Model('./facial_emotions_model.h5')
model.summary()

cap = cv2.VideoCapture(0)
expressionsDictionary={'angry':0,'fear':0,'happy':0,'neutral':0,'sad':0,'surprise':0}
modelInput=48
with mp_face_detection.FaceDetection(
        min_detection_confidence=0.5) as face_detection:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = face_detection.process(image)
        # Draw the face detection annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        copyImage = image.copy()
        if not results.detections:
            continue
        if results.detections:
            BoundingBox= results.detections[0].location_data.relative_bounding_box
            x_min,y_min, width, height = BoundingBox.xmin, BoundingBox.ymin, BoundingBox.width, BoundingBox.height
            x_max, y_max = x_min+width, y_min+height
            x_min, x_max, y_min, y_max = int(x_min*image.shape[1]), int(x_max*image.shape[1]), int(y_min*image.shape[0]), int(y_max*image.shape[0])
            cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            copyImage=copyImage[y_min:y_max, x_min:x_max]
            copyImage = cv2.resize(copyImage, (modelInput, modelInput))
            copyImage=cv2.cvtColor(copyImage, cv2.COLOR_BGR2GRAY)
            x=img_to_array(copyImage)
            x=np.expand_dims(x, axis=0)
            copyImage= np.vstack([x])
            myPrediction=model.predict(copyImage)

            print(type(myPrediction))
            index=np.argmax(myPrediction)
            answers = ['angry','fear','happy','neutral','sad','surprise']
            count=0
            for i in myPrediction[0]:
                print(i)
                if i>=1:
                    cv2.putText(image,answers[count]+'    '+str(i) ,(x_min,y_min+(count*50)-10),cv2.FONT_HERSHEY_SIMPLEX,0.9,(36,255,12),2)
                    expressionsDictionary[answers[count]]+=1
                count+=1


        #cv2.imshow('copyImage', copyImage)

        cv2.imshow('MediaPipe Face Detection', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
    cap.release()
    import matplotlib.pyplot as plt


    plt.bar(list(expressionsDictionary.keys()), expressionsDictionary.values(), color='g')
    plt.show()


