#!/usr/bin/python
# -*- coding: utf8 -*-
## Steuerungs Script Domenik Zimmermann
version = 3.5-github

# Zuluftsteuerung und Zuteilung der einzelnen Messpunkte
# Temp/RH1: Schrank
# Temp/RH2: Raum 
# Temp/RH3: Aussen
test_light = "false"
test_relais = "false"

# Speichert Werte in Datenbank
import mysql.connector
use_db = "true"
create_new_db = "false"
####################################
DB_NAME = 'klima_growbox'
DB_TABLE = 'daten'
#
DB_USER = 'pi'
DB_PASSWD = 'pi'
DB_HOST = 'localhost'
####################################

import math				#fuer absolute feuchte rechnung
import RPi.GPIO as GPIO
import time,re, os			# import for and database entries
import Adafruit_DHT			# import for DHT22-inclusion
import datetime				# Datensicherung in Datei

now = datetime.datetime.now()

###############################################
#be verbose! detailliertere fehlermeldungen, 0=normal -- 1=detalliert
verbose = 1

if verbose != 1:
	 GPIO.setwarnings(False)
###############################################

GPIO.setmode(GPIO.BCM)		#GPIO-numbering
#GPIO.setmode(GPIO.BOARD)	#Pin-numbering 1-40

# Relais-Pins
fanpinlow = 5				# Relais-Pin der kleinsten Luefter-Spannungsversorgung
fanpinmid = 6
fanpinhigh = 13				# Relais-Pin der hoechsten Luefter-Spannungsversorgung
intakepin = 19				# GPIO-Pin des Zuluft-Fan-Relais
lightpin = 26				# GPIO des Licht-Relais
rh1pin = 16				    # auch wennGPIO.BOARD gesetzt ist, Pin zwischen 0-31 setzen (DHT22) BOARDpin 32 = BCOMpin 12
rh2pin = 20				# auch wennGPIO.BOARD gesetzt ist, Pin zwischen 0-31 setzen (DHT22) BOARDpin 32 = BCOMpin 12
rh3pin = 21				# auch wennGPIO.BOARD gesetzt ist, Pin zwischen 0-31 setzen (DHT22) BOARDpin 32 = BCOMpin 12

GPIO.setup(fanpinlow, GPIO.OUT)
GPIO.setup(fanpinmid, GPIO.OUT)
GPIO.setup(fanpinhigh, GPIO.OUT)
GPIO.setup(intakepin, GPIO.OUT)
GPIO.setup(lightpin, GPIO.OUT)

GPIO.setup(rh1pin, GPIO.IN)
GPIO.setup(rh2pin, GPIO.IN)
GPIO.setup(rh3pin, GPIO.IN)
 
# Setzt die Sollwerte
# Temperaturmessung
tmax = 25
tmin = 15
rhsoll = 50				# RH in percent to maintain

tmid = (tmax  + tmin) / 2
##########################################
fanstate = "off"		# Zustand der Abluft -- values: {off/low/mid/high}
fanstateold = "off"		# vorheriger fanstate
intakestate = "on"		# Zustand der Zuluft -- values: {on/off)
lightstate = "off"
# RH messung
rhsensor = Adafruit_DHT.DHT22

# Vergleich der temperaturen mit Sollwert und wechsel des fan-relais falls noetig
def lti_relais_control():
	global fanstate
	if verbose == 1:
		print('fan_control: fanstate is {}'.format(fanstate))
	fanstateold = fanstate		#save ols fanstate for comparison if one has to switch
	temp = t1					# regulate on t1 (rh1pin)
	######################## Entscheidet sich fur eine 
	if temp < tmin:
		fanstate = "off"
		if verbose == 1:
			if fanstate != fanstateold:		
				print('fan_control: fan state changed to {}'.format(fanstate))

	if tmin < temp < tmid:
		fanstate = "low"
		if verbose == 1:
			if fanstate != fanstateold:		
				print('fan_control: fan state changed to {}'.format(fanstate))

	if tmid < temp < tmax:
		fanstate = "mid"
		if verbose == 1:
			if fanstate != fanstateold:		
				print('fan_control: fan state changed to {}'.format(fanstate))

	if temp > tmax:
		fanstate = "high"
		if verbose == 1:
			if fanstate != fanstateold:		
				print('fan_control: fan state changed to {}'.format(fanstate))
	######################## Regelt die Fan-Relais
	if fanstate != fanstateold:		# schaltet fan-relais nur wenn noetig
		if fanstate == "off":
			switch_of_fan()
		elif fanstate == "low":
			switch_of_fan()
			GPIO.output(fanpinlow, 1)
			if verbose == 1:
				print('fan_control: switched on fan-relais ({})'.format(fanstate))
		elif fanstate == "mid":
			switch_of_fan()
			GPIO.output(fanpinmid, 1)
			if verbose == 1:
				print('fan_control: switched on fan-relais ({})'.format(fanstate))
		elif fanstate == "high":
			switch_of_fan()
			GPIO.output(fanpinhigh, 1)
			if verbose == 1:
				print('fan_control: switched on fan-relais ({})'.format(fanstate))
	else:
		print('fan_control: No change in fan')
def intake_relais_control():
	global intakestate

	if verbose == 1:
		print('intake_relais_control: instakestate is {}'.format(intakestate))
	intakestateold = intakestate		#save ols fanstate for comparison if one has to switch
	if (absdraussen < absdrinnen):   #draussen ist die abs.feuchte kleiner als drinnen
	        intakestate = "on"
		switch_on_intake()
	else:
		intakestate = "off"	
	
	if fanstate != fanstateold:		# schaltet fan-relais nur wenn noetig
		if intakestate == "off":
			switch_off_intake()		
	
	else:
		print('fan_control: No change in fan')

def switch_off_intake():
	GPIO.output(intakepin, 0)
	if verbose == 1:
		print('switch_of_intake: switched off intake-relais')

def switch_on_intake():
	GPIO.output(intakepin, 1)
	if verbose == 1:
		print('switch_on_intake: switched on intake-relais')


def switch_of_fan():
	GPIO.output(fanpinlow, 0)
	if verbose == 1:
		print('switch_of_fan: switched off fan-relais (low)')
	GPIO.output(fanpinmid, 0)
	if verbose == 1:
		print('switch_of_fan: switched off fan-relais (mid)')
	GPIO.output(fanpinhigh, 0)
	if verbose == 1:
		print('switch_of_fan: switched off fan-relais (high)')
	print('switch_of_fan: switched off all fan-relais')
	
def switch_light(status):
	global lightstate	

	if status != lightstate:
		if status == "on":
			GPIO.output(lightpin, 1)
			lightstate = "on"
			if verbose == 1:
				print('switch_light: Switch on light.')
		else:
			GPIO.output(lightpin, 0)
			lightstate = "off"
			if verbose == 1:
				print('switch_light: Switch off light.')
		
def test_light(repeattimes):
        # schaltet das licht ein (5s) und aus (2s)
	for i in range(0,repeattimes):
		switch_light("on")
		time.sleep(5)		#10s Pause
		switch_light("off")
		time.sleep(2)

def test_relais(repeattimes):
        # schaltet relais der reihe nach ein (5s) und aus (2s)
	for i in range(0,repeattimes):
		switch_of_fan()
		GPIO.output(fanpinlow, 1)
		time.sleep(2)
		GPIO.output(fanpinlow, 0)
		GPIO.output(fanpinmid, 1)
		time.sleep(2)
		GPIO.output(fanpinmid, 0)
		GPIO.output(fanpinhigh, 1)
		time.sleep(2)
		GPIO.output(fanpinhigh, 0)

		
def status_to_console():
	if verbose == 0:
		os.system('clear')
	if verbose == 1:
		print('This is Version {}'.format(version))
	print '******Temp/Humidity Test******'
	print '###Conditions###'
	print 'Air Temp (Maintained): {}'.format(tmid)
	print 'Air Temp Upper: {}'.format(tmax)
	print 'Air Temp Lower: {}'.format(tmin)
	print ''
	print 'Light is: {}'.format(lightstate)
	print'Current RH1/T1: {}%/{}*C'.format(rh1,t1)
	print'Current RH2/T2: {}%/{}*C'.format(rh2,t2)
	print'Current RH3/T3: {}%/{}*C'.format(rh3,t3)
	print'[g/m³] (draußen / drinnen) {}/{}'.format(absdraussen,absdrinnen)
	print('Fan-level: {}'.format(fanstate))
	print('Intake-level: {}'.format(intakestate))
	if verbose == 1:
		print ('Datenbanktimestamp: {} ist {}'.format(timestamp,datetime.datetime.fromtimestamp(timestamp/1000.0)))
		print('now.isoformat(): {}'.format(now.isoformat()))
		print '######################### End of Cycle #########################'
	print ''

def read_temperatures():
# Schreibt alle Variablen fuer die anderen Funktionen
	global rh1,rh2,rh3,t1,t2,t3
	global absdraussen,absdrinnen
	global timestamp
  #zeit im ms seid 1/1/1970 + 2h UTC=>berlin+7200					
	timestamp = time.time()*1000+7200	

	humidity, temperature = Adafruit_DHT.read_retry(rhsensor,rh1pin)
	rh1 = round(humidity,1)
	t1 = round(temperature,1)
	if verbose == 1:
		print('main: Sensor1: DHT{} -- Temp={}*C  Humidity={}%'.format(rhsensor,t1,rh1))

	humidity, temperature = Adafruit_DHT.read_retry(rhsensor,rh2pin)
	rh2 = round(humidity,1)
	t2 = round(temperature,1)
	if verbose == 1:
		print('main: Sensor2: DHT{} -- Temp={}*C  Humidity={}%'.format(rhsensor,t2,rh2))

	humidity, temperature = Adafruit_DHT.read_retry(rhsensor,rh3pin)
	rh3 = round(humidity,1)
	t3 = round(temperature,1)
	if verbose == 1:
		print('main: Sensor3: DHT{} -- Temp={}*C  Humidity={}%'.format(rhsensor,t3,rh3))
	
	absdraussen = round(absfeucht(t1,rh1),3)
	absdrinnen = round(absfeucht(t2,rh2),3)

def absfeucht(t,rh):
        tk=t+273.15 ## Temperatur in Kelvin

# sdd Sattigungsdampfdruck bei Temperatur T
        sdd = 6.1078 * 10**((7.5*t)/(237.3+t))
 
# Partialdruck des enthaltenen Wassers ist pd=sdd*rh1/100 (Sattigungsdampfdruck*RLF)
        pd=sdd*rh/100
# Taupunkttemperatur
        td = 237.3*math.log10(pd/6.1078)/(7.5-math.log10(pd/6.1078))
# absolute feuchte
        af = 100000*(18.016)/(8314)*pd/tk
        if verbose == 1:
                print ('T={},RH={} ==> Absolute Feuchte {} [g/m^3]').format(t,rh,af)
        return af


def init_sensors():
	print('    Initialisiere Messpunkte (DHT22 1-3) mit Adafruit-Library...')
	read_temperatures()
	print('    Alle Sensoren angesprochen, beginne mit Steuerung...')

	####################################### SQL-STUFF #############################
def create_database_stucture():
	if verbose == "1":
		print('Erzeuge neue Datenbankstruktur {}.{}'.format(DB_NAME,DB_TABLE))	
	try:
		cnx = mysql.connector.connect(user='root', password='3e64J%', host='localhost')
		cursor = cnx.cursor()
		cursor.execute("DROP USER {}@'localhost'".format(DB_USER))
		cursor.execute("DROP DATABASE {}".format(DB_NAME))
		cursor.execute("CREATE USER 'pi'@'localhost' IDENTIFIED BY 'pi'")
		cursor.execute("CREATE DATABASE IF NOT EXISTS {} CHARACTER SET=utf8".format(DB_NAME))
		cursor.execute("CREATE TABLE IF NOT EXISTS {}.{} (timestamp REAL, date DATETIME, temp1 REAL, temp2 REAL, temp3 REAL, rh1 REAL, rh2 REAL, rh3 REAL, tmax REAL, tmin REAL, absdraussen REAL, absdrinnen REAL) CHARACTER SET=utf8".format(DB_NAME,DB_TABLE))
		cursor.execute("GRANT ALL PRIVILEGES on {}.{} TO 'pi'@'localhost'".format(DB_NAME,DB_TABLE))
		cursor.execute("FLUSH PRIVILEGES")
	except mysql.connector.Error as err:
		print(err)
	###################################
def insert_into_sql():
	try:
		cnx = mysql.connector.connect(user=DB_USER, password=DB_PASSWD, host=DB_HOST)
		cursor = cnx.cursor()
	except mysql.connector.Error as err:
		print("Failed connecting database {}: {}".format(DB_NAME,err))
		
	date = "'"+str(time.strftime('%Y-%m-%dT%H:%M:%S'))+"'"		#SQL compatible time-object
	
	try:
		cursor.execute("INSERT into {}.{} values ({},{},{},{},{},{},{},{},{},{},{},{})".format(DB_NAME,DB_TABLE,timestamp,date,t1,t2,t3,rh1,rh2,rh3,tmax,tmin,absdraussen,absdrinnen))
		cnx.commit()
	except mysql.connector.Error as err:
		print("Failed inserting ({},{},{},{},{},{},{},{},{},{},{},{}) into table {}/{}: {}".format(timestamp,date,t1,t2,t3,rh1,rh2,rh3,tmax,tmin,absdraussen,absdrinnen,DB_NAME,DB_TABLE,err))
	##########################################################################
	
################### MAIN #########################
##Testroutinen
if test_light == "true":	
	test_light(1)
if test_relais == "true":	
	test_relais(1)
##
##########################
init_sensors()

if create_new_db == "true":	
	create_database_stucture()
while 1:
	try:	
		read_temperatures()
		lti_relais_control()
		intake_relais_control()
		
		status_to_console()
		if use_db == "true":
			insert_into_sql()

	except KeyboardInterrupt:
		print('captured CRTL+C . . . resetting ports ... exiting')
		GPIO.cleanup()	
		break
#####################################################
