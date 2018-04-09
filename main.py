from __future__ import unicode_literals
from flask import Flask, request, redirect, url_for, send_from_directory, session
from twilio.twiml.voice_response import VoiceResponse
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from pytube import YouTube
from helpers import sanitize, RepresentsInt, CorrectRequest
import urllib, json
import os
import ffmpy

SECRET_KEY = os.environ['SECRET_KEY']
app = Flask(__name__)
app.config.from_object(__name__)

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

@app.route("/", methods=['GET', 'POST'])
def main():
	body = request.values.get('Body', None)
	request_number=session.get('request_number', 0)
		
	if CorrectRequest(body):
		data = body.split(",")
		data[1] = data[1][1:]
		session['request_number'] = data[1]
		return redirect(url_for('search', song_req=data[0]))
	elif RepresentsInt(body):
		sender = request.values.get('From', None)
		return redirect(url_for('answer_sms', choice=body, sender=sender))
	else:
		session.clear()
		resp = MessagingResponse()
		resp.message("An error has occurred")
		return str(resp)
	
@app.route("/search", methods=['POST'])
def search():
	song_req = request.args['song_req']
	#search for the songs
	q = sanitize(song_req) #remove all spaces
 	url = "https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=3&q={}&key={}".format(q, API_KEY)
	response = urllib.urlopen(url)
	data = json.loads(response.read())

	#start storing lists
	session['songIds'] = []
	session['songNames'] = []

	#construct the response
	resp = MessagingResponse()
	resp.message("We found three songs for you!")

	#add to storing lists
	for i in range(3):
		title = data['items'][i]["snippet"]['title']
		author = data['items'][i]["snippet"]['channelTitle']
		resp.message("{}. Song {} by {}".format(i, title, author))

		videoId = data['items'][0]['id']['videoId']
		session['songIds'].append(videoId)
		session['songNames'].append(title)

	session['state'] = 1
	return str(resp)

@app.route("/sms", methods=['GET', 'POST'])
def answer_sms():
	choice=request.args['choice']
	choice=int(choice)
	sender=request.args['sender']
	song_req=session.get('songNames')[choice]
	request_number=session.get('request_number')
	chosen_id=session.get('songIds')[choice]

	reply = "Thanks for your message! The request to {} with the song {}".format(request_number, song_req)

	client = Client(account_sid, auth_token)

	#start the reply message
	client.api.account.messages.create(
	    to=sender,
	    from_=phone_number,
	    body=reply)

	return redirect(url_for('send_music', request_number=request_number, chosen_id=chosen_id), code=302)
	

@app.route("/send_music", methods=['POST'])
def send_music():
 	
	#extract data from API call
	videoId = choice=request.args['chosen_id']
	file_name = "{}.mp3".format(videoId)
	request_number=session.get('request_number')

	global avail_songs
	#check if song already available
	if videoId not in avail_songs:
		avail_songs.append(videoId)
		ori_file_name = "{}.mp4".format(videoId)
		

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

	session.clear()
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