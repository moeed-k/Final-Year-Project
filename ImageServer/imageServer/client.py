import json

import requests
host =  'localhost:8005'
host2= 'localhost:8000'
response = requests.post(f'http://{host2}/analytics/get_sessionID/', files={'id': 'userWasayTesting'})
results = json.loads(response.text)
sessionID = results['session_id']

url=f'http://{host}/processData'
mp3_f = open('C:/Users/Wasay Rizwani/Desktop/Video Integration/test.mp4', 'rb')
files = {'videoFile': mp3_f,
         'id':'userWasayTesting',
         'session_id':sessionID}

req = requests.post(url, files=files)
print (req.status_code)
print (req.content)