# Setting up the audio processing pipeline

## Installation
1. Under the NLP directory, install 'requirements1' and 'requirements2' respectively using pip. This will setup the environment for the audio processing daemon (requires python 3.8)
2. In the daemon directory, make sure you have an empty folder called 'analytics_data'. This is used to store user data. 
3. Make sure you have Django installed.
4. Go to nlp_server/analytics/views.py and set the 'daemon_directory_path'.

## Processing audio
1. Run the daemon using 'python nlp.py'
2. Start django (under nlp_server) using 'python manage.py runserver' to start django on the localhost.
3. Run client.py 

