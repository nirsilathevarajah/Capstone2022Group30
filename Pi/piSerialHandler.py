#!/usr/bin/python3
import serial
import time

ser = serial.Serial("/dev/ttyACM0", 56700, timeout=1)

# Reset the Arduino's line. This is key to getting the write to work.
# Without it, the first few writes don't work.
# Clear DTR, wait one second, flush input, then set DTR.
# Without this, the first write fails.
# This trick was learned from:
# https://github.com/miguelasd688/4-legged-robot-model

global startMeasuring
global temperature
global heartRate
global systolic
global diastolic

startMeasuring = False
temperature = 0
heartRate = 0
systolic = 0
diastolic = 0

count = 0

ser.setDTR(False)
time.sleep(1)
ser.flushInput()
ser.setDTR(True)
time.sleep(2)

# getter and setter functions for startMeasuring
def getStartMeasuring():
	return startMeasuring
	
def setStartMeasuring(val):
	global startMeasuring
	startMeasuring = val
	
# getter and setter functions for sensor values
def getSensorValues():
	sensorValues = [temperature, heartRate, systolic, diastolic]
	return sensorValues
	
def setSensorValues(temp, hr, sys, dia):
	global temperature
	global heartRate
	global systolic
	global diastolic
	temperature = temp
	heartRate = hr
	systolic = sys
	diastolic = dia

while True:
	if count == 1:
		setStartMeasuring(True)
	
	count+=1
	
	startMeasuringTrigger = getStartMeasuring()
	
	if(startMeasuringTrigger):
		print('Telling the Arduino to start measuring...')
		ser.write(b'0')

		# read to get the acknowledgement from the Arduino
		while True:
			ack = ser.read()
			if ack == b'A':
				break
			else:
				msg = ser.readline()
				print(msg)
		print('Arduino sent back %s' % ack)
		setStartMeasuring(False)
	else:
		print('startMeasuringTrigger not enabled')

	# read to check if arduino is sending sensor data
	serRx = ser.read()
	if serRx == b'T':
		sensorRead = ser.readline().decode('ascii').rstrip().split(',')
		setSensorValues(sensorRead[0], sensorRead[1], sensorRead[2], sensorRead[3])
		sensorValues = getSensorValues()
		print(sensorValues)
	else:
		print("no sensor values received")
		

	
