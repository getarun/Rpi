
#!/usr/bin/python
# -*- coding: utf8 -*-
## Steuerungs Script

# Zuluftsteuerung und Zuteilung der einzelnen Messpunkte
version     = 	"update to rpi 4.1.1"
test_light  = 	"false"
test_relais = 	"false"
use_db      = 	"true"
use_file    = 	"true"
create_new_db = "false"
#use_json    =	"false"
import json
#be verbose! detailliertere fehlermeldungen, 0=normal -- 1=detalliert
verbose = 0
clear_konsole_after_cycle = 1

## checks command line for options "sudo python control.py test_light test_relais will enable test options
import sys
for arg in sys.argv:
	if arg == "test_relais":
		test_relais = "true"
	if arg == "test_light":
		test_light = "true"
	if arg == "use_db":
		use_db = "true"
	if arg == "use_file":
		use_file = "true"
	if arg == "use_json":
		use_json = "true"

# Speichert Werte in Datenbank
import mysql.connector
####################################
DB_NAME 	= 'klima_growbox'
DB_TABLE 	= 'daten'
DB_TABLE2 	= 'giessen'
#
DB_USER 	= 'pi'
DB_PASSWD 	= 'pi'
DB_HOST 	= 'localhost'
####################################

import math				#fuer absolute feuchte rechnung
import RPi.GPIO as GPIO
import time,re, os			# import for and database entries
import Adafruit_DHT			# import for DHT22-inclusion
import datetime				# Datensicherung in Datei

now = datetime.datetime.now()

###############################################
if verbose != 1:
	 GPIO.setwarnings(False)
###############################################

GPIO.setmode(GPIO.BCM)		#GPIO-numbering
#GPIO.setmode(GPIO.BOARD)	#Pin-numbering 1-40

# Relais-Pins
fanpinlow = 12				# Relais-Pin der kleinsten Luefter-Spannungsversorgung
fanpinmid = 6
fanpinhigh = 13				# Relais-Pin der hoechsten Luefter-Spannungsversorgung
intakepin = 19				# GPIO-Pin des Zuluft-Fan-Relais
lightpin = 26				# GPIO des Licht-Relais

############# Messungspins ############
# auch wennGPIO.BOARD gesetzt ist, Pin zwischen 0-31 setzen (DHT22) BOARDpin 32 = BCOMpin 12
rhsensor = Adafruit_DHT.DHT22
#
name1  = "        LSR    "	#absdraussen
rh1pin = 16				# T1 |	RH1 # langer Sensor -- Entfeuchter
name2  = "       Raum    "	#absdrinnen
rh2pin = 20				# T2 |	RH2 # Schrank
name3  = "        NDL    "
rh3pin = 21				# T3 |	RH3 # Zuluft
name4 = "Wassertemp"
#Pin 1-wire (GPIO5 geaenert in /boot/config.txt

#set output pins
GPIO.setup(fanpinlow, GPIO.OUT)
GPIO.setup(fanpinmid, GPIO.OUT)
GPIO.setup(fanpinhigh, GPIO.OUT)
GPIO.setup(intakepin, GPIO.OUT)
GPIO.setup(lightpin, GPIO.OUT)
#set input pins
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
lightstate = "off"
intakestate = "off"		# Zustand der Zuluft -- values: {on/off)


# Vergleich der temperaturen mit Sollwert und wechsel des fan-relais falls noetig
def lti_relais_control():
	global fanstate
	if verbose == 1:
		print('fan_control: fanstate is {}'.format(fanstate))
	fanstateold = fanstate		#save ols fanstate for comparison if one has to switch
	temp = t3			# regulate on t2 (rh2pin)				#######################
	######################## Entscheidet sich fur ein LTI-level
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
	
	if intakestate != intakestateold:		# schaltet fan-relais nur wenn noetig
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
	if verbose == 1:
		print('test_light: Teste Licht:')
        # schaltet das licht ein (5s) und aus (2s)
	for i in range(0,repeattimes):
		switch_light("on")
		time.sleep(5)		#10s Pause
		switch_light("off")
		time.sleep(2)

def test_relais(repeattimes):
	if verbose == 1:
		print('test_relais: Teste Relais:')
        # schaltet relais der reihe nach ein (5s) und aus (2s)
	for i in range(0,repeattimes):
		if verbose == 1:
			print('test_relais: Teste Relais...beginnne mit alle aus und schalte FAN[low|mid|high] der Reihe nach (an(2sec)aus) ')
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
	if clear_konsole_after_cycle == 1:
		#time.sleep(5)
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
	print'RH1/T1:: {} ::   {}% | {}*C'.format(name1,rh1,t1)
	print'RH2/T2:: {} ::   {}% | {}*C'.format(name2,rh2,t2)
	print'RH3/T3:: {} ::   {}% | {}*C'.format(name3,rh3,t3)
	print'DS18B :: {} ::   {}*C'.format(name4,t4)
	print'[g/cmeter] (AUX/Schrank) :: {} | {}'.format(absdraussen,absdrinnen)
	print ''
	print('Fan-level: {}'.format(fanstate))
	print('Intake-level: {}'.format(intakestate))
	if verbose == 1:
		print ''
		print ('Datenbanktimestamp: {} ist {}'.format(timestamp,datetime.datetime.fromtimestamp(timestamp/1000.0)))
		print('now.isoformat():                         {}'.format(now.isoformat()))
		print '######################### End of Cycle #########################'
	print ''


def read_temperatures():
# Schreibt alle Variablen fuer die anderen Funktionen
	global rh1,rh2,rh3,t1,t2,t3,t4
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
	
	absdraussen = round(absfeucht(t2,rh2),2)						######################
	absdrinnen = round(absfeucht(t3,rh3),2)							######################

# Wassertemperatur mittels DS18B20 lesen
	id="28-021502f5e1ff"
	t4=read_DS18B20(id)
	
	
def absfeucht(t,rh):
# Temperatur in Kelvin
        tk=t+273.15 
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

def read_DS18B20(id):
  path="/sys/bus/w1/devices/"+id+"/w1_slave"
  if verbose == 1:
  	print ('Sensor---Path{}').format(path)
  try:
    sensorfile = open(path, "r")
    outputtext = sensorfile.read()
    sensorfile.close()
    tempdata = outputtext.split("\n")[1].split(" ")[9]
    temperature = float(tempdata[2:])
    temperature = temperature / 1000
  except (IOError), e:
    print time.strftime("%x %X"), "Error reading", path, ": ", e
  return temperature

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
#		cursor.execute("DROP USER {}@'localhost'".format(DB_USER))
#		cursor.execute("DROP DATABASE {}".format(DB_NAME))
#		cursor.execute("CREATE USER 'pi'@'localhost' IDENTIFIED BY 'pi'")
		cursor.execute("CREATE DATABASE IF NOT EXISTS {} CHARACTER SET=utf8".format(DB_NAME))
		cursor.execute("CREATE TABLE IF NOT EXISTS {}.{} (timestamp REAL, date DATETIME, temp1 REAL, temp2 REAL, temp3 REAL, rh1 REAL, rh2 REAL, rh3 REAL, tmax REAL, tmin REAL, absdraussen REAL, absdrinnen REAL, t4 REAL) CHARACTER SET=utf8".format(DB_NAME,DB_TABLE))
		cursor.execute("CREATE TABLE IF NOT EXISTS {}.{} (timestamp REAL, plantnumber INT, amount INT, PH REAL, EC REAL) CHARACTER SET=utf8".format(DB_NAME,DB_TABLE2))
		cursor.execute("GRANT ALL PRIVILEGES on {}.{} TO 'pi'@'localhost'".format(DB_NAME,DB_TABLE))
		cursor.execute("GRANT ALL PRIVILEGES on {}.{} TO 'pi'@'localhost'".format(DB_NAME,DB_TABLE2))
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
		cursor.execute("INSERT into {}.{} values ({},{},{},{},{},{},{},{},{},{},{},{},{})".format(DB_NAME,DB_TABLE,timestamp,date,t1,t2,t3,rh1,rh2,rh3,tmax,tmin,absdraussen,absdrinnen,t4))
		cnx.commit()
	except mysql.connector.Error as err:
		print("Failed inserting ({},{},{},{},{},{},{},{},{},{},{},{},{}) into table {}/{}: {}".format(timestamp,date,t1,t2,t3,rh1,rh2,rh3,tmax,tmin,absdraussen,absdrinnen,t4,DB_NAME,DB_TABLE,err))
	##########################################################################
	
def insert_into_file():
	if verbose == "1":
		print("Writing values {},{},{},{},{},{},{},{},{},{},{},{},{} into file".format(timestamp,date,t1,t2,t3,rh1,rh2,rh3,tmax,tmin,absdraussen,absdrinnen,t4))
	if use_json == "false":
		with open("./data.list", "a") as file_list:
			file_list.write(timestamp+"\t"+date+"\t"+t1+"\t"+t2+"\t"+t3+"\t"+rh1+"\t"+rh2+"\t"+rh3+"\t"+tmax+"\t"+tmin+"\t"+absdraussen+"\t"+absdrinnen+"\t"+t4+"\n")
	if use_json == "true":
		print 'JSON-insert-into-file: removed because not tested'
		#with open("./data.json", "a") as file_json:
		#	old_data = file_json.read()
		#	data = old_data
		#	file_json.write("[",json.dumps([timestamp, t1,t2,t3,rh1,rh2,rh3,absdraussen,absdrinnen],"]"))
################### MAIN #########################
##Testroutinen
if test_light == "true":	
	test_light(2)
if test_relais == "true":	
	test_relais(2)
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
		if use_file == "true":
			insert_into_file()

	except KeyboardInterrupt:
		print('captured CRTL+C . . . resetting ports ... exiting')
		GPIO.cleanup()	
		break
#####################################################
