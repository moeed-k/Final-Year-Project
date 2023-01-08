import cv2
import mediapipe as mp
import sys
import tensorflow as tf
import csv
import pandas as pd
import numpy as np


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


def drawBoundingBox(image,hand_landmarks,height,width):
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



def getUniqueWords(sentence):
    filtered_sentence = []
    for word in sentence:
        if word not in filtered_sentence:
            filtered_sentence.append(word)

    return filtered_sentence



# word_counts = {}
sentence = []
currentWordCount = 0
translation = ''
old_label = ''
new_label = ''

if __name__ == '__main__':
    model_save_path = './gesture_classifier.hdf5'
    model = tf.keras.models.load_model(model_save_path)
    mphands = mp.solutions.hands


    hands = mphands.Hands(
        model_complexity=1,
        min_detection_confidence=0.3,
        min_tracking_confidence=0.3)

    mp_drawing = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    _, frame = cap.read()
    height, width, c = frame.shape


    mode_description = "Detection Mode"
    mode = DETECT_MODE
    currLabel = -1

    labels = getLabels()

    while True:
        success, frame = cap.read()

        pressed_key = cv2.waitKey(1)

        if pressed_key == 27:
            break
        elif pressed_key == ord('s'):
            mode = SAVE_MODE
            mode_description = "Save Mode"
            cv2.destroyAllWindows()
            currLabel = -1
        elif pressed_key == ord('d'):
            mode_description = "Detection Mode"
            mode = DETECT_MODE
            currentWordCount = 0
            translation = ''
            old_label = ''
            new_label = ''
            sentence = []
            cv2.destroyAllWindows()
        elif pressed_key == ord('p'):
            mode_description = "Print mode"
            currentWordCount = 0
            old_label = ''
            new_label = ''

            sentence = getUniqueWords(sentence)
            for word in sentence:
                translation += word + ' '

            sentence = []

            cv2.destroyAllWindows()


        #flipping mirrored frame
        frame = cv2.flip(frame, 1)

        if not success:
            continue

        frame.flags.writeable = False
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(frameRGB)
        hand_landmarks = result.multi_hand_landmarks

        if (mode_description == "Print mode"):
            text = translation
            frame = cv2.putText(frame, text, (0, 100), cv2.FONT_HERSHEY_SIMPLEX,
                                1, (0, 0, 255), 2, cv2.LINE_AA)

        if (mode == SAVE_MODE):
            text = "Current Label: " + str(currLabel) + f'({chr(currLabel+65)})'
            frame = cv2.putText(frame, text, (0, 100), cv2.FONT_HERSHEY_SIMPLEX,
                                1, (0, 0, 255), 2, cv2.LINE_AA)

            # if a key between 'A' and 'Z' is pressed in saving mode, the data is stored using the pressed key as a label, with 'A' being label 0
            if pressed_key >= 65 and pressed_key <= 90:
                currLabel = pressed_key - 65


        if hand_landmarks:
            frame, x_min, y_min, x_max, y_max = drawBoundingBox(frame, hand_landmarks, height, width)
            data = Preprocess_data(result.multi_hand_landmarks, result.multi_handedness, height, width, x_min, y_min,
                                   x_max, y_max)
            if data:

                if (mode == DETECT_MODE):
                    DataFrame=pd.DataFrame([data])
                    output =np.argmax(model.predict(DataFrame))
                    text= labels[output]

                    new_label = text

                    if (old_label != new_label):
                        old_label = new_label
                        currentWordCount = 0
                    else:
                        currentWordCount += 1

                    if currentWordCount > 5:
                        sentence.append(old_label)



                    frame=WriteOnBoundingBox(frame, x_min, y_max, text)

                elif (mode == SAVE_MODE):
                    if currLabel > -1:
                        writeData(data, currLabel)

        cv2.imshow(mode_description, frame)
