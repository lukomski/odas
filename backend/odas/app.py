from flask import Flask, request, render_template, jsonify, session, redirect, send_file, escape
from flask_cors import CORS, cross_origin
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from argon2 import PasswordHasher
ph = PasswordHasher()


import os

import random
import string
from datetime import datetime

app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = "uploadFiles/"
app.config['EXPIRATION_SECONDS'] = 300

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["3 per second"] # limit for all endpoints
)

import redis
db = redis.StrictRedis(host='redis', port=6379)

# temporary database
import json
DB_USERS = []

@app.route("/register")
def registerPage():
	return render_template("register.html", authorize=isLogged(request))


@app.route("/login")
def loginPage():
	success_messages = []
	if 'success_message' in request.values:
		success_messages.append(request.values.get("success_message"))
	fail_messages = []
	if 'fail_message' in request.values:
		fail_messages.append(request.values.get("fail_message"))
	return render_template("login.html", success_messages=success_messages, fail_messages=fail_messages)

@app.route("/user/<username>")
def userPage(username):
	curr_username = None
	if 'session_id' in request.cookies:
		session_id = request.cookies.get("session_id")
		curr_username = getUserKeyForSessionId(session_id)

	isOwner = curr_username == username
	directory = "/odas/" + app.config['UPLOAD_FOLDER'] + username

	pub_files = []
	if os.path.exists(directory+"/pub"):
		pub_files = os.listdir(directory+"/pub")
	priv_files = []
	if isOwner and os.path.exists(directory+"/priv"):
		priv_files = os.listdir(directory+"/priv")

	return render_template("home.html", username=username, pub_files=pub_files, priv_files=priv_files, isOwner=isOwner)

@app.route("/")
def homePage():
	if 'session_id' not in request.cookies:
		return redirect("/login")
	session_id = request.cookies.get("session_id")

	username = getUserKeyForSessionId(session_id)

	if username == None:
		return redirect("/login?"+"zaloguj się ponownie")

	directory = "/odas/" + app.config['UPLOAD_FOLDER'] + username

	pub_files = []
	if os.path.exists(directory+"/pub"):
		pub_files = os.listdir(directory+"/pub")
	priv_files = []
	if os.path.exists(directory+"/priv"):
		priv_files = os.listdir(directory+"/priv")

	return render_template("home.html", username=username, pub_files=pub_files, priv_files=priv_files, isOwner=True)

# backend

@app.route("/api/files/<user_id>/pub", methods=["GET"])
@cross_origin(supports_credentials=True)
def api_allpublicfiles(user_id):
	if request.method == "GET":

		directory = "/odas/" + app.config['UPLOAD_FOLDER'] + user_id

		pub_files = []
		if os.path.exists(directory+"/pub"):
			pub_files = os.listdir(directory+"/pub")
		return jsonify(
			success=True,
			message="poprawne pobranie dostepnych plikow publicznych dla uzytkownika " + user_id,
			files=pub_files
			)
	return jsonify(
			success=False,
			message="method " + request.method + " is forbidden for the request"
			)


# return file or json if eny error
@app.route("/api/files/<user_id>/pub/<file_name>", methods=["POST", "GET", "delete", "options"])
@cross_origin(supports_credentials=True)
def api_publicfile(user_id, file_name):
	if request.method == "GET":
		try:
			path = "/odas/" + app.config['UPLOAD_FOLDER'] + user_id + "/pub/" + file_name
			return send_file(path)
		except Exception as e:
			return jsonify(
				success=False,
				message=str(e)
				)
	elif request.method == "POST":
		if 'session_id' not in request.cookies:
			return jsonify(
				success=False,
				message="brak session_id w cookies"
				)
		session_id = request.cookies.get("session_id")
		
		username = getUserKeyForSessionId(session_id)

		if username == None:
			return jsonify(
				success=False,
				message="sesja wygasla - zaloguj sie ponownie"
				)

		# upload file
		if not 'file' in request.files:
			return jsonify(
				success=False,
				message="Brak pliku 'file' w request.data"
				)
		
		file = request.files['file']
		filename = file.filename

		if filename == "":
			return jsonify(
				success=False,
				message="pusta nazwa pliku"
				)

		directory = app.config['UPLOAD_FOLDER'] + username + "/pub"
		
		if not os.path.exists(directory):
			os.makedirs(directory)
		if os.path.exists(directory + "/" + filename):
			return jsonify(
				success=False,
				message="Plik o takiej nazwie już istnieje"
				)

		file.save(os.path.join(directory, filename))
		return jsonify(
				success=True,
				message="dodano plik " + filename
				)
	elif request.method == "DELETE":
		directory = app.config['UPLOAD_FOLDER'] + user_id + "/pub"	
		full_path = directory + "/" + file_name
		if not os.path.exists(full_path):
			return jsonify(
				success=False,
				message="Plik " + full_path + " nie istnieje"
				)
		
		os.remove(full_path)
		return jsonify(
			success=True,
			message="Poprawne usunięcie  pliku " + full_path
			)
	return jsonify(
			success=False,
			message="method " + request.method + " is forbidden for the request"
			)

@app.route("/api/files/<user_id>/priv", methods=["GET"])
@cross_origin(supports_credentials=True)
def api_allprivatefiles(user_id):
	if request.method == "GET":
		if 'session_id' not in request.cookies:
			return jsonify(
				success=False,
				message="brak session_id w cookies"
				)
		session_id = request.cookies.get("session_id")
		
		username = getUserKeyForSessionId(session_id)

		if username == None:
			return jsonify(
				success=False,
				message="sesja wygasla - zaloguj sie ponownie"
				)
		
		directory = "/odas/" + app.config['UPLOAD_FOLDER'] + username

		pub_files = []
		if os.path.exists(directory+"/priv"):
			pub_files = os.listdir(directory+"/priv")
		return jsonify(
			success=True,
			message="poprawne pobranie dostepnych plikow prywatnych dla uzytkownika " + username,
			files=pub_files
			)
	return jsonify(
			success=False,
			message="method " + request.method + " is forbidden for the request"
			)	

@app.route("/api/files/<user_id>/priv/<file_name>", methods=["POST", "GET", "delete"])
@cross_origin(supports_credentials=True)
def api_privatefile(user_id, file_name):
	if request.method == "GET":
		try:
			path = "/odas/" + app.config['UPLOAD_FOLDER'] + user_id + "/priv/" + file_name
			return send_file(path)
		except Exception as e:
			return jsonify(
				success=False,
				message=str(e)
				)
		# return jsonify(
		# 	success=True,
		# 	message="private file " + file_name + " for user " + user_id
		# 	)
	elif request.method == "POST":
		if 'session_id' not in request.cookies:
			return jsonify(
				success=False,
				message="brak session_id w cookies"
				)
		session_id = request.cookies.get("session_id")
		
		username = getUserKeyForSessionId(session_id)

		if username == None:
			return jsonify(
				success=False,
				message="sesja wygasla - zaloguj sie ponownie"
				)

		# upload file
		if not 'file' in request.files:
			return jsonify(
				success=False,
				message="Brak pliku 'file' w request.data"
				)
		
		file = request.files['file']
		filename = file.filename

		if filename == "":
			return jsonify(
				success=False,
				message="pusta nazwa pliku"
				)

		directory = app.config['UPLOAD_FOLDER'] + username + "/priv"
		
		if not os.path.exists(directory):
			os.makedirs(directory)
		if os.path.exists(directory + "/" + filename):
			return jsonify(
				success=False,
				message="Plik o takiej nazwie już istnieje"
				)

		file.save(os.path.join(directory, filename))
		return jsonify(
				success=True,
				message="dodano plik " + filename
				)
	elif request.method == "DELETE":
		directory = app.config['UPLOAD_FOLDER'] + user_id + "/priv"	
		full_path = directory + "/" + file_name
		if not os.path.exists(full_path):
			return jsonify(
				success=False,
				message="Plik " + full_path + " nie istnieje"
				)
		
		os.remove(full_path)
		return jsonify(
			success=True,
			message="Poprawne usunięcie  pliku " + full_path
			)
	return jsonify(
			success=False,
			message="method " + request.method + " is forbidden for the request"
			)

@app.route("/api/authorize", methods=["GET", "POST"])
@cross_origin(supports_credentials=True)
def api_authorize():
	# get input values
	if 'username' not in request.values:
		message = "username jest wymagany"
		return jsonify(
			success=False,
			message=message
			)
	if 'password' not in request.values:
		message = "password jest wymagane"
		return jsonify(
			success=False,
			message=message		
			)

	username = request.values.get("username")
	password = request.values.get("password")

 
	# check if corrent login and password
	if db.hget(username, "password_hash") == None :
		return jsonify(
			success=False,
			message="Niepoprawny login lub hasło użytkownika"
			)
	pass_hash = db.hget(username, "password_hash").decode()
	try:
		ph.verify(pass_hash, password)
	except Exception as e:
		# wrong password, but dont tell it straight to user
		return jsonify(
			success=False,
			message="Niepoprawny login lub hasło użytkownika"
			)
 
	# create session_id
	session_id = None
	for i in range(10):
		lettersAndDigits = string.ascii_letters + string.digits
		session_id = ''.join(random.choice(lettersAndDigits) for i in range(100))
		if getUserKeyForSessionId(session_id) == None:
			break
	if getUserKeyForSessionId(session_id) != None:
		return jsonify(
			success=False,
			message="Nieudane wygenerowanie klucza sesji - spróbuj ponownie " + session_id
			)

	# save to DB
	now = datetime.now()
	timestamp = datetime.timestamp(now)
	db.hmset(username, {"session_timestamp" : timestamp})
	db.hmset(username, {"session_id" : session_id})

	answer = jsonify(
		success=True, 
		message="Poprawne zalogowanie użytkownika " + username, 
		username=username,
		session_id=session_id
		)
	answer.set_cookie("session_id", session_id)
	return answer

@app.route("/api/adduser", methods=["GET", "POST"])
def api_addUser():
	if 'username' not in request.values:
		return jsonify(
			success=False,
			message="username jest wymagany"	
			)

	if 'password' not in request.values:
		return jsonify(
			success=False,
			message="password jest wymagany"
			)

	username = request.values.get("username")
	password = request.values.get("password")

	if db.hexists(username, "username"):
		return jsonify(
			success=False,
			message="użytkownik " + username + " istnieje"
			)

	pass_hash = ph.hash(password.encode())
	db_line = {"username" : username, "password_hash" : pass_hash}
	db.hmset(username, db_line)

	message = "Poprawne dodanie użytkownika " + username
	return jsonify(
		success=True,
		message=message
		)

@app.route("/api/getUserKeyForSessionId", methods=["GET", "POST"])
def api_getUserKeyForCurrentSession():
	if 'session_id' not in request.cookies:
		return jsonify(
			success=False,
			message="Brak session_id w cookies"
			)

	session_id = request.cookies.get("session_id")
	username = getUserKeyForSessionId(session_id)

	if username == None:
		return jsonify(
			success=False,
			message="Sesja wygasła, zaloguj się ponownie"
			)
	return jsonify(
		success=True,
		message="Poprawne znalezienie uzytkownika",
		username=username
		)
@app.route("/api/hardreset", methods=["GET", "POST"])
def api_hardReset():
	db.flushdb()
	return jsonify(
		success=True,
		message="hard reset"
		)
@app.route("/api/redis", methods=["GET", "POST"])
def api_printRedis():
	l = []
	keys=getDBKeys()
	for key in keys:
		l.append(str(db.hgetall(key)))
	return jsonify(
		success=True,
		message=l
		)
@app.route("/api/logout", methods=["GET", "POST"])
def api_logout():
	if 'session_id' not in request.cookies:
		return jsonify(
		success=False,
		message="Nie było session_id w cookies"
		)
	session_id = request.cookies.get("session_id")
	
	username = getUserKeyForSessionId(session_id)

	if username == None:
		return jsonify(
		success=False,
		message="sesja wygasła"
		)
	db.hdel(username, "session_id")
	return jsonify(
		success=True,
		message="Poprawne usunięcie sesji z aplikacji"
		)

@app.route("/api/test")
def test():
	return "elo"

# tool functions

def getDBKeys():
	keys=[]
	for key in db.scan_iter():
		keys.append(key.decode("utf-8"))
	return keys

# return None if not found
def getUserKeyForSessionId(session_id: str):
	keys = getDBKeys()
	username = None
	for key in keys:
		if not db.hexists(key, "session_id"):
			continue
		curr_session_id = db.hget(key, "session_id").decode("utf-8")
		curr_session_timestamp = db.hget(key, "session_timestamp").decode("utf-8")
		if curr_session_id == session_id:
			username = key
			break
	return username

def isLogged(request):
	if 'session_id' not in request.cookies:
		return False
	session_id = request.cookies.get("session_id")
	username = getUserKeyForSessionId(session_id)
	if username == None:
		return False
	return True

def isValidSessionId(session_id: str) -> bool:
	username = getUserKeyForSessionId(session_id)
	if username == None:
		return False
	return True

if __name__ == "__main__":
	PORT = os.environ.get('PORT')
	app.run(host="0.0.0.0", port=int(PORT), debug=True)


