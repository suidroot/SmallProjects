import serial
import time
import signal
import os
# import curses
# from curses.textpad import Textbox, rectangle
# import io

PORT = '/dev/ttyUSB0'
SPEED = 115200
DEBUG = False #True

def openserial():
	ser = serial.Serial(PORT, baudrate=SPEED, timeout=1, xonxoff=False, 
		rtscts=False, dsrdtr=False)
	print(ser.name)         # check which port was really used

	return ser

def sendcommand(command, returnlength):

	ser.write(command + '\r')     # write a string
	ser.flush()
	line = ser.read(returnlength)

	if DEBUG:
		print line

	if 'ERR' in line:
		print "INVALID COMMAND!!!!"

	return line

def checkok(radiooutput):

	radiooutput = radiooutput.split(',')[1]
	radiooutput = radiooutput.strip()

	if radiooutput != 'OK':
		print "ERROR"
		status = False
	else:
		status = True

	return status

def collectscreen():

	line = sendcommand('STS', 136)
	displayarray = line.split(',')

	if DEBUG:
		print displayarray

	if displayarray[1] == '011000':
		# Home Screen
		# ['STS', '011000', '                ', '', 'PortlandCity    ', '', 
		# 'H   ID SEARC \x81  ', '', ' 852.7875       ', '', 'S0:----------   ', 
		# '', '              WX', '', '1', '1', '0', '0', '0', '0', '0', '', 
		# '3\r'] 0 - 22
		line1 = displayarray[4].strip()
		line2 = displayarray[6].strip()
		line3 = displayarray[10].strip()
                # print 'line1' + line1
                # print 'line2' + line2
                # print 'line3' + line3
		modes = displayarray[12].split()

		frequency = displayarray[8].strip() # text float value

		squelchmode = bool(displayarray[15]) # 0 or 1
		mutemode = bool(displayarray[16]) # 0 or 1

		weatheralertstatus = displayarray[18] # 0 or 1 or $$$
		ccled = bool(displayarray[19]) # 0 or 1
		alertled = bool(displayarray[20]) # 0 or 1

		backlightlevel = int(displayarray[22]) # 1 - 3

		#leds
		return line1, line2, line3 #, modes, frequency

	elif displayarray[1] == '1111':
		# Menu 0 - 18
		# ['STS', '1111', ' -- M E N U --  ', '________________', 
		# 'Program System  ', '****************', 'Program Location', '', 
		# 'Srch/CloCall Opt', '', '1', '1', '0', '0', '0', '0', '0', '', '3\r']
		line1 = displayarray[2].strip()
		line2 = displayarray[4].strip()
		line3 = displayarray[6].strip()
		line4 = displayarray[8].strip()

		squelchmode = bool(displayarray[10]) # 0 or 1
		mutemode = bool(displayarray[11]) # 0 or 1

		weatheralertstatus = displayarray[13] # 0 or 1 or $$$
		ccled = bool(displayarray[15]) # 0 or 1
		alertled = bool(displayarray[16]) # 0 or 1

		backlightlevel = int(displayarray[18]) # 1 - 3


		return line1, line2, line3, line4

def signalstrength():

	line = sendcommand('PWR', 17)
	powerarray = line.split(',')
	powerpercent = (int(powerarray[1])/1023)*100

	if DEBUG:
		print powerarray

	# Return singal power, and 3 screen lines
	return powerpercent

def volume(setvol=''):

	if setvol == '':
		volume = sendcommand('VOL', 6)
		status = 'SET'
		volume = volume.split(',')[1]

	else:
		volume = sendcommand('VOL,' + str(setvol), 6)
		status = checkok(radioout)
		volume = setvol

	return status, volume

def squelch(setsql=''):

	if setsql == '':
		squelch = sendcommand('SQL', 6)
		status = 'SET'
		squelch = squelch.split(',')[1]

	else:
		squelch = sendcommand('SQL,' + str(setsql), 6)
		status = checkok(radioout)
		squelch = setsql

	return status, squelch

def getinfo():
	# MDL Get Model Info
	# VER Get Firmware Version
	model = sendcommand('MDL', 10)
	model = model.split(',')
	version = sendcommand('VER', 10)
	version = version.split(',')

	return version, model

def buttonpush(key, mode, function=False):

	validmodes = ['P', 'L', 'H', 'R']
	validkeys = ['P', 'W', 'G', 'M', 'F', 'H', 
	'S', 'L', '1', '2', '3', '4', '5', '6', '7',
	'8', '9', '0', '.', 'E', 'Q', 'V', '<', '>']

	if function == True:
		radioout = sendcommand('KEY,F,P', 10)
		checkok(radioout)


	if key not in validkeys:
		print 'KEY ERROR'

	if mode not in validmodes:
		print 'MODE ERROR'

	radioin = 'KEY,' + key + ',' + mode

	radioout = sendcommand(radioin, 10)
	status = checkok(radioout)

	return status


def menu(line1, line2, line3, strength='', vol='', sql=''):

	spacerwith = 30

 	spacer1 = " " * (spacerwith - len(line1))
 	spacer2 = " " * (spacerwith - len(line2))
 	spacer3 = " " * (spacerwith - len(line3))

 	
 	# print 35 - len(str(vol))

	display = """
  +--------------------------------+
  | {0} {3}|
  | {1} {4}|
  | {2} {5}|
  +--------------------------------+
  """.format(line1, line2, line3, spacer1, spacer2, spacer3)


  	if strength != '':
		vol = vol.strip()
		sql = sql.strip()

	 	spacer4 = " " * (13 - len(str(strength)))
	 	spacer5 = " " * (22 - len(str(vol)))
	 	spacer6 = " " * (21 - len(str(sql)))

		levels = """| Signal Strength: {0} {3}|
  | Volume: {1} {4}|
  | Squelch: {2} {5}|
  +--------------------------------+""".format(strength, vol, sql, spacer4, spacer5, spacer6)
	else:
		levels = ''


	controls = """| P PRI          < Turn Knob >   |
  | W WX   |1|2|3|      *  *       |
  | G GPS  |4|5|6|   *        *    |
  | M MENU |7|8|9|  *  Push =  *   |
  | L L/O  |.|0|E|  *     F    *   |
  | V VOL Push       *        *    |
  | Q SQL Push          *  *       |
  | S Scan/Search                  |
  | H Hold                         |
  | Z Radio Info                   |
  +--------------------------------+
  | Modes                          |
  | P = Press, L = Long Press      |
  | H = Hold, R = Release          |
  +--------------------------------+
  | B Set Volume                   |
  | D Set Squelch                  |
  +--------------------------------+
"""

	fullmenu = display + levels + controls

	return fullmenu


def commandloop(button):

	# set time out
	# funtion 2 sec
	# system 3 sec

	if button == 'F':
		timeout = 2
	elif button == '<' or '>':
		timeout = 3

		 
	line1, line2, line3 = collectscreen()
	print menu(line1, line2, line3)

	print "You have ten seconds to answer!"

	i, o, e = select.select( [sys.stdin], [], [], 10 )

	if (i):
	  print "You said", sys.stdin.readline().strip()
	else:
	  print "You said nothing!"

	time.sleep(timeout)



##############
# Main Routines
##############
ser = openserial()

try:
	while True:
		line1, line2, line3 = collectscreen()
		strength = signalstrength()
		vol =  volume()[1]
		sql =  squelch()[1]

		os.system('clear')
		print menu(line1, line2, line3, strenght, vol, sql)
		time.sleep(1)

except KeyboardInterrupt:
	print "W: interrupt received, stopping..."
	ser.close()


finally:
	ser.close()


