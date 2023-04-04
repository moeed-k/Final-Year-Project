from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import shutil
from multiprocessing.connection import Client
import json
from .report import reportGen
import os
import wave

# send daemon the sessionID, path to file, userID, audio name
daemon_directory_path = "C:/Users/Wasay Rizwani/Desktop/NLP_Server/FYP/NLP"

@csrf_exempt
def process_data(request):
    audio_byte_stream = request.FILES['audio'].read()
    userID = request.FILES['id'].read().decode()
    sessionID = request.FILES['session_id'].read().decode()


    audio_clip_number = str(len(os.listdir(f'{daemon_directory_path}/analytics_data/{userID}/session{sessionID}/audio/')))
    filePath = f'{daemon_directory_path}/analytics_data/{userID}/session{sessionID}/audio/{audio_clip_number}.wav'
    metricsPath = f'{daemon_directory_path}/analytics_data/{userID}/session{sessionID}/metrics/{audio_clip_number}.json'
    snippetPath = f'{daemon_directory_path}/analytics_data/{userID}/session{sessionID}/snippets/'

    # saving file in analytics_data/userID/sessionID/audio/
    wf = wave.open(filePath, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(16000)
    wf.writeframes(audio_byte_stream)
    wf.close()

    msg = filePath+','+metricsPath+','+snippetPath

    address = ('localhost', 6000)
    conn = Client(address, authkey=b'secret password')
    print("Connecting to daemon...")
    conn.send(msg)
    print("Signal sent to daemon.")
    conn.close()

    return HttpResponse("Audio clip received.")

@csrf_exempt
def getReport(request):
    userID = request.FILES['id'].read().decode()
    sessionID = request.FILES['session_id'].read().decode()
    waitForResults = request.FILES['wait'].read().decode()


    metricsPath = f'{daemon_directory_path}/analytics_data/{userID}/session{sessionID}/metrics/'
    audioPath = f'{daemon_directory_path}/analytics_data/{userID}/session{sessionID}/audio/'

    fileCount, metrics = reportGen.getReport(audioPath,metricsPath,waitForResults)

    print("Used " + str(fileCount) + " JSONs to successfully generate a metrics report at " + metricsPath)
    return HttpResponse(json.dumps(metrics))

@csrf_exempt
def getSessionID(request):
    userID = request.FILES['id'].read().decode()
    isExist = os.path.exists(daemon_directory_path+"/analytics_data")
    if not isExist:
        os.mkdir( daemon_directory_path+"/analytics_data")

    isExist = os.path.exists(f'{daemon_directory_path}/analytics_data/{userID}')

    # if userID doesnt exist, creates the folder and initializes it with an empty session1
    if (isExist == False):
        os.mkdir(f'{daemon_directory_path}/analytics_data/{userID}')

    sessionID = len(os.listdir(f'{daemon_directory_path}/analytics_data/{userID}/'))
    sessionID += 1

    os.mkdir(f'{daemon_directory_path}/analytics_data/{userID}/session{sessionID}')
    os.mkdir(f'{daemon_directory_path}/analytics_data/{userID}/session{sessionID}/audio')
    os.mkdir(f'{daemon_directory_path}/analytics_data/{userID}/session{sessionID}/metrics')
    os.mkdir(f'{daemon_directory_path}/analytics_data/{userID}/session{sessionID}/snippets')

    data = {}
    data['session_id'] = sessionID
    return HttpResponse(json.dumps(data))
