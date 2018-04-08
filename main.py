from __future__ import unicode_literals
from flask import Flask, request, redirect, url_for, send_from_directory
from twilio.twiml.voice_response import VoiceResponse
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from pytube import YouTube
from helpers import sanitize
import urllib, json
import os
import ffmpy

app = Flask(__name__)

account_sid = os.environ['account_sid']
auth_token = os.environ['auth_token']
phone_number = os.environ['phone_number']
home_url = os.environ['home_url']
API_KEY = os.environ['API_KEY']
avail_songs=[]

@app.route("/answer", methods=['GET', 'POST'])
def answer_call():
    """Respond to incoming phone calls with a brief message."""
    # Start our TwiML response
    resp = VoiceResponse()

    # Read a message aloud to the caller
    resp.say("Thank you for calling! Please message us your request.", voice='alice')

    return str(resp)

@app.route("/sms", methods=['GET', 'POST'])
def answer_sms():
	body = request.values.get('Body', None)
	data = body.split(",")
	data[1] = data[1][1:]
	
	request_number = data[1]
	song_req = data[0]

	reply = "Thanks for your message! The request to {} with the song {}".format(request_number, song_req)

	caller = request.values.get('From', None)
	client = Client(account_sid, auth_token)

	#start the reply message
	client.api.account.messages.create(
	    to=caller,
	    from_=phone_number,
	    body=reply)

	return redirect(url_for('send_music', request_number=request_number, song_req=song_req), code=302)
	

@app.route("/send_music", methods=['POST'])
def send_music():
 	request_number=request.args['request_number']
 	song_req = request.args['song_req']

 	#search for music
 	q = sanitize(song_req) #remove all spaces
 	url = "https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={}&key={}".format(q, API_KEY)
	response = urllib.urlopen(url)
	data = json.loads(response.read())

	#extract data from API call
	videoId = data['items'][0]['id']['videoId']
	file_name = videoId + ".mp3"

	global avail_songs
	#check if song already available
	if videoId not in avail_songs:
		avail_songs.append(videoId)
		ori_file_name = videoId + ".mp4"
		

		#download the music
		yt = YouTube('http://youtube.com/watch?v={}'.format(videoId))
	 	yt.streams.filter(only_audio=True, subtype='mp4').first().download(
	 		output_path='Music', 
	  		filename=videoId,
	 	)
		
		#convert the file
		ff = ffmpy.FFmpeg(
			inputs={'Music/{}'.format(ori_file_name): None},
			outputs={'Music/{}'.format(file_name): None}
		)
		ff.run()

		#remove the original file
		os.remove("Music/{}".format(ori_file_name))


	client = Client(account_sid, auth_token)

	# Start a phone call
	call = client.calls.create(
	    to=request_number,
	    from_=phone_number,
	    url="{}/response/{}".format(home_url, file_name)
	)
	return "success!"

@app.route('/Music/<path:path>', methods=['GET', 'POST'])
def retrieve_music(path):
    """ retrieve the music from folder """ 
    return send_from_directory('Music', path)

@app.route('/response/<path:path>', methods=['GET', 'POST'])
def construct_response(path):
    """ return an xml response to request """
    url = '{}/Music/{}'.format(home_url, str(path))

    response = VoiceResponse()
    response.say("This is a music gift just for you!", voice='man')
    response.play(url)
    print(response)
    return str(response)



if __name__ == "__main__":
    app.run(debug=True)