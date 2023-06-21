from flask import Flask, render_template, request, redirect, session, url_for
from sqlite3 import *
from random import randrange
import pickle

app = Flask(__name__)
app.secret_key = "heartapp"


@app.route("/home")
def home():
	if 'username' in session:
		return render_template("home.html", name = session['username'])
	else:
		return redirect(url_for('signup'))

@app.route("/")
def landing():
	return render_template("landing.html")

@app.route("/find")
def find():
	if 'username' in session:
		return render_template("find.html", name = session['username'])
	else:
		return redirect(url_for('home'))

@app.route("/check", methods = ["POST"])
def check():
	if request.method == "POST":
		if 'username' in session:
			name = session['username']
		age = float(request.form["age"])
		r1 = request.form["r1"]
		if r1 == "1":
			cp = 1
		elif r1 == "2":
			cp = 2	
		elif r1 == "3":
			cp = 3
		else:
			cp = 4
		BP = float(request.form["BP"])
		CH = float(request.form["CH"])
		maxhr = float(request.form["maxhr"])
		STD = float(request.form["STD"])
		fluro = float(request.form["fluro"])
		Th = float(request.form["Th"])
		d = [[age, cp, BP, CH, maxhr, STD, fluro, Th]]	
		with open("heartdiseaseprediction.model", "rb") as f:
			model = pickle.load(f)	# study the model
		res = model.predict(d)
		res=res[0]+" of heart disease has been detected"
		return render_template("find.html", msg = res, name = session['username'])	
	else:
		return render_template("home.html")

@app.route("/signup", methods = ["GET", "POST"])
def signup():
	if request.method == "POST":
		pm = request.form["pm"]
		un = request.form["un"]
		con = None
		try:
			con = connect("monicaheart.db")
			cursor = con.cursor()
			sql = "insert into user values('%s', '%s')"
			con.execute(sql % (un, pm))
			con.commit()
			return render_template("login.html", msg = "Password has been set")
		except Exception as e:
			con.rollback()
			return render_template("signup.html", msg = "User already exists" + str(e))
	else:
		return render_template("signup.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
	if request.method == "POST":
		un = request.form["un"]
		pw = request.form["pw"]
		con = None
		try:
			con = connect("monicaheart.db")
			cursor = con.cursor()
			sql = "select * from user where username = '%s' and password = '%s'"
			cursor.execute(sql % (un,pw))
			data = cursor.fetchall()
			if len(data) == 0:
				return render_template("login.html", msg = "invalid login")
			else:	
				session['username'] = un
				return redirect( url_for('home'))
		
		except Exception as e:
			msg = "Issue " + str(e)
			return render_template("login.html", msg = msg)
	else:
		return render_template("login.html")
		

@app.route("/logout", methods = ["POST"])
def logout():
	session.clear()	
	return redirect(url_for("login"))

if __name__ == "__main__":
	app.run(debug = True)
