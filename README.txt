   This is a simple Python command-line application that makes requests to the Gmail API. You can send and read emails through voice commands. 

Step 1:Follow the first step in link given to create credentials.json to turn on the Gmail API https://developers.google.com/gmail/api/quickstart/python 

Step 2:Install the Google Client Library by running following command
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

   Put the files main.py, gmail_api.py, send_mail, read_mail.py and credentials.json(created in first step) in a same folder named voice_project.Before executing the application, below libraries should be installed.
	
	SpeechRecognition
	gtts
	pygame
	pyaudio
	mutagen
	email
	base64
	apiclient

   After installing, navigate to folder 'voice_project' and run 'python main.py' in terminal.   
	