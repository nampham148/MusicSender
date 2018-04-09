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