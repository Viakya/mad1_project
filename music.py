
# --------- IMPORTS -------------------------------------------------------------------------------------------------
import os
import datetime

from werkzeug.utils import secure_filename

from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask_sqlalchemy import SQLAlchemy


# ----------CONFIG AND SETUP ------------------------------------------------------------------------------------------

current_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(current_dir , "listen_music.sqlite3")
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()


# ---------- DATA MODEL -----------------------------------------------------------------------------------------------

class Admin(db.Model):
	__tablename__ = 'admin'
	admin_id = db.Column(db.Integer , primary_key=True)
	admin_key = db.Column(db.Integer , nullable = False)

class User(db.Model):
	__tablename__ = 'user'
	user_id = db.Column(db.Integer , autoincrement = True , primary_key = True)
	first_name = db.Column(db.String , nullable = False)
	last_name = db.Column(db.String)
	email = db.Column(db.String , nullable=False , unique = True)
	password = db.Column(db.Integer , nullable = False)

class User_Type(db.Model):
	__tablename__ = 'user_types'
	user_id = db.Column(db.Integer , db.ForeignKey("user.user_id") , primary_key = True )
	typee = db.Column(db.String , primary_key = True , nullable = False)

class Song(db.Model):
	__tablename__ = "song"
	song_id = db.Column(db.Integer , primary_key = True , autoincrement = True )
	name = db.Column(db.String , nullable = False )
	lyrics = db.Column(db.String)
	song_file = db.Column(db.String,nullable = False)
	duration = db.Column(db.String)
	artist = db.Column(db.String , nullable = False)
	upload_date = db.Column(db.String,nullable=False)
	uploaded_by = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable = False)

class Like_Song(db.Model):
	__tablename__ = "like_song"
	user_id = db.Column(db.Integer , db.ForeignKey("user.user_id") , primary_key = True)
	song_id = db.Column(db.Integer, db.ForeignKey("song.song_id") , primary_key = True)

class Album(db.Model):
	__tablename__ = "album"
	album_id = db.Column(db.Integer , primary_key = True , autoincrement = True)
	date_created = db.Column(db.String , nullable = False)
	genere = db.Column(db.String,nullable = False)
	album_by = db.Column(db.Integer, db.ForeignKey("user.user_id"),nullable = False)
	album_name = db.Column(db.String,nullable=False)

class Album_Song(db.Model):
	__tablename__ = "album_song"
	album_id = db.Column(db.Integer , db.ForeignKey("album.album_id") , primary_key = True)
	song_id = db.Column(db.Integer, db.ForeignKey("song.song_id") , primary_key = True)

class Playlist(db.Model):
	__tablename__ = "playlist"
	playlist_id = db.Column(db.Integer,primary_key=True)
	date_created = db.Column(db.String,nullable = False)
	user_id = db.Column(db.Integer, db.ForeignKey("user.user_id") , nullable = False)
	playlist_name = db.Column(db.String,nullable=False)
	
class Playlist_Song(db.Model):
	__tablename__ = "playlist_song"
	playlist_id = db.Column(db.Integer, db.ForeignKey("album.album_id") , primary_key = True)
	song_id = db.Column(db.Integer, db.ForeignKey("song.song_id"), primary_key = True)

class Black_Song(db.Model):
	__tablename__ = "black_song"
	song_id = db.Column(db.Integer,db.ForeignKey("song.song_id") , primary_key = True)

class Black_Album(db.Model):
	__tablename__ = "black_album"
	album_id = db.Column(db.Integer,db.ForeignKey("album.album_id") , primary_key = True)

class Black_Creator(db.Model):
	__tablename__ = "black_creator"
	user_id = db.Column(db.Integer,db.ForeignKey("user.user_id") , primary_key = True)


# ------------SOME FUNCTIONS USED ----------------------------------------------------------------------------------

def all_emails():
	all_emails_of = []
	peoples = User.query.all()
	for each in peoples:
		all_emails_of.append(each.email)
	return all_emails_of

def adding_a_new_user(data):
	try:
		user = User(first_name=data[0], last_name=data[1], email=data[2], password=data[3])
		db.session.add(user)
		db.session.flush()
        #adding user_type
		user_type = User_Type(user_id=user.user_id,typee="G")
		db.session.add(user_type)
		db.session.commit()
	except:
		db.session.rollback()
		return None
	else:
		return user.user_id

def verification_for_login(id_password):
	person = User.query.filter_by(user_id=int(id_password[0])).first()
	if person:
		if person.password == id_password[1]:
			return True
		else:
			return False
	return False

def check_if_creator(idd):
	cree = User_Type.query.filter_by(user_id=int(idd)).all()
	if len(cree)==2:
		return True
	else:
		return False

def make_him_creator(idd):
	try:
		data = User_Type(user_id=int(idd),typee="C")
		db.session.add(data)
		db.session.commit()
	except:
		db.session.rollback()
		return False
	else:
		return True

def save_uploaded_music(file, new_filename):
	STATIC_FOLDER = 'static'
	if not file:
		return "No file provided"
	# Make sure the filename is safe to use

	safe_filename = secure_filename(file.filename)

	# Construct the full file path for the new filename

	file_path = os.path.join(STATIC_FOLDER, new_filename)

	# Save the file with the new filename
	file.save(file_path)
	return True

def adding_song_data(data_in_list):
	try:
		a = data_in_list
		song_data = Song(name=a[0],lyrics=a[1],song_file=a[2],duration=a[3],artist=a[4],upload_date=a[5],uploaded_by=int(a[6]))
		db.session.add(song_data)
		db.session.flush()
		idd = song_data.song_id
		print(idd)
		db.session.commit()
	except:
		db.session.rollback()
		return 0
	else:
		return idd

def create_the_album(data_in_list):
	try:
		a = data_in_list
		album_data = Album(date_created=a[0],genere=a[1],album_by=int(a[2]),album_name=a[3])
		print(album_data)
		db.session.add(album_data)
		db.session.commit()
	except:
		db.session.rollback()
		return False
	else:
		return True

# ---------------------- Initial Pages for Login and Authentication --------------------------------------------------
@app.route("/")
def start():
	return render_template("start.html")

@app.route("/user_login",methods=["GET","POST"])
def userr():
	if request.method == "GET":
		return render_template("user_login.html")
	elif request.method == "POST":
		user_id = request.form["username"]
		password = request.form["password"]
		if user_id.isdigit() == False:
			return "User_id is integer"
		val = verification_for_login([user_id,password])
		if val == True:
			return redirect('/home_tem/'+str(user_id))
		else:
			return render_template("notice_wrong_login_details.html")
	else:
		pass

@app.route("/admin_login")
def admin():
	return render_template("admin_login.html")

@app.route("/register_new",methods=["GET","POST"])
def register():
	if request.method == "GET":
		return render_template("register_new.html")
	elif request.method == "POST":
		first_name = request.form["first_name"]
		last_name = request.form["last_name"]
		email = request.form["email"]
		password = request.form["password"]
		if first_name.isalpha() == False:
			return "first_name should contain letters only"
		if last_name.isalpha() == False:
			return "last_name should contain letters only"
		if "@" not in email:
			return "Enter a valid email"
		if password.isalnum() == False:
			return "password can have numbers and letters only "
		#check if email already exists and render a page telling this ..
		ee = all_emails()
		if email in ee:
			return render_template("notice_email_already_exists.html")
		else:
			register_data = [first_name , last_name , email , password]
			sign = adding_a_new_user(register_data)
			print(sign)
			if sign:
				user_name = str(sign)
				return render_template("notice_after_registration.html",username=user_name,password=password)
			else:
				return render_template("error_not_solved.html")
	else:
		return render_template("error_not_solved.html")

#-------------------------ADMIN PAGES ----------------------------------------------------------------------------


@app.route("/admin_login",methods=["GET","POST"])
def admin_login():
	admin_id = request.form["username"]
	admin_key = request.form["password"]
	if admin_id.isdigit() == False:
		return "Admin id should be a integer"
	if admin_key.isdigit() == False:
		return "Admin key should be a integer"
	admin = Admin.query.filter_by(admin_id=int(admin_id)).first()
	if admin is not None:
		if admin.admin_key == int(admin_key):
			return redirect("/admin")
		else:
			return "Wrong Key"
	else:
		return "Wrong Admin_id"

@app.route("/admin")
def admin_main():
	song = Song.query.all()
	album = Album.query.all()
	user_types = User_Type.query.filter_by(typee="C").all()
	users = User_Type.query.filter_by(typee="G").all()
	black_song = Black_Song.query.all()
	black_album = Black_Album.query.all()
	black_creator = Black_Creator.query.all()
	return render_template("admin_tem.html",black_song=black_song,black_album=black_album,black_creator=black_creator,t_song=len(song),t_album=len(album),t_creator=len(user_types),t_user=len(users))

#<a href="/admin/user" > User Table </a>
@app.route("/admin/user")
def admin_user():
	users = User.query.all()
	return render_template("admin_user.html",users=users)

#<a href="/admin/user_type" > User_Type Table </a>
@app.route("/admin/user_type")
def admin_usertype():
	user_type = User_Type.query.all()
	return render_template("admin_usertype.html",users=user_type)

#<a href="/admin/song" > Song Table </a>
@app.route("/admin/song")
def admin_song():
	song =  Song.query.all()
	return render_template("admin_song.html",songs=song)

#<a href="/admin/playlist"> Playlist Table </a>
@app.route("/admin/playlist")
def admin_playlist():
	playlist = Playlist.query.all()
	return render_template("admin_playlist.html",playlist=playlist)

@app.route("/admin/playlist_song")
def admin_playlist_song():
	playlist_song = Playlist_Song.query.all()
	return render_template("admin_playlist_song.html",playlist_song=playlist_song)

@app.route("/admin/album")
def admin_album():
	album = Album.query.all()
	return render_template("admin_album.html",album=album)

@app.route("/admin/album_song")
def admin_album_song():
	album_song = Album_Song.query.all()
	return render_template("admin_album_song.html",album_song=album_song)

@app.route("/admin/like_song")
def admin_like_song():
	like_song = Like_Song.query.all()
	return render_template("admin_like_song.html",like_song=like_song)

#<td><a href="/admin/black_song/{{ song.song_id }}"> Blacklist </a></td>
@app.route("/admin/black_song/<song_id>")
def admin_black_song(song_id):
	black_song = Black_Song.query.filter_by(song_id=song_id).first()
	if black_song is None:
		try:
			black = Black_Song(song_id=int(song_id))
			db.session.add(black)
			db.session.commit()
		except:
			db.session.rollback()
		else:
			pass
	else:
		pass
	return redirect("/admin")

#/admin/white_song/18
@app.route("/admin/white_song/<song_id>")
def white_song(song_id):
	black_song = Black_Song.query.filter_by(song_id=song_id).first()
	if black_song is None:
		pass
	else:
		try:
			db.session.delete(black_song)
			db.session.commit()
		except:
			db.session.rollback()
		else:
			pass
	return redirect("/admin")

#<td><a href="/admin/black_album/{{ k.album_id }}"> Blacklist </a></td>
@app.route("/admin/black_album/<album_id>")
def black_album(album_id):
	black_album = Black_Album.query.filter_by(album_id=album_id).first()
	if black_album is None:
		try:
			black = Black_Album(album_id=int(album_id))
			db.session.add(black)
			db.session.commit()
		except:
			db.session.rollback()
		else:
			pass
	else:
		pass
	return redirect("/admin")

@app.route("/admin/white_album/<album_id>")
def white_album(album_id):
	black_album = Black_Album.query.filter_by(album_id=album_id).first()
	if black_album is None:
		pass
	else:
		try:
			db.session.delete(black_album)
			db.session.commit()
		except:
			db.session.rollback()
		else:
			pass
	return redirect("/admin")


#<td><a href="/admin/black_creator/{{ user.user_id }}">Blacklist</a></td>

@app.route("/admin/black_creator/<user_id>")
def black_creator(user_id):
	black_creator = Black_Creator.query.filter_by(user_id=user_id).first()
	if black_creator is None:
		try:
			black = Black_Creator(user_id=int(user_id))
			db.session.add(black)
			db.session.commit()
		except:
			db.session.rollback()
		else:
			pass
	else:
		pass
	return redirect("/admin")

@app.route("/admin/white_creator/<user_id>")
def white_creator(user_id):
	black_creator = Black_Creator.query.filter_by(user_id=user_id).first()
	if black_creator is None:
		pass
	else:
		try:
			db.session.delete(black_creator)
			db.session.commit()
		except:
			db.session.rollback()
		else:
			pass
	return redirect("/admin")








# ------------------------HOME PAGES -------------------------------------------------------------------------------


@app.route("/home_tem/<naam>")
def home(naam):
	song = Song.query.all()
	album = Album.query.all()
	dd = {}
	for each in song:
		ll = []
		if each.song_id not in dd:
			like_song = Like_Song.query.filter_by(song_id=each.song_id)
			for k in like_song:
				ll.append(str(k.user_id))
			dd[str(each.song_id)] = ll
	return render_template("home_tem.html",name=naam,songs=song,albums=album,dd=dd)

@app.route("/home_tem/<naam>/<song_id>/play")
def play_music(naam,song_id):
	black_song = Black_Song.query.filter_by(song_id=song_id).first()
	if black_song is not None:
		return render_template("play_block_song.html",username=naam)
	for_lyrics = Song.query.filter_by(song_id=song_id).first()
	lyrics = for_lyrics.lyrics
	song = "/static/song_"+str(song_id)
	return render_template("playing_song.html",username=naam,song=song,lyrics=lyrics)


@app.route("/home_album_detail/<naam>/<idd>",methods=["GET"])
def home_album_detail(naam , idd):
	black_album = Black_Album.query.filter_by(album_id=idd).first()
	if black_album is not None:
		return render_template("home_album_block.html",username=naam)
	album_song = Album_Song.query.filter_by(album_id=int(idd)).all()
	album = Album.query.filter_by(album_id=int(idd)).first()
	listt = []
	for each in album_song:
		song = Song.query.filter_by(song_id=each.song_id).first()
		listt.append(song)
	return render_template("home_album_detail.html",username=naam,album=album,listt=listt)



@app.route("/home_tem/<naam>/<song_id>/like")
def like_button(naam,song_id):
	try:
		like = Like_Song.query.filter_by(song_id=int(song_id),user_id=int(naam)).first()
		if like is None:
			like = Like_Song(song_id=int(song_id),user_id=int(naam))
			db.session.add(like)
			print("if block")
		else:
			db.session.delete(like)
		db.session.commit()
		return redirect("/home_tem/"+str(naam))
		print("else block")
	except:
		db.session.rollback()
		return redirect("/home_tem/"+str(naam))
		print("except block")
	else:
		pass




#-------------------------SEARCH PAGES-------------------------------------------------------------------------------


@app.route("/search_tem/<naam>",methods=["GET","POST"])
def search(naam):
	if request.method == "GET":
		return render_template("search_tem.html",name=naam)
	elif request.method == "POST":
		what = request.form["search"]
		select_options = request.form["selectOption"]
		for_song = request.form["for_song"]
		for_album = request.form["for_album"]
		if select_options == "song":
			if for_song == "song_name":
				results = Song.query.filter(Song.name.like(f'%{what}%')).all()
				return render_template("song_on_search.html",name=naam,listt=results)
			elif for_song == "lyrics":
				results = Song.query.filter(Song.lyrics.like(f'%{what}%')).all()
				return render_template("song_on_search.html",name=naam,listt=results)
			elif for_song == "artist":
				results = Song.query.filter(Song.artist.like(f'%{what}%')).all()
				return render_template("song_on_search.html",name=naam,listt=results)
			else:
				pass
		else:
			if for_album == "album_name":
				results = Album.query.filter(Album.album_name.like(f'%{what}%')).all()
				return render_template("album_on_search.html",name=naam,albums=results)
			elif for_album == "Genre":
				results = Album.query.filter(Album.genere.like(f'%{what}%')).all()
				return render_template("album_on_search.html",name=naam,albums=results)
			else:
				pass
	else:
		pass






#-----------------------------YOU PAGES ------------------------------------------------------------------------------

@app.route("/you_tem/<naam>")
def you(naam):
	playlist = Playlist.query.filter_by(user_id=int(naam)).all()
	return render_template("you_tem.html",name=naam,playlist=playlist)

@app.route("/you_tem/create_playlist/<naam>",methods=["GET","POST"])
def new_playlist(naam):
	if request.method == "GET":
		return render_template("create_new_playlist.html",username=int(naam))
	elif request.method == "POST":
		current_date = datetime.date.today()
		date_created = str(current_date.strftime("%d-%m-%Y"))
		playlist_name = request.form["playlist_name"]
		user_id = request.form["user_id"]
		if playlist_name.isalpha() == False:
			return "playlist_name should contain letters only"
		if user_id.isdigit() == False:
			return "user_id must be integer only"
		#adding to database
		try:
			playlist = Playlist(date_created=date_created,playlist_name=playlist_name,user_id=user_id)
			db.session.add(playlist)
			db.session.commit()
			return redirect("/you_tem/"+str(naam))
		except:
			db.session.rollback()
		else:
			pass
	else:
		pass

@app.route("/you_tem/playlist_song/<naam>",methods=["GET","POST"])
def add_song_playlist(naam):
	if request.method == "GET":
		playlist = Playlist.query.filter_by(user_id=int(naam))
		song = Song.query.all()
		return render_template("add_song_to_playlist.html",username=int(naam),playlist=playlist,song=song)
	elif request.method == "POST":
		playlist_id = request.form["playlist"]
		song_id = request.form["songs"]
		try:
			q = Playlist_Song.query.filter_by(playlist_id=playlist_id,song_id=song_id).first()
			if q is None:
				playlist_song = Playlist_Song(playlist_id=playlist_id,song_id=song_id)
				db.session.add(playlist_song)
				db.session.commit()
			return redirect("/you_tem/"+str(naam))
		except:
			db.session.rollback()
		else:
			pass
	else:
		pass

@app.route("/you_tem/playlist/<naam>/<playlist_id>/update",methods=["GET","POST"])
def update_playlist(naam,playlist_id):
	if request.method == "GET":
		playlist = Playlist.query.filter_by(playlist_id=playlist_id).first()
		return render_template("update_playlist.html",username = int(naam),playlist=playlist)
	elif request.method == "POST":
		playlist = Playlist.query.filter_by(playlist_id=playlist_id).first()
		playlist.playlist_name = request.form["playlist_name"]
		try:
			db.session.add(playlist)
			db.session.commit()
			return redirect("/you_tem/"+str(naam))
		except:
			db.session.rollback()
		else:
			pass
	else:
		pass

#<a href="/you_tem/playlist/{{ name }}/{{ i['plalist'] }}/delete" type="button">Delete</a>
@app.route("/you_tem/playlist/<naam>/<playlist_id>/delete")
def delete_playlist(naam,playlist_id):
	try:
		playlist = Playlist.query.filter_by(playlist_id=playlist_id).first()
		db.session.delete(playlist)
		playlist_song = Playlist_Song.query.filter_by(playlist_id=playlist_id).all()
		for u in playlist_song:
			db.session.delete(u)
		db.session.commit()
		return redirect("/you_tem/"+str(naam))
	except:
		db.session.rollback()
	else:
		pass

@app.route("/you_tem/playlist_view/<naam>/<playlist_id>")
def view_playlist(naam,playlist_id):
	listt = []
	playlist_song = Playlist_Song.query.filter_by(playlist_id=int(playlist_id)).all()
	for each in playlist_song:
		song = Song.query.filter_by(song_id=each.song_id).first()
		listt.append(song)
	playlist = Playlist.query.filter_by(playlist_id=int(playlist_id)).first()
	return render_template("view_playlist.html",playlist=playlist,listt=listt,username=int(naam))


@app.route("/you_tem/<naam>/withdraw/<playlist_id>/<song_id>")
def withdraw_song_playlist(naam,playlist_id,song_id):
	try:
		playlist_song = Playlist_Song.query.filter_by(playlist_id=int(playlist_id),song_id=int(song_id)).first()
		db.session.delete(playlist_song)
		db.session.commit()
		return redirect("/you_tem/playlist_view/"+str(naam)+"/"+str(playlist_id))
	except:
		db.session.rollback()
	else:
		pass

@app.route("/you_tem/about_you/<naam>")
def about_you(naam):
	user = User.query.filter_by(user_id=int(naam)).first()
	return render_template("about_you.html",user=user,username=naam)

# <a href="http://127.0.0.1:5000/you_tem/liked_songs/{{ name }}"><button>Liked Songs</button></a>

@app.route("/you_tem/liked_songs/<naam>")
def liked_song(naam):
	like_song = Like_Song.query.filter_by(user_id=int(naam)).all()
	listt = []
	for i in like_song:
		song = Song.query.filter_by(song_id=i.song_id).first()
		listt.append(song)
	return render_template("liked_song.html",username=int(naam),listt = listt)







# ------------------------------CREATOR PAGES ---------------------------------------------------------------------------

@app.route("/creator_tem/<naam>")
def creator(naam):
	#check if the user is a creator or not ...
	val = check_if_creator(naam)
	if val == True:
		u_songs = Song.query.filter_by(uploaded_by=int(naam)).all()
		u_albums = Album.query.filter_by(album_by=int(naam)).all()
		dd = {}
		for each in u_songs:
			ll = []
			if each.song_id not in dd:
				like_song = Like_Song.query.filter_by(song_id=each.song_id)
				for k in like_song:
					ll.append(str(k.user_id))
					dd[str(each.song_id)] = ll
		return render_template("real_creator_tem.html",name=naam,u_songs=u_songs,u_albums=u_albums,dd=dd)
	else:
		return render_template("creator_tem.html",name=naam)

@app.route("/make_me_creator/<naam>")
def making_creator(naam):
	val = make_him_creator(naam)
	if val == True:
		return redirect('/creator_tem/'+str(naam))
	else:
		return render_template("error_not_solved.html")

@app.route("/creator_upload_song/<naam>",methods=["GET","POST"])
def song_upload(naam):
	black_creator = Black_Creator.query.filter_by(user_id=naam).first()
	if black_creator is not None:
		return render_template("creator_block.html",username=naam)
	if request.method == "GET":
		return render_template("creator_upload_song.html",username=naam)
	elif request.method == "POST":
		current_date = datetime.date.today()

		name = request.form["name"]
		lyrics = request.form["lyrics"]
		song_file = request.files["song_file"]
		duration = request.form["duration"]
		artist = request.form["artist"]
		upload_date = str(current_date.strftime("%d-%m-%Y"))
		uploaded_by = request.form["uploaded_by"]

		if name.isalpha() == False:
			return "song name should contain letters only"
		if artist.isalpha() == False:
			return "artist name should contain letters only"
		if duration.isalnum() == False:
			return "duration should contain letters and numbers only "
		get_song_id = adding_song_data([name,lyrics,name,duration,artist,upload_date,uploaded_by])
		if get_song_id != 0:
			song_name = "song_" + str(get_song_id)
			sign = save_uploaded_music(song_file,song_name)
			if sign == True:
				return render_template("notice_song_uploaded_done.html",username=uploaded_by)
			else:
				print(1)
				return render_template("error_not_solved.html")
		else:
			print(2)
	else:
		print(3)
		return render_template("error_not_solved.html")


@app.route("/creator_make_album/<naam>",methods=["GET","POST"])
def creating_new_album(naam):
	black_creator = Black_Creator.query.filter_by(user_id=naam).first()
	if black_creator is not None:
		return render_template("creator_block.html",username=naam)
	if request.method == "GET":
		return render_template("creating_new_album.html",username=naam)
	elif request.method == "POST":
		current_date = datetime.date.today()
		date_created = str(current_date.strftime("%d-%m-%Y"))
		genre = request.form["genre"]
		album_by = request.form["album_by"]
		album_name = request.form["album_name"]

		if album_name.isalpha() == False:
			return "album_name should contain letters only"
		if genre.isalpha() == False:
			return "genre should contain letters only "

		sign = create_the_album([date_created,genre,album_by,album_name])
		if sign == True:
			return render_template("notice_after_adding_album.html",username=naam)
		else:
			return render_template("error_not_solved.html")
	else:
		return render_template("error_not_solved.html")

@app.route("/creator_add_song_album/<naam>",methods=["GET","POST"])
def creator_add_song_to_album(naam):
	black_creator = Black_Creator.query.filter_by(user_id=naam).first()
	if black_creator is not None:
		return render_template("creator_block.html",username=naam)
	songs = Song.query.filter_by(uploaded_by=int(naam)).all()
	albums = Album.query.filter_by(album_by=int(naam)).all()
	if request.method  == "GET":
		return render_template("add_song_to_album.html",username = naam , albums = albums , songs = songs)
	elif request.method == "POST":
		album_id = request.form["album"]
		song_id = request.form["songs"]
		try:
			album_song = Album_Song(album_id=int(album_id),song_id=int(song_id))
			db.session.add(album_song)
			db.session.commit()
		except:
			db.session.rollback()
			pass
		else:
			return render_template("notice_album_song.html",username=naam)
	else:
		pass

@app.route("/album_detail/<naam>/<idd>",methods=["GET"])
def album_detail(naam , idd):
	album_song = Album_Song.query.filter_by(album_id=int(idd)).all()
	album = Album.query.filter_by(album_id=int(idd)).first()
	listt = []
	for each in album_song:
		song = Song.query.filter_by(song_id=each.song_id).first()
		listt.append(song)
	dd = {}
	for each in album_song:
		ll = []
		if each.song_id not in dd:
			like_song = Like_Song.query.filter_by(song_id=each.song_id)
			for k in like_song:
				ll.append(str(k.user_id))
				dd[str(each.song_id)] = ll
	return render_template("album_detail.html",username=naam,album=album,listt=listt,dd=dd)


@app.route("/creator/song/<naam>/<song_id>/delete",methods=["GET"])
def delete_song(naam,song_id):
	full_path = 'static/song_'+str(song_id)
	print(full_path)
	os.remove(full_path)
	try:
		song = Song.query.filter_by(song_id=int(song_id)).first()
		if song is not None:
			playlist_song = Playlist_Song.query.filter_by(song_id=int(song_id)).all()
			for i in playlist_song:
				db.session.delete(i)
				db.session.flush()
			album_song = Album_Song.query.filter_by(song_id=int(song_id)).all()
			for k in album_song:
				db.session.delete(k)
				db.session.flush()
			like_song = Like_Song.query.filter_by(song_id=int(song_id)).all()
			for m in like_song:
				db.session.delete(m)
				db.session.flush()
			db.session.delete(song)
			db.session.commit()
			return redirect("/creator_tem/"+str(naam))
	except:
		db.session.rollback()
	else:
		pass

@app.route("/creator/song/<naam>/<song_id>/update",methods=["GET","POST"])
def update_song(naam,song_id):
	if request.method == "GET":
		song = Song.query.filter_by(song_id=int(song_id)).first()
		return render_template("creator_update_song.html",username=naam ,song=song)
	elif request.method == "POST":
		song = Song.query.filter_by(song_id=int(song_id)).first()
		song.name = request.form["name"]
		song.lyrics = request.form["lyrics"]
		song.duration = request.form["duration"]
		song.artist = request.form["artist"]
		try:
			db.session.add(song)
			db.session.commit()
			return redirect("/creator_tem/"+str(naam))
		except:
			db.session.rollback()
		else:
			pass
	else:
		pass

@app.route("/creator/album/<naam>/<album_id>/delete",methods=["GET"])
def delete_album(naam,album_id):
	try:
		album = Album.query.filter_by(album_id=int(album_id)).first()
		if album is not None:
			album_song = Album_Song.query.filter_by(album_id=int(album_id)).all()
			for u in album_song:
				db.session.delete(u)
				db.session.flush()
			db.session.delete(album)
			db.session.commit()
			return redirect("/creator_tem/"+str(naam))
	except:
		db.session.rollback()
	else:
		pass

@app.route("/creator/album/<naam>/<album_id>/update",methods=["GET","POST"])
def update_album(naam,album_id):
	if request.method == "GET":
		album = Album.query.filter_by(album_id=int(album_id)).first()
		return render_template("update_album.html",username=naam,album=album)
	elif request.method == "POST":
		try:
			album = Album.query.filter_by(album_id=int(album_id)).first()
			album.album_name = request.form["album_name"]
			album.genere = request.form["genre"]
			db.session.add(album)
			db.session.commit()
			return redirect("/creator_tem/"+str(naam))
		except:
			db.session.rollback()
		else:
			pass

@app.route("/creator/<naam>/<album_id>/<song_id>",methods=["GET"])
def remove_song_from_album(naam,album_id,song_id):
	album_song = Album_Song.query.filter_by(album_id=int(album_id)).all()
	for ss in album_song:
		if ss.song_id == int(song_id):
			try:
				db.session.delete(ss)
				db.session.commit()
				return redirect("/album_detail/"+str(naam)+"/"+str(album_id))
			except:
				db.session.rollback()
			else:
				pass	



#----------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)

