#!/usr/bin/python
"""\
Simple g-code streaming script

@modifier: @antoi
"""
 
import serial
import time
import argparse

## Global variables

number_of_lines = 0
trig = int(number_of_lines / 100)
counter = 0

parser = argparse.ArgumentParser(description='This is a basic gcode sender')
parser.add_argument('-p','--port',help='Input USB port',required=True)
parser.add_argument('-f','--file',help='Gcode file name',required=True)
args = parser.parse_args()
 
## show values ##
print ("USB Port: %s" % args.port )
print ("Gcode file: %s" % args.file )


def removeComment(string):
	if (string.find(';')==-1 or string.find('(') > 0):
		return string
	else:
		return string[:string.index(';')]

def checkTime(time1):
	# Get the current time 
	time2 = time.clock()
	#If 600 secondes have elapsed, we're taking a pause
	if ((time2-time1) > 540):	
		s.write("E0A".encode()) #E0A is the instruction to stop  drivers
		print("Pause de 30 sec afin d'éviter le surchauffement des drivers ...")
		time.sleep(30)
		print("Fin de la pause !")
		time.sleep(2)
		time1  = time.clock()
		s.write("E1A".encode()) #E1A is the instruction to relauch drivers
		return time1

	# Else we keep time1 value
	else:
		return time1

def sendPercentage(counter):
	percentage = int((counter/number_of_lines)*100)
	s.write(("P01A" + str(percentage)+"A").encode())
	grbl_out = s.readline() # Wait for response with carriage return
	while grbl_out!=b'OK\r\n':
		print(grbl_out)
		grbl_out = s.readline() # Wait for response with carriage return
		time.sleep(0.05)

 
# Open serial port
s = serial.Serial(args.port,9600)
print ('Opening Serial Port')
 
# Open g-code file
f = open(args.file,'r')
print ('Opening gcode file')

for line in f:
	number_of_lines+=1

print(str(number_of_lines) + " lignes\n")
f.close()

f = open(args.file, 'r')

 
# Wake up 
time.sleep(2)   # Wait for Printrbot to initialize
#s.flushInput()  # Flush startup text in serial input
print ('Sending gcode\n\n')

# Start the Chrono
time1 = time.clock()
 
# Stream g-code
for line in f:
	l = removeComment(line)
	l = l.replace(" ","A")
	l = l.strip() # Strip all EOL characters for streaming
	
	#Check execution time >15 min and stop 2 min if it is the case
	time1 = checkTime(time1)

	#Send a percentage message all 1% 
	#sendPercentage(counter)
	if  (l.isspace()==False and len(l)>0) :

		l+='A'
		print ('Sending: ' + l)
		l+='\n'
		s.write((l + '\n').encode()) # Send g-code block
		time.sleep(0.3)
		print("Waiting responses :\n")
		grbl_out = s.readline() # Wait for response with carriage return

		while grbl_out!=b'OK\r\n':
			print(grbl_out)
			grbl_out = s.readline() # Wait for response with carriage return
			time.sleep(0.05)

		print(grbl_out)
		grbl_out = ""
		print("\n")
		counter+=1
	     
 
# Close file and serial port
f.close()
s.close()

