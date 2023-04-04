# from multiprocessing import Process
import threading
import cv2
import mediapipe as mp
import sys
import tensorflow as tf
import csv
import pandas as pd
import numpy as np
import datetime
from moviepy.video.io.VideoFileClip import VideoFileClip
import os
import queue
# from tensorflow.keras.preprocessing.image import img_to_array
from EmotionDetection import emotion

DETECT_MODE = 0
SAVE_MODE = 1
DATASET_PATH = './dataset/dataset.csv'
LABEL_PATH = './dataset/labels.txt'

# returns a list of labels
def getLabels():
    labels = []
    with open(LABEL_PATH) as file:
        for line in file:
            labels.append(line.rstrip())
    return labels


def drawBoundingBox(image,hand_landmarks,height,width,mp_drawing,mphands):
    x_max = 0
    y_max = 0
    x_min = width
    y_min = height

    for handLMs in hand_landmarks:
        for lm in handLMs.landmark:
            #multiplying by the width and height since landmark coordinates are normalized by default
            x, y = int(lm.x * width), int(lm.y * height)
            x_max = max(x_max, x)
            y_max = max(y_max, y)
            x_min = min(x_min, x)
            y_min = min(y_min, y)

        mp_drawing.draw_landmarks(image, handLMs, mphands.HAND_CONNECTIONS)

    cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
    return image,x_min,y_min,x_max,y_max




#normalizes all x,y coordinates of landmarks so they become scale invariant and are relative only to the top left corner of the bounding box
#returns 1D list of normalized x,y coordinates in the form [left hand , right hand ]
def Preprocess_data(multi_hand_landmarks,multi_handedness,height,width,x_min,y_min,x_max,y_max):
    numberOfHands = []
    landmark = list()  # storing like x1,y1,x2,y2....
    # storing points in such a way that landmark list has left hand coordinates before right hand

    #getting number of hands
    for hand in multi_handedness:
        numberOfHands.append(hand.classification[0].label)


    #normalization
    for handLMs in multi_hand_landmarks:
        for lm in handLMs.landmark:
            x, y = (int(lm.x * width) - x_min)/x_max,\
                   (int(lm.y * height) - y_min)/y_max  # subtracting to get position of the points relative to the bounding box
                                        #dividing so that all the values are in range 0-1
                                        #if needed can be rounded
            landmark.append(x)
            landmark.append(y)



    preprocessed_Data = list()
    #Data should be in the form [left hand landmarks  , right hand landmarks ]
    #If only 1 hand detected then we will initialize the data of the other hand to 0
    if len(numberOfHands) == 1:
        newlist = [0 for i in range(42)]
        if numberOfHands[0] != 'Left':
            preprocessed_Data = newlist + landmark
        else:
            preprocessed_Data = landmark + newlist

    elif len(numberOfHands) == 2:
        if numberOfHands[0] != 'Left':
            #slicing x,y coordinates of landmarks so that left hand coordinates come first
            preprocessed_Data = landmark[42:] + landmark[:42]
        else:
            preprocessed_Data = landmark

    return preprocessed_Data



def writeData(data,label):
    with open(DATASET_PATH, 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        data.append(label)
        writer.writerow(data)



def WriteOnBoundingBox(image,minwidth ,maxheigth,text):
    image = cv2.putText(image, text, (minwidth,maxheigth), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0,0,255), 2, cv2.LINE_AA)
    return image





def load_Model(path):
    return tf.keras.models.load_model(path)









# word_counts = {}
sentence = []
currentWordCount = 0
translation = ''
old_label = ''
new_label = ''
def ProcessHands(path,hands,model_save_path,mp_drawing,mphands,skipFrames,queue):
    GestureModel = load_Model(model_save_path)
    cap = cv2.VideoCapture(path)
    _, frame = cap.read()
    frame = cv2.resize(frame, (640, 480))
    height, width, c = frame.shape
    count=0
    labels = getLabels()
    handGestures = []
    # allEmotions = []
    while cap.isOpened():
        success, frame = cap.read()
        #lower resolutions
        try:
            frame = cv2.resize(frame, (640, 480))
        except:
            print("Video Ended")
            break

        if not success:
            break
        cv2.waitKey(1)
        cv2.imshow('MediaPipe Hands', frame)
        frame.flags.writeable = False
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(frameRGB)
        hand_landmarks = result.multi_hand_landmarks
        text=[]
        if hand_landmarks:
            frame, x_min, y_min, x_max, y_max = drawBoundingBox(frame, hand_landmarks,
                                                                height, width, mp_drawing, mphands)
            data = Preprocess_data(result.multi_hand_landmarks, result.multi_handedness,
                                   height, width, x_min, y_min,
                                   x_max, y_max)
            if data:
                DataFrame=pd.DataFrame([data])
                output =np.argmax(GestureModel.predict(DataFrame))
                text= labels[output]
                new_label = text
                handGestures.append(text)
                frame=WriteOnBoundingBox(frame, x_min, y_max, text)
        # cv2.imshow('MediaPipe Hands', frame)
        count += skipFrames
        cap.set(1, count)
    cap.release()
    # cv2.destroyAllWindows()
    queue.put(handGestures)
    return handGestures




def makeVideoChunks(path,chunk_duration):

    video_path = path+'/test.mp4'
    os.makedirs(path+'/videoChunks', exist_ok=True)
    # create a VideoFileClip object from the video file
    video = VideoFileClip(video_path)
    # get the total duration of the video in seconds
    total_duration = video.duration
    # calculate the number of chunks needed
    num_chunks = int(total_duration // chunk_duration) + 1


    # split the video into chunks and save them in the output folder
    for i in range(num_chunks):
        start_time = i * chunk_duration
        end_time = min(total_duration, start_time + chunk_duration)
        chunk = video.subclip(start_time, end_time)
        chunk_filename = f'chunk{i + 1}.mp4'
        chunk_path = os.path.join(path+'/videoChunks', chunk_filename)
        chunk.write_videofile(chunk_path)

def startProcessing(videoPath,FolderPath):

    #Loading Models from local storage
    emotionModelPath = './facial_emotions_model.h5'
    handsModelPath = './gesture_classifier.hdf5'


    # defaultPath ='C:/Users/Wasay Rizwani/PycharmProjects/pythonProject8/VideoModels'
    # videoPath="C:/Users/Wasay Rizwani/Desktop/Video Integration/test.mp4"


    #Setting up mediapipe
    mphands = mp.solutions.hands
    hands = mphands.Hands(max_num_hands=2,model_complexity=1,
                          min_detection_confidence=0.3
                          ,min_tracking_confidence=0.3)
    mp_drawing = mp.solutions.drawing_utils
    mp_face_detection = mp.solutions.face_detection
    # Setting up the speed of the video
    skipFrames=5
    totalModels= 1

    # Setting up threads
    threads=[]
    datetime_object = datetime.datetime.now()
    que = queue.Queue()
    t1=threading.Thread(target=ProcessHands, args=(videoPath,hands,handsModelPath,mp_drawing,mphands,skipFrames,que))
    t2=threading.Thread(target=emotion.emotionAnalysis, args=(videoPath,emotionModelPath,mp_face_detection,skipFrames,que))
    t1.start()
    t2.start()
    threads.append(t1)
    threads.append(t2)

    # Joining threads
    for t in threads:
        t.join()
    while not que.empty():
        print(que.get())

    datetime_object2 = datetime.datetime.now()
    print(datetime_object2 - datetime_object)




