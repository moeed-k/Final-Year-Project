import mediapipe as mp
import cv2
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array


def load_Model(path):
    return tf.keras.models.load_model(path)
def emotionAnalysis(path,modelPath,mp_face_detection,skipFrames,queue):
    model = load_Model(modelPath)
    expressionsDictionary={'angry':0,'fear':0,'happy':0,'neutral':0,'sad':0,'surprise':0}
    modelInput=48
    cap = cv2.VideoCapture(path)
    _, frame = cap.read()
    frame = cv2.resize(frame, (640, 480))
    frameCount = 0
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            break
        cv2.waitKey(1)
        image = cv2.resize(image, (640, 480))
        cv2.imshow('Emotion Detection', image)
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        with mp_face_detection.FaceDetection(
                min_detection_confidence=0.5) as face_detection:
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = face_detection.process(image)
            # Draw the face detection annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            copyImage = image.copy()
            if results.detections:
                # Bounding box
                BoundingBox= results.detections[0].location_data.relative_bounding_box
                x_min,y_min, width, height = BoundingBox.xmin, BoundingBox.ymin, BoundingBox.width, BoundingBox.height
                x_max, y_max = x_min+width, y_min+height
                x_min, x_max, y_min, y_max = int(x_min*image.shape[1]), int(x_max*image.shape[1]), int(y_min*image.shape[0]), int(y_max*image.shape[0])
                cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                # Bounding box
                copyImage=copyImage[y_min:y_max, x_min:x_max]
                copyImage = cv2.resize(copyImage, (modelInput, modelInput))
                copyImage=cv2.cvtColor(copyImage, cv2.COLOR_BGR2GRAY)
                x=img_to_array(copyImage)
                x=np.expand_dims(x, axis=0)
                copyImage= np.vstack([x])
                myPrediction=model.predict(copyImage)
                print(type(myPrediction))
                answers = ['angry','fear','happy','neutral','sad','surprise']
                count=0
                for i in myPrediction[0]:
                    if i>=1:
                        cv2.putText(image,answers[count]+'    '+str(i) ,(x_min,y_min+(count*50)-10),cv2.FONT_HERSHEY_SIMPLEX,0.9,(36,255,12),2)
                        expressionsDictionary[answers[count]]+=1
                    count+=1
        frameCount += skipFrames
        cap.set(1, frameCount)
    queue.put(expressionsDictionary)
    return expressionsDictionary

