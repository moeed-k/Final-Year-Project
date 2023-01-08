import pyaudio
import wave
import requests
import json
import time
from threading import Thread

# host = '35.84.179.188'
host = 'localhost:8000'

def postDataA(data, sessionID):
    response = requests.post(f'http://{host}/analytics/process_data/', files={'id': 'userA', 'audio': data, 'session_id':sessionID})
    print("Data Sent. Status code A: ", response.status_code)


def postDataB(data, sessionID):
    response = requests.post(f'http://{host}/analytics/process_data/', files={'id': 'userB', 'audio': data, 'session_id':sessionID})
    print("Data Sent. Status code B: ", response.status_code)




chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1
fs = 16000  # Record at 44100 samples per second
seconds = 5
loops = 3
p = pyaudio.PyAudio()  # Create an interface to PortAudio

# getting sessionIDs
print("Getting session ID....")
response = requests.post(f'http://{host}/analytics/get_sessionID/', files={'id': 'userA'})
results = json.loads(response.text)
sessionID_A = results['session_id']
print("Session ID A:", sessionID_A)


response = requests.post(f'http://{host}/analytics/get_sessionID/', files={'id': 'userB'})
results = json.loads(response.text)
sessionID_B = results['session_id']
print("Session ID B:", sessionID_B)


print('Recording Started....')

stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

frames = []  # Initialize array to store frames

# Store data in chunks for 3 seconds
for i in range(loops):
    data = b''
    for i in range(0, int(fs / chunk * seconds)):
        data += stream.read(chunk)

    senderA = Thread(target=postDataA, args=([data, sessionID_A]))
    senderB = Thread(target=postDataB, args=([data, sessionID_B]))
    senderA.start()
    senderB.start()

# Stop and close the stream
stream.stop_stream()
stream.close()
# Terminate the PortAudio interface
p.terminate()

print('Finished recording. Getting  results...')

response = requests.post(f'http://{host}/analytics/get_report/', files={'id': 'userA', 'session_id': sessionID_A,'wait':1})
print("Result Response A:", response.text)

response = requests.post(f'http://{host}/analytics/get_report/', files={'id': 'userB', 'session_id': sessionID_B,'wait':1})
print("Result Response B:", response.text)


