from __future__ import unicode_literals
from flask import Flask, request, redirect, url_for, send_from_directory, session, render_template
from twilio.twiml.voice_response import VoiceResponse
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from pytube import YouTube
from helpers import sanitize, RepresentsInt, CorrectRequest, db_add, search_not_have
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

@app.route("/health", methods=['GET', 'POST'])
def health():
	return render_template('index.html')

@app.route("/answer", methods=['POST'])
def answer_call():
    """Respond to incoming phone calls with a brief message."""
    # Start our TwiML response
    resp = VoiceResponse()

    # Read a message aloud to the caller
    resp.say("Thank you for calling! Please message us your request.", voice='alice')

    return str(resp)

@app.route("/", methods=['POST'])
def main():
	body = request.values.get('Body', None)
	state = session.get('state', 0)
	
	#if first request
	if CorrectRequest(body):
		session.clear()
		data = body.split(",")
		data[1] = data[1][1:]
		session['request_number'] = data[1]
		return redirect(url_for('search', song_req=data[0]))
	#if choosing song
	elif RepresentsInt(body) and state == 1:
		sender = request.values.get('From', None)
		return redirect(url_for('send_music', choice=body))
	#invalid syntax
	else:
		session.clear()
		resp = MessagingResponse()
		resp.message("An error has occurred! Please message [song info], [phone number]")
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

	reply = "We found three songs for you!\n"

	#add to storing lists
	for i in range(3):
		title = data['items'][i]["snippet"]['title']
		author = data['items'][i]["snippet"]['channelTitle']
		reply += "{}. Song {} by {}\n".format(i, title, author)
		videoId = data['items'][0]['id']['videoId']
		session['songIds'].append(videoId)
		session['songNames'].append(title)

	#construct the response
	resp = MessagingResponse()
	resp.message(reply)
	session['state'] = 1
	return str(resp)
	

@app.route("/send_music", methods=['POST'])
def send_music():
	#extract data from API call
 	choice=request.args['choice']
	choice=int(choice)
	song_req=session.get('songNames')[choice]
	videoId=session.get('songIds')[choice]
	request_number=session.get('request_number')
	file_name = "{}.mp3".format(videoId)
	
	#check if song already available
	if search_not_have(videoId):
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

		db_add(videoId)

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

	#notify that call is made
	reply = "Thanks for your message! The request to {} with the song {}".format(request_number, song_req)
	resp = MessagingResponse()
	resp.message(reply)
	return str(resp)

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
    return str(response)



if __name__ == "__main__":
    app.run(debug=True)