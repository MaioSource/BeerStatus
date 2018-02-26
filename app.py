from flask import Flask, redirect, url_for, render_template, session, request, flash
from flask import jsonify
import requests
import os
import datetime
import json
import forms
import serial
from flask_sqlalchemy import SQLAlchemy





os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
app.config['SECRET_KEY']='secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app,session_options={"autoflush": False})


class Ajustes(db.Model):
    __tablename__ = 'Ajustes'
    Id = db.Column(db.Integer, primary_key = True)
    TemperatureAlarm = db.Column(db.String(20), unique = False, nullable = False)
    RefreshRate = db.Column(db.String(20), unique=False)
    ReceiverMail = db.Column(db.String(50))
class Medicion(db.Model):
    __tablename__ = 'Medicion'
    Id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    Temperature = db.Column(db.String(20), unique = False, nullable = False)
    Time = db.Column(db.String(20), unique = False, nullable = False)

if not os.path.isfile("db.db"):
    db.create_all()



@app.route('/', methods=['GET', 'POST'])
def inicio():
	return render_template('index.html')


@app.route('/beer', methods=['POST'])
def beer():
	refresh_rate = request.form['refresh_rate']
	temperature_alarm = request.form['temperature_alarm']
	receiver_mail = request.form['receiver_mail']

	ajustes = Ajustes(RefreshRate=refresh_rate, TemperatureAlarm=temperature_alarm, ReceiverMail=receiver_mail)

	res = Ajustes.query.with_entities(Ajustes.TemperatureAlarm, Ajustes.RefreshRate).order_by(Ajustes.Id.desc()).first()

	if res:
		if res[0] == temperature_alarm and res[1] == refresh_rate:
			print "Same as last entry"
		else:
			db.session.add(ajustes)
			db.session.commit()
	else:
		db.session.add(ajustes)
		db.session.commit()
	return jsonify(refresh_rate=refresh_rate)


@app.route('/beerData', methods=['POST'])
def beerData():
	
	res = Medicion.query.with_entities(Medicion.Time, Medicion.Temperature).order_by(Medicion.Id.desc()).all()
	result = []
	for row in res:
		result.append(
			{
				"time": row[0],
				"temperature": row[1],
			})

	
	return jsonify(data=result)

if __name__ == '__main__':
	app.run(host="192.168.0.8", port=81, debug=True)

