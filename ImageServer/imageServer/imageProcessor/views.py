from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
from .videoModels.Gestures import main as VideoProcessor
import json
import datetime
# Create your views here.
@csrf_exempt
def index (request):
    return HttpResponse("hello")
def coundGoodAndBadGestures(gestureResults):
    goodGestures=['thumbs_up','thumbs_down','ok','peace','rock','call_me','fist','palm','palm_moved','fingers_spread','double_tap']
    badGestures=[]
    goodGesturesCount=0
    badGesturesCount=0
    for gesture in gestureResults:
        if gesture['gesture']in goodGestures:
            goodGestures+=1
        else:
            badGesturesCount+=1
    return goodGestures,badGestures

@csrf_exempt
def processData(request):
    print(request.FILES)
    datetime_object = datetime.datetime.now()
    video_byte_stream = request.FILES['videoFile'].read()
    userID = request.FILES['id'].read().decode()
    sessionID = request.FILES['session_id'].read().decode()
    userFolderPath="./VideoProcessingResults/"+userID
    sessionFolderPath=userFolderPath+'/'+sessionID

    print("userID is " ,userID)
    print("SesssionID is " ,sessionID)
    if not os.path.isdir('VideoProcessingResults'):
        os.mkdir('VideoProcessingResults')
    if not os.path.isdir(userFolderPath):
        os.mkdir(userFolderPath)
    if not os.path.isdir(sessionFolderPath):
        os.mkdir(sessionFolderPath)
    numberOfClips=len(os.listdir(sessionFolderPath))
    if not os.path.isdir(sessionFolderPath+'/clip'+str(numberOfClips)):
        os.mkdir(sessionFolderPath+'/clip'+str(numberOfClips))
    userClipFolderPath = sessionFolderPath + '/clip' + str(numberOfClips) + '/'

    FILE_OUTPUT = 'video.mp4'
    if os.path.isfile(FILE_OUTPUT):
        os.remove(FILE_OUTPUT)
    out_file = open(userClipFolderPath+FILE_OUTPUT, "wb")
    out_file.write(video_byte_stream)
    out_file.close()
    handsResult,emotionResults,headDirections =VideoProcessor.startProcessing(userClipFolderPath+FILE_OUTPUT
                                                                              ,userClipFolderPath,userID,sessionID)

    results={
        'hands':handsResult,
        'emotion':emotionResults,
        'head':headDirections
    }
    open(userClipFolderPath+'results.json', 'w').write(json.dumps(results))
    datetime_object2 = datetime.datetime.now()
    print(datetime_object2 - datetime_object)
    return HttpResponse("Results are saved in "+userClipFolderPath)