import sqlite3
import serial
import time
import datetime
from marrow.mailer import Mailer, Message
import logging 

logging.basicConfig(level=logging.INFO)

mailer = Mailer(dict(
        transport = dict(
                use = 'smtp',
                host = '*.com.ar',
                username='*',
                password='*',)))
mailer.start()


RefreshRate = 30000
while True:
	conn = sqlite3.connect('db.db')
	c = conn.cursor()

	c.execute('SELECT RefreshRate, TemperatureAlarm, ReceiverMail FROM Ajustes ORDER BY Id DESC')
	rRate = c.fetchall()

	if rRate[0][0] != RefreshRate:
		RefreshRate = rRate[0][0]

	print("Refresh rate: %s" %RefreshRate)
	time.sleep(int(RefreshRate)/1000)

	arduino = serial.Serial('/dev/ttyACM0', 9600)
	rawString = arduino.readline()
	etime = datetime.datetime.now().time()
	etime=str(etime).split(".")[0]
	print("Temperature: %s" %rawString)
	print("Time: %s" %etime)


	try:
		if rawString >= float(rRate[0][1])-2:
			message = Message(author="*", to=str(rRate[0][2]))
			message.subject = "Alerta de temperatura!"

			msgBody = "Hola!\n\n\tSe esta por llegar a la temperatura deseada.\n\tLa temperatura actual es: %s\n\t\t\tSaludos!" %rawString
			message.plain = msgBody
			mailer.send(message)
	except Exception as e:
		print "No hay alarma setteada"
	

	c.execute("INSERT INTO Medicion(Time, Temperature) VALUES ('%s', '%s')" %(str(etime), str(rawString)))
	conn.commit()

mailer.stop()