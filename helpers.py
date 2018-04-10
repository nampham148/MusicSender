import sqlite3

def sanitize(string):
	return string.replace(" ", "%20")

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def CorrectRequest(s):
	try:
		data = s.split(",")
		s1 = data[0]
		s2 = data[1]
		return True
	except:
		return False

def db_add(videoID):
	connection = sqlite3.connect("song.db")
	cursor = connection.cursor()
	cursor.execute("INSERT INTO song(song_id) VALUES (?)", (videoID,))
	connection.commit()
	connection.close()

def search_not_have(videoID):
    print(videoID)
    connection = sqlite3.connect("song.db")
    cursor = connection.cursor()
    cursor.execute("SELECT song_id FROM song WHERE song_id = ?", (videoID,))
    data = cursor.fetchone()
    connection.close()
    return(data is None)
