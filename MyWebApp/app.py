import requests
from flask import Flask, render_template, request, redirect
import psycopg2


app = Flask(__name__)
conn = psycopg2.connect(database="service_db",
	user="postgres",
	password="admin123",
	host="localhost",
	port="5432"
)
cursor = conn.cursor()


@app.route('/login/', methods=['POST', 'GET'])
def login():
	if request.method == 'POST':
		if request.form.get("login"):
			username = request.form.get('username')
			password = request.form.get('password')
			cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
			records = list(cursor.fetchall())
			if records:
				return render_template('account.html', full_name=records[0][1], username=username, password=password)
		elif request.form.get("registration"):
			return redirect("/registration/")
	return render_template('login.html')


@app.route('/registration/', methods=['POST', 'GET'])
def registration():
	if request.method == 'POST':
		name = request.form.get('name', '').strip()
		login = request.form.get('login', '').strip()
		password = request.form.get('password', '').strip()
		if name and login and password:
			cursor.execute(
				'INSERT INTO service.users (full_name, login, password) VALUES(%s, %s, %s);',
				(str(name),
				str(login),
				str(password)),
			)
			conn.commit()
			return redirect('/login/')
	return render_template('registration.html')
