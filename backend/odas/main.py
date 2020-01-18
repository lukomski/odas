from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import os # for environment

app = Flask(__name__)
CORS(app)

app.config['EXPIRATION_SECONDS'] = 300

import redis
db = redis.StrictRedis(host='redis', port=6379)

import uuid
from datetime import datetime # to add timestamp to notes

import ast # need to str -> array
import json # need to parser str -> json

from argon2 import PasswordHasher
ph = PasswordHasher()

# ENDPOINTS
#------------------------------------------

@app.route('/api/user', methods=["GET", "POST"])
@cross_origin(supports_credentials=True)
def apiUser():
	if request.method == 'GET':
		# base info about current user based on cookies
		if 'session_id' not in request.cookies:
			return jsonify(
				success=False,
				message="brak session_id w cookies"
				)
		session_hash = request.cookies.get("session_id")
		user_hash = getUserHashBySessionHash(session_hash)

		if user_hash == None:
			return jsonify(
				success=False,
				message="sesja wygasla - zaloguj sie ponownie",
				)

		username = getUsernameByUserHash(user_hash)
		if username == None:
			return jsonify(
				success=False,
				message="sesja wygasla - zaloguj sie ponownie"
				)

		return jsonify(
			success=True,
			message="zalogowany jako " + username,
			username=username,
			user_id=user_hash
			)
	elif request.method == 'POST':
		# authorize, create session
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

		user_hash = getUserHashByUsername(username)
		if user_hash == None:
			# unkown username
			return jsonify(
				success=False,
				message="Niepoprawny login lub hasło użytkownika"
				)
		user_id = 'user:' + user_hash
		# verify login and password
		if db.hget(user_id, "password_hash") == None:
			# break DB - critical
			return jsonify(
				success=False,
				message="Niepoprawny login lub hasło użytkownika"
				)
		pass_hash = db.hget(user_id, "password_hash").decode()
		try:
			ph.verify(pass_hash, password)
		except Exception as e:
			# wrong password, but dont tell it straight to user
			return jsonify(
				success=False,
				message="Niepoprawny login lub hasło użytkownika"
				)
	 
		# create session_id
		session_hash = str(uuid.uuid4()) # generate uuid
		session_id = 'session:' + session_hash

		# save to DB
		db.hmset(session_id, {
			"session_hash" : session_hash,
			"user_hash" : user_hash
			})
		db.expire(session_id, app.config['EXPIRATION_SECONDS'])

		answer = jsonify(
			success=True, 
			message="Poprawne zalogowanie użytkownika " + username, 
			username=username,
			user_id=user_hash,
			session_id=session_hash
			)
		answer.set_cookie("session_id", session_hash, max_age=app.config['EXPIRATION_SECONDS'])
		return answer
	else:
		return jsonify(
			success=False,
			message="method  " + request.method + " is forbidden for the request"
			)


@app.route('/api/users', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def apiUsers():
	if request.method == 'GET':
		# get list of users
		return jsonify(
			success=True,
			message="poprawne pobranie listy uzytkownikow",
			users=getJsonAboutUsers()
			)
	elif request.method == 'POST':
		# create new user
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
		if username in getAllUsernames():
			return jsonify(
				success=False,
				message="Uzytkownik o nazwie " + username + " juz istnieje"
				)

		password = request.values.get("password")
		user_hash = str(uuid.uuid4()) # generate uuid
		user_id = 'user:' + user_hash
		pass_hash = ph.hash(password.encode()) # make hash from password

		db.hmset(user_id, {
			"user_hash" : user_hash,
			"username" : username,
			"password_hash" : pass_hash
			})

		return jsonify(
			success=True,
			message="poprawne dodanie uzytkownika " + username
			)
	else:
		return jsonify(
			success=False,
			message="method  " + request.method + " is forbidden for the request"
			)
@app.route('/api/users/<username>/password', methods=['PUT'])
@cross_origin(supports_credentials=True)
def apiUserPassword(username):
	if request.method == 'PUT':
		# change password
		if 'session_id' not in request.cookies:
			return jsonify(
				success=False,
				message="brak session_id w cookies"
				)
		session_hash = request.cookies.get("session_id")
		c_user_hash = getUserHashBySessionHash(session_hash)

		if c_user_hash == None:
			return jsonify(
				success=False,
				message="sesja wygasla - zaloguj sie ponownie",
				)
		user_hash = getUserHashByUsername(username)
		if c_user_hash != user_hash:
			return jsonify(
				success=False,
				message="brak uprawnien do wykonania operacji",
				user_hash=user_hash,
				c_user_hash=c_user_hash
				)

		user_id = 'user:' + user_hash
		if user_id not in getAllUserKeys():
			# user not found
			return jsonify(
				success=False,
				message="brak uzytkownika",
				)

		if 'password' not in request.values:
			return jsonify(
				success=False,
				message="password jest wymagany"
				)

		password = request.values.get("password")


		if 'old_password' not in request.values:
			return jsonify(
				success=False,
				message="old_password jest wymagany"
				)
		old_password = request.values.get("old_password")

		password_hash = getPasswordHashByUserHash(user_hash)
		if password_hash == None:
			return jsonify(
				success=False,
				message="Niepoprawny uzytkownik"
				)
		try:
			ph.verify(password_hash, old_password)
		except Exception as e:
			# wrong password, but dont tell it straight to user
			return jsonify(
				success=False,
				message="Niepoprawne obecne hasło uzytkownika"
				)

		# change password
		user_id = 'user:' + user_hash
		pass_hash = ph.hash(password) # make hash from password

		db.hmset(user_id, {
			"password_hash" : pass_hash
			})

		return jsonify(
			success=True,
			message="Poprawna zmiana hasla użytkownika " + getUsernameByUserHash(user_hash)
			)
	else:
		return jsonify(
			success=False,
			message="method  " + request.method + " is forbidden for the request"
			)

@app.route('/api/notes', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def apiNotes():
	if request.method == 'GET':
		# notes filterd by userId if set
		user_hash = None
		if 'session_id' in request.cookies:
			session_hash = request.cookies.get("session_id")

			user_hash = getUserHashBySessionHash(session_hash)
		sender_username = getUsernameByUserHash(user_hash)
		if sender_username == "":
			print ("public request")
		else:
			print("requested by " + getUsernameByUserHash(user_hash))

		owner_hash = None
		username = ''
		if 'username' in request.values:
			# dont want all accesible notes but only owned by the username
			username = request.values.get('username')
			owner_hash = getUserHashByUsername(username)
			if owner_hash == None:
				# want filter by username which not exists
				print("apiNotes: " + username + " not exists in DB")
				return jsonify(
					success=True,
					message="lista notatek",
					notes=[],
					)

		print("apiNotes: " + "owner_username = " + username )
		return jsonify(
			success=True,
			message="lista notatek",
			notes=getJsonAboutNotes(owner_hash, user_hash),
			username=user_hash
			)
	elif request.method == 'POST':
		# add new note for current user
		if 'session_id' not in request.cookies:
			return jsonify(
				success=False,
				message="brak session_id w cookies"
				)
		session_hash = request.cookies.get("session_id")

		user_hash = getUserHashBySessionHash(session_hash)
			
		field = 'title'
		if field not in request.json:
			return jsonify(
				success=False,
				message=field +" jest wymagany"
				)
		title = request.json.get(field)

		field = 'message'
		if field not in request.json:
			return jsonify(
				success=False,
				message=field +" jest wymagany"
				)
		message = request.json.get(field)

		field = 'public'
		if field not in request.json:
			return jsonify(
				success=False,
				message=field +" jest wymagany"
				)
		public = request.json.get(field)

		field = 'viewers'
		if field not in request.json:
			return jsonify(
				success=False,
				message=field +" jest wymagany"
				)
		viewers = request.json.get(field)


		if public:
			viewers = []

		# filter viewers to only existings
		all_user_hashes = getAllUserHashes()
		filtered_viewers = []
		for viewer in viewers:
			print("check viewer = " + str(viewer))
			viewer_user_hash = getUserHashByUsername(viewer)
			if viewer_user_hash != None and viewer_user_hash in all_user_hashes:
				viewer_json = {
					"username": viewer
				}
				filtered_viewers.append(viewer_json)
		viewers = filtered_viewers

		print("viewers after filter = " + str(viewers))

		# all input read
		# save it to DB
		note_hash = str(uuid.uuid4()) # generate uuid

		# create timestamp od now
		now = datetime.now()
		timestamp = int(datetime.timestamp(now))
		print("timestamp = " + str(timestamp))

		note_id = 'note:' + note_hash

		db.hmset(note_id, {
			"note_hash" : note_hash,
			"title" : title,
			"message" : message,
			"public" : str(public),
			"viewers" : str(viewers),
			"owner" : str(user_hash),
			"last_edit" : timestamp
			})

		return jsonify(
			success=True,
			message="poprawne utworzenie notatki " + title,
			note_id=note_hash
			)
	else:
		return jsonify(
			success=False,
			message="method  " + request.method + " is forbidden for the request"
			)

@app.route('/api/notes/<note_hash>', methods=['GET', 'POST', 'DELETE'])
@cross_origin(supports_credentials=True)
def appNote(note_hash):
	if request.method == 'GET':
		if 'session_id' not in request.cookies:
			return jsonify(
				success=False,
				message="brak session_id w cookies"
				)
		session_hash = request.cookies.get("session_id")
		user_hash = getUserHashBySessionHash(session_hash)

		if user_hash == None:
			return jsonify(
				success=False,
				message="sesja wygasla"
			)

		has_access, dbg = checkUserAccessToNote(user_hash, note_hash)
		if not has_access:
			return jsonify(
				success=False,
				message="brak uprawnien",
				debug=dbg
			)
		note_json = getJsonAboutNote(note_hash)
		if note_json == None:
			return jsonify(
			success=False,
			message="nie znaleziono notatki " + note_hash
			)

		return jsonify(
			success=True,
			message="poprawne pobranie notatki",
			note=note_json
			)
	elif request.method == 'POST':
		# update note
		if 'session_id' not in request.cookies:
			return jsonify(
				success=False,
				message="brak session_id w cookies"
				)
		session_hash = request.cookies.get("session_id")
		user_hash = getUserHashBySessionHash(session_hash)
			
		field = 'title'
		if field not in request.json:
			return jsonify(
				success=False,
				message=field +" jest wymagany"
				)
		title = request.json.get(field)

		field = 'message'
		if field not in request.json:
			return jsonify(
				success=False,
				message=field +" jest wymagany"
				)
		message = request.json.get(field)

		field = 'public'
		if field not in request.json:
			return jsonify(
				success=False,
				message=field +" jest wymagany"
				)
		public = request.json.get(field)

		field = 'viewers'
		if field not in request.json:
			return jsonify(
				success=False,
				message=field +" jest wymagany"
				)
		viewers = request.json.get(str(field))
		print("found viewers = " + str(viewers))
		print("is public: " + str(public))

		if public:
			print("public is set - clear all viewers")
			viewers = []

		# filter viewers to only existings
		all_user_hashes = getAllUserHashes()
		filtered_viewers = []
		for viewer in viewers:
			print("check viewer = " + str(viewer))
			viewer_user_hash = getUserHashByUsername(viewer)
			if viewer_user_hash != None and viewer_user_hash in all_user_hashes:
				viewer_json = {
					"username": viewer
				}
				filtered_viewers.append(viewer_json)
		viewers = filtered_viewers

		print("viewers after filter = " + str(viewers))

		
		# all input read

		# create timestamp od now
		now = datetime.now()
		timestamp = int(datetime.timestamp(now))

		# save it to DB
		note_id = 'note:' + note_hash

		db.hmset(note_id, {
			"note_hash" : note_hash,
			"title" : title,
			"message" : message,
			"public" : str(public),
			"viewers" : str(viewers),
			"owner" : str(user_hash),
			"last_edit" : timestamp
			})

		return jsonify(
			success=True,
			message="poprawne zaktualizowanie notatki " + str(title),
			note_id=note_hash
			)
	elif request.method == 'DELETE':
		# delete note
		if 'session_id' not in request.cookies:
			return jsonify(
				success=False,
				message="brak session_id w cookies"
				)
		session_hash = request.cookies.get("session_id")
		user_hash = getUserHashBySessionHash(session_hash)

		if user_hash == None:
			return jsonify(
				success=False,
				message="sesja wygasla"
			)

		has_access, dbg = checkUserAccessToNote(user_hash, note_hash)
		if not has_access:
			return jsonify(
				success=False,
				message="brak uprawnien"
			)
		note_id = 'note:'+note_hash
		if note_id not in getAllNoteKeys():
			return jsonify(
			success=False,
			message="to nie jest hash nalezacy do notatki"
			)
		db.delete(note_id)
		return jsonify(
			success=True,
			message="poprawne usuniecie notatki"
			)
	else:
		return jsonify(
			success=False,
			message="method  " + request.method + " is forbidden for the request"
			)
# ENDPOINTS FOR DEVELOPMENT
#------------------------------------------
@app.route('/api/keys')
def keys():
	return jsonify(
		success=False,
		message=str(getDBKeys())
		)

@app.route("/api/hardreset")
def api_hardReset():
	db.flushdb()
	return jsonify(
		success=True,
		message="hard reset",
		keys=str(getDBKeys())
		)

@app.route("/api/test")
def api_test():
	print("testowy endpoint")
	return jsonify(
		success=True,
		message="test",
		users=str(getAllNoteKeys())
		)

@app.route("/api/sessions")
def api_sessions():
	return jsonify(
		success=True,
		message="sessions",
		users=str(getAllSessionKeys())
		)

@app.route("/api/redis")
def api_printRedis():
	l = []
	keys=getDBKeys()
	for key in keys:
		l.append(str(db.hgetall(key)))
	return jsonify(
		success=True,
		message=l
		)


# FUNCTIONS
#------------------------------------------

def getDBKeys():
	keys=[]
	for key in db.scan_iter():
		keys.append(key.decode("utf-8"))
	return keys

def getAllUserKeys():
	keys = []
	for key in db.scan_iter("user:*"):
		keys.append(key.decode("utf-8"))
	return keys

def getAllSessionKeys():
	keys = []
	for key in db.scan_iter("session:*"):
		keys.append(key.decode("utf-8"))
	return keys

def getAllNoteKeys():
	keys = []
	for key in db.scan_iter("note:*"):
		keys.append(key.decode("utf-8"))
	return keys
#---

def getAllUsernames():
	usernames = []
	keys = getAllUserKeys()
	field_name = "username"
	for key in keys:
		if db.hget(key, field_name) == None:
			continue
		username = db.hget(key, field_name).decode()
		usernames.append(username)
	return usernames

def getAllUserHashes():
	user_hashes = []
	keys = getAllUserKeys()
	field_name = "user_hash"
	for key in keys:
		if db.hget(key, field_name) == None:
			continue
		user_hash = db.hget(key, field_name).decode()
		user_hashes.append(user_hash)
	return user_hashes

def getJsonAboutUsers():
	users = []
	keys = getAllUserKeys()
	username_field = "username"
	user_id_field = "user_hash"
	for key in keys:
		if db.hget(key, username_field) == None:
			continue
		if db.hget(key, user_id_field) == None:
			continue
		username = db.hget(key, username_field).decode()
		user_hash = db.hget(key, user_id_field).decode()

		user_json = {
			"username" : username,
			"user_id" : user_hash
		}
		users.append(user_json)
	return users

def getJsonAboutNote(note_hash):
	note_id = 'note:' + note_hash
	if note_id not in getAllNoteKeys():
		return None

	key = note_id
	title_field = "title"
	message_field = "message"
	public_field = "public"
	viewers_field = "viewers"
	note_hash_field = "note_hash"
	owner_field = "owner"
	last_edit_field = "last_edit"
	title = db.hget(key, title_field)
	if title == None:
		return None
	title = title.decode()

	message = db.hget(key, message_field)
	if message == None:
		return None
	message = message.decode()

	public = db.hget(key, public_field)
	if public == None:
		return None
	public = public.decode()

	viewers = db.hget(key, viewers_field)
	if viewers == None:
		return None
	viewers = viewers.decode()

	note_hash = db.hget(key, note_hash_field)
	if note_hash == None:
		return None
	note_hash = note_hash.decode()

	owner_hash = db.hget(key, owner_field)
	if owner_hash == None:
		return None
	owner_hash = owner_hash.decode()

	last_edit = db.hget(key, last_edit_field)
	if last_edit == None:
		return None
	last_edit = last_edit.decode()

	note_json = {
		"title" : title,
		"message" : message,
		"public" : public == str(True),
		"viewers" : ast.literal_eval(viewers),
		"id" : note_hash,
		"owner_id" : owner_hash,
		"last_edit" : last_edit
	}
	return note_json

def getJsonAboutNotes(owner_hash, user_hash):
	notes = []
	title_field = "title"
	message_field = "message"
	public_field = "public"
	viewers_field = "viewers"
	note_hash_field = "note_hash"
	owner_field = "owner"
	last_edit_field = "last_edit"
	for key in getAllNoteKeys():

		c_owner_hash = db.hget(key, owner_field)
		if c_owner_hash == None:
			print("getJsonAboutNotes: key without owner")
			continue
		c_owner_hash = c_owner_hash.decode()

		if owner_hash != None and owner_hash != c_owner_hash:
			# filter by owner if is not None
			print("getJsonAboutNotes: omit due to fileter by owner")
			continue

		note_hash = db.hget(key, note_hash_field)
		if note_hash == None:
			print("getJsonAboutNotes: key without note_hash")
			continue
		note_hash = note_hash.decode()

		has_access, dbg = checkUserAccessToNote(user_hash, note_hash)

		if not has_access:
			# check if is vaccesible for user_hash
			print("getJsonAboutNotes: has no access")
			continue

		title = db.hget(key, title_field)
		if title == None:
			print("getJsonAboutNotes: key without title")
			continue
		title = title.decode()

		message = db.hget(key, message_field)
		if message == None:
			print("getJsonAboutNotes: key without message")
			continue
		message = message.decode()

		public = db.hget(key, public_field)
		if public == None:
			print("getJsonAboutNotes: key without public")
			continue
		public = public.decode()

		viewers = db.hget(key, viewers_field)
		if viewers == None:
			print("getJsonAboutNotes: key without viewers")
			continue
		viewers = viewers.decode()

		last_edit = db.hget(key, last_edit_field)
		if last_edit == None:
			continue
		last_edit = last_edit.decode()
		

		viewer_json = {
			"title" : title,
			"message" : message,
			"public" : public == str(True),
			"viewers" : ast.literal_eval(viewers),
			"id" : note_hash,
			"owner_id" : owner_hash,
			"last_edit" : last_edit
		}
		notes.append(viewer_json)
	return notes

def getUserHashByUsername(username):
	keys = getAllUserKeys()
	username_field = "username"
	user_id_field = "user_hash"
	for key in keys:
		if db.hget(key, username_field) == None:
			continue
		if db.hget(key, user_id_field) == None:
			continue
		c_username = db.hget(key, username_field).decode()
		if c_username != username:
			continue
		return db.hget(key, user_id_field).decode()
	return None

def getUserHashBySessionHash(session_hash):
	session_id = "session:" + session_hash
	if session_id not in getAllSessionKeys():
		# check if session exists
		return None

	user_id_field = "user_hash"
	if db.hget(session_id, user_id_field) == None:
		# break database - critical
		return None
	return db.hget(session_id, user_id_field).decode()

def getUsernameByUserHash(user_hash):
	if user_hash == None:
		return ""
	user_id = "user:" + user_hash
	if user_id not in getAllUserKeys():
		return ""

	username_field = "username"
	if db.hget(user_id, username_field) == None:
		# user not exists
		return None
	username = db.hget(user_id, username_field).decode()
	return username

def getPasswordHashByUserHash(user_hash):
	user_id = "user:" + user_hash
	if user_id not in getAllUserKeys():
		return None

	password_hash_field = "password_hash"
	if db.hget(user_id, password_hash_field) == None:
		# user not exists
		return None
	return db.hget(user_id, password_hash_field).decode()

def checkUserAccessToNote(user_hash, note_hash: str): # TODO check if is in viewers

	user_id = None
	if user_hash != None:
		user_id = 'user:' + str(user_hash)

	note_id = 'note:' + note_hash
	print("checkUserAccessToNote: user_id = " + str(user_id) + ", note_id = " + note_id)

	if user_id != None and user_id not in getAllUserKeys():
		return False, "user_id not in getAllUserKeys()"
	if note_id not in getAllNoteKeys():
		return False, "note_id not in getAllNoteKeys()"

	public = db.hget(note_id, 'public')
	if public == None:
		return False, "public == None"
	public = (public.decode() == str(True))
	if public:
		print("checkUserAccessToNote: is public " + note_hash + str(type(public))) 
		return True, "OK"


	# check if is viewer
	user_username = getUsernameByUserHash(user_hash)
	if user_username == None:
		print("checkUserAccessToNote: username = None")
		return False, "user_username == None"

	viewers_json = db.hget(note_id, 'viewers')
	if viewers_json == None:
		print("has no viewers json in DB")
		return False, "owner_hash == None"
	viewers_json_raw = viewers_json.decode()
	print("viewers_json_raw = " + str(viewers_json_raw))
	viewers_json_list = ast.literal_eval(viewers_json_raw)
	print("viewers_json_list = " + str(viewers_json_list))
	for viewer in viewers_json_list:
		v_username = viewer['username']
		if v_username == user_username:
			print("found as viewer " + user_username)
			return True, "is viewer"

	# check owner
	owner_hash = db.hget(note_id, 'owner')
	if owner_hash == None:
		return False, "owner_hash == None"
	owner_hash = owner_hash.decode()

	if owner_hash != user_hash:
		return False, str(owner_hash) + " != " + str(user_hash)
	return True, "OK"


if __name__ == "__main__":
	PORT = os.environ.get('PORT')
	app.run(host="0.0.0.0", port=int(PORT), debug=True)