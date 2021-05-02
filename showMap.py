import io
import os
import sys
import math
import time
import json
import pygame
import requests
import argparse
import pygame.locals
from io import BytesIO
from PIL import Image

# --- Variables -----------------------------------------------------------------------------------

pygame.init()
version = '1.0'	# All done
font09 = pygame.font.Font('freesansbold.ttf', 9)
font20 = pygame.font.Font('freesansbold.ttf', 20)
font30 = pygame.font.Font('freesansbold.ttf', 30)
baseUrl = 'http://127.0.0.1:8111/'.rstrip('/')
#mapObj = json.loads(requests.get(baseUrl + 'map_obj.json').content)
#mapInfo = json.loads(requests.get(baseUrl + 'map_info.json').content)
#print(json.dumps(mapObj, indent=2, sort_keys=True))
objTypes = []
correction = [0, 0, 1.0]
zoneLetters = ['A', 'B', 'C', 'D']
msgActions = ['destroyed', 'has achieved', 'has disconnected', 'set afire', 'has delivered', 'damaged', 'shot down', 'has crashed', 'performed a soft landing', 'has been wrecked']
gridLetters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


# --- Functions -----------------------------------------------------------------------------------

# --- Classes -------------------------------------------------------------------------------------

class colorList:

	black =			(0, 0, 0)
	white =			(255, 255, 255)
	red =			(255, 0, 0)
	cyan =			(0, 255, 255)
	green =			(0, 255, 0)
	grey =			(150, 150, 150)
	darkGrey =		(50, 50, 50)
	almostBlack =	(20, 20, 20)
	orange =		(220, 162, 57)
	green =			(70, 180, 50)
	blue =			(80, 120, 250)
	background =	(55, 55, 55)


class MapObject():

	def __init__(self, xPos, yPos, color, oType, angle = False, extra = None):
		self.xPos = xPos
		self.yPos = yPos
		self.type = oType
		self.extra = extra		# used for airfields
		if oType == 0:		# unknown
			self.image = pygame.Surface((13, 13), pygame.SRCALPHA)
			pygame.draw.circle(self.image, colors.black, (7, 7), 6)
			pygame.draw.circle(self.image, color,     (7, 7), 4)
		elif oType == 99:		# capture zone
			letter = zoneLetters.pop(0)
			self.image = pygame.Surface((19, 19), pygame.SRCALPHA)
			pygame.draw.polygon(self.image, colors.black,	[(9, 0), (18, 9), (9, 18), (0, 9)], False)
			pygame.draw.polygon(self.image, color,		[(9, 2), (16, 9), (9, 16), (2, 9)], False)
			font09.set_bold(True)
			text = font09.render(letter, True, colors.black, color)
			textRect = text.get_rect()
			textRect.topleft = (6, 5)
			self.image.blit(text, textRect)
		elif oType == 2:		# respawn, bomber
				self.image = pygame.image.load("icons/bomber_spawn_red.png") if color == (255, 13, 0) else pygame.image.load("icons/bomber_spawn_blue.png")
		elif oType == 3:		# respawn, fighter
				self.image = pygame.image.load("icons/fighter_spawn_red.png") if color == (255, 13, 0) else pygame.image.load("icons/fighter_spawn_blue.png")
		elif oType == 4:		# respawn, tank
				self.image = pygame.image.load("icons/tank_spawn_red.png") if color == (255, 13, 0) else pygame.image.load("icons/tank_spawn_blue.png")
		elif oType == 5:		# respawn, boat
				self.image = pygame.image.load("icons/boat_spawn_red.png") if color == (255, 13, 0) else pygame.image.load("icons/boat_spawn_blue.png")
		elif oType == 6:		# respawn, ship
				self.image = pygame.image.load("icons/ship_spawn_red.png") if color == (255, 13, 0) else pygame.image.load("icons/ship_spawn_blue.png")
		elif oType == 7:		# SPAA
			self.image = pygame.Surface((13, 8), pygame.SRCALPHA)
			pygame.draw.rect(self.image, colors.black,	(0, 4, 13, 4))
			pygame.draw.rect(self.image, colors.black,	(1, 0, 4, 8))
			pygame.draw.rect(self.image, colors.black,	(8, 0, 4, 8))
			pygame.draw.rect(self.image, color,	(1, 5, 11, 2))
			pygame.draw.rect(self.image, color,	(2, 1, 2, 6))
			pygame.draw.rect(self.image, color,	(9, 1, 2, 6))
		elif oType == 8:		# fighter
			self.image = pygame.Surface((13, 13), pygame.SRCALPHA)
			pygame.draw.polygon(self.image, colors.black,	[(6, 0), (12, 6), (6, 12), (0, 6)], False)
			pygame.draw.polygon(self.image, color,		[(6, 2), (10, 6), (6, 10), (2, 6)], False)
		elif oType == 9:		# assault plane
			self.image = pygame.Surface((13, 9), pygame.SRCALPHA)
			pygame.draw.polygon(self.image, (0,0,0),	[(0, 4), (6, 0), (12, 4), (6, 8)], False)
			pygame.draw.polygon(self.image, color,		[(1, 4), (6, 1), (11, 4), (6, 7)], False)
		elif oType == 10:	# bomber
			self.image = pygame.Surface((13, 13), pygame.SRCALPHA)
			pygame.draw.polygon(self.image, colors.black,	[(0, 0), (12, 0), (6, 12)], False)
			pygame.draw.polygon(self.image, color,		[(1, 1), (11, 1), (6, 11)], False)
		elif oType == 11:	# airdefence
			self.image = pygame.Surface((12, 12), pygame.SRCALPHA)
			pygame.draw.rect(self.image, colors.black,	(4, 0, 4, 12))
			pygame.draw.rect(self.image, colors.black,	(0, 8, 12, 4))
			pygame.draw.rect(self.image, color,	    (5, 1, 2, 10))
			pygame.draw.rect(self.image, color,		(1, 9, 10, 2))
		elif oType == 12:	# light tank
			self.image = pygame.Surface((12, 4), pygame.SRCALPHA)
			pygame.draw.rect(self.image, colors.black, (0, 0, 12, 4))
			pygame.draw.rect(self.image, color,	    (1, 1, 10, 2))
		elif oType == 13:	# medium tank
			self.image = pygame.Surface((12, 6), pygame.SRCALPHA)
			pygame.draw.rect(self.image, colors.black, (0, 0, 12, 4))
			pygame.draw.rect(self.image, colors.black, (0 ,0, 4, 6))
			pygame.draw.rect(self.image, colors.black, (8, 0, 4, 6))
			pygame.draw.rect(self.image, color,	    (1, 1, 10, 2))
			pygame.draw.rect(self.image, color,	    (1, 1, 2, 4))
			pygame.draw.rect(self.image, color,	    (9, 1, 2, 4))
		elif oType == 14:	# heavy tank
			self.image = pygame.Surface((12, 8), pygame.SRCALPHA)
			pygame.draw.rect(self.image, colors.black, (0, 2, 4, 6))
			pygame.draw.rect(self.image, colors.black, (3, 0, 6, 6))
			pygame.draw.rect(self.image, colors.black, (8, 2, 4, 6))
			pygame.draw.rect(self.image, color,	    (4, 1, 4, 2))
			pygame.draw.rect(self.image, color,	    (1, 3, 10, 2))
			pygame.draw.rect(self.image, color,	    (1, 5, 2, 2))
			pygame.draw.rect(self.image, color,	    (9, 5, 2, 2))
		elif oType == 15:	# tank destroyer
			self.image = pygame.Surface((13, 13), pygame.SRCALPHA)
			pygame.draw.polygon(self.image, colors.black,	[(0, 9), (7, 2), (9, 4), (4, 9), (12, 9), (12, 12), (0, 12)], False)
			pygame.draw.polygon(self.image, color,		[(1, 9), (7, 3), (8, 4), (3, 9)], False)
			pygame.draw.rect(self.image, color,	    (1, 10, 11, 2))
		elif oType == 16:		# Tracked'
			self.image = pygame.Surface((12, 6), pygame.SRCALPHA)
			pygame.draw.rect(self.image, colors.black, (0, 1, 12, 2))
			pygame.draw.rect(self.image, colors.black, (1, 0, 10, 4))
			pygame.draw.rect(self.image, color,	    (1, 2, 10, 2))
		elif oType == 17:		# 'Wheeled'
			self.image = pygame.Surface((12, 6), pygame.SRCALPHA)
			pygame.draw.circle(self.image, colors.black, (3, 3), 3)
			pygame.draw.circle(self.image, colors.black, (9, 3), 3)
			pygame.draw.circle(self.image, color, (3, 3), 2)
			pygame.draw.circle(self.image, color, (9, 3), 2)
		elif oType == 18:		# bluewater ship
			self.image = pygame.Surface((13, 13), pygame.SRCALPHA)
			pygame.draw.polygon(self.image, colors.black,  [(0, 6), (12, 6), (6, 12)], False)
			pygame.draw.polygon(self.image, colors.black,  [(2, 6), (6, 2), (10, 6)], False)
			pygame.draw.polygon(self.image, color, 		[(4, 5), (6, 3), (8, 5)], False)
			pygame.draw.polygon(self.image, color, 		[(2, 7), (10, 7), (6, 11)], False)
		elif oType == 19:		# boat
			self.image = pygame.Surface((13, 6), pygame.SRCALPHA)
			pygame.draw.polygon(self.image, colors.black,  [(0, 0), (12, 0), (10, 5), (2, 5)], False)
			pygame.draw.polygon(self.image, color,		[(1, 1), (11, 1), (9, 4), (3, 4)], False)
		elif oType == 20:		# torpedoboat
			self.image = pygame.Surface((13, 6), pygame.SRCALPHA)
			pygame.draw.polygon(self.image, colors.black,  [(0, 0), (12, 0), (10, 5), (2, 5)], False)
			pygame.draw.polygon(self.image, color,		[(1, 1), (11, 1), (9, 4), (3, 4)], False)
			pygame.draw.rect(self.image, colors.black, (5, 2, 7, 2))
		elif oType == 21:		# bombing point
			self.image = pygame.Surface((19, 19), pygame.SRCALPHA)
			pygame.draw.circle(self.image, color, (9, 9), 7)
			pygame.draw.circle(self.image, colors.black, (9, 9), 6)
			pygame.draw.rect(self.image, color, (8, 0, 2, 18))
			pygame.draw.rect(self.image, color, (0, 8, 18, 2))
		elif oType == 22:		# defending point
			self.image = pygame.Surface((19, 19), pygame.SRCALPHA)
			pygame.draw.circle(self.image, color, (9, 9), 9)
			pygame.draw.circle(self.image, colors.black, (9, 9), 8)
			pygame.draw.rect(self.image, color, (5, 5, 8, 6))
			pygame.draw.polygon(self.image, color, [(5, 11), (12, 11), (9, 14), (8, 14)], False)
		elif oType == 95:		# airfield
			_image = pygame.Surface((6 , 60), pygame.SRCALPHA)  		# always use same length for airfield
			pygame.draw.rect(_image, colors.black, (0, 0, 6, 60))
			pygame.draw.rect(_image, color, (1, 1, 4, 58))
			self.image = pygame.transform.rotate(_image , angle)
		elif oType == 100:		# player
			_image = pygame.image.load("icons/player.png")
			self.image = pygame.transform.rotozoom(_image, angle, 1)
			# offset = pygame.math.Vector2(0, 10) # move rotaion 10 up from center
			# rotated_image = pygame.transform.rotozoom(_image, angle, 1)  # Rotate the image.
			# rotated_offset = offset.rotate(-angle)  # Rotate the offset vector the other way (-angle)
			# _rect = rotated_image.get_rect(center = [int(i) for i in ((xPos, yPos) + rotated_offset)])
			self.xPos -= 10	# correction of player position compared to other objects, unknown why
			self.yPos -= 10
		elif oType == 150:		# test dot for corners
			self.image = pygame.Surface((1, 1), pygame.SRCALPHA)
			self.image.fill((0, 255, 255))
		else:					# unknown object
			self.image = pygame.Surface((7, 7), pygame.SRCALPHA)
			pygame.draw.circle(self.image, colors.black, (3, 3), 3)
			pygame.draw.circle(self.image, color, (3, 3), 2)



	def draw(self, _display, _zoom):
		w, h = self.image.get_size()
		x = int( correction[2] * (19 + self.xPos + _zoom[0]) * _zoom[2]) - int(w / 2) + correction[0]
		y = int( correction[2] * (19 + self.yPos + _zoom[1]) * _zoom[2]) - int(h / 2) + correction[1]
		_display.blit(self.image, (x, y) )



class WarThunderMap():
	""" get data from API and display it """

	def __init__(self):
		self.width = 1920
		self.height = 1080
		self.mapWidth = 1012
		self.mapHeight = 1012
		self.rawMap = False
		self.running = True
		self.mapObjects = None
		self.mapInfo = None
		self.drawList = []	# contains all objects to be drawn on map
		self.chatBuffer = []
		self.msgBuffer = []
		self.lastId = [1,1]
		self.zoomFactor = [0, 0, 1.0]
		self.blinkingInterval = 0
		pygame.init()
		programIcon = pygame.image.load("icons/war_thunder_icon.png")
		pygame.display.set_icon(programIcon)
		pygame.display.set_caption('War Thunder current map')
		self.display = pygame.display.set_mode((self.width,self.height))
		self.loop()


	def getMapObjects(self):
		""" querys server for map objects and updates mapObjects as json object """
		fileUrl = 'map_obj.json'
		url = f"{baseUrl}/{fileUrl}"
		try:
			reply = requests.get(url)
			self.mapObjects = json.loads(reply.content) if reply.content != b'' else json.loads(b'[]')
		except:
			return False
		if self.mapObjects == []:
			return False
		else:
			return True


	def getMapInfo(self):
		""" querys server for map info and updates mapObjects as json object """
		fileUrl = 'map_info.json'
		url = f"{baseUrl}/{fileUrl}"
		try:
			reply = requests.get(url)
			self.mapInfo = json.loads(reply.content) if reply.content != b'' else json.loads(b'[]')
		except:
			self.mapInfo = json.loads(b'[]')



	def drawGrid(self):
		if self.mapInfo:
			mapSize = self.mapInfo['map_max'][0] - self.mapInfo['map_min'][0]
			noOfSteps = mapSize / self.mapInfo['grid_steps'][0]
			scale = self.mapWidth / self.zoomCoords[2] if args.zoom else 1
			stepWidth = int(self.mapWidth / noOfSteps * scale)
			# draw horizontal and vertical lines
			offsetX = int(-(self.zoomCoords[0] % stepWidth) * scale) if args.zoom else 0
			offsetY = int(-(self.zoomCoords[1] % stepWidth) * scale) if args.zoom else 0
			counterX = int((self.zoomCoords[0] - (self.zoomCoords[0] % stepWidth)) / stepWidth) if args.zoom else 0
			counterY = int((self.zoomCoords[1] - (self.zoomCoords[1] % stepWidth)) / stepWidth) if args.zoom else 0
			# draw vertical lines 
			for x in range(stepWidth, self.mapWidth + stepWidth, stepWidth):
				counterX += 1
				x += 19 + offsetX
				pygame.draw.line(self.display, colors.black, (x, 19), (x, self.mapHeight + 19))
				text = font20.render(str(counterX + 1), True, colors.black)
				text.set_alpha(127)
				w, h = text.get_size()
				self.display.blit(text, (19 + int(x + (stepWidth / 2) - (w / 2)), 25))
			# print first column number
			text = font20.render('1', True, colors.black)
			text.set_alpha(127)
			w, h = text.get_size()
			self.display.blit(text, (19 + int(((stepWidth + offsetX) / 2) - (w / 2)), 25))
			# # draw horizontal lines
			for x in range(stepWidth, self.mapWidth + stepWidth, stepWidth):
				counterY += 1
				x += 19 + offsetY
				pygame.draw.line(self.display, colors.black, (19, x), (self.mapWidth + 19, x))
				text2 = font20.render(gridLetters[counterY], True, colors.black)
				text2.set_alpha(127)
				w, h = text2.get_size()
				self.display.blit(text2, (25, (19 + int(x + (stepWidth / 2) - (h / 2)))))
			# print first row letter
			text = font20.render('A', True, colors.black)
			text.set_alpha(127)
			w, h = text.get_size()
			self.display.blit(text, (25, 19 + int(((stepWidth + offsetY) / 2) - (h / 2))))




	def getTextObjects(self):
		""" querys server for chat and messages and updates self.chatBuffer and self.msgBuffer """
		fileUrl1 = 'gamechat?lastId=' + str(self.lastId[0])
		fileUrl2 = 'hudmsg?lastEvt=0&lastDmg=' + str(self.lastId[1])
		url1 = f"{baseUrl}/{fileUrl1}"
		url2 = f"{baseUrl}/{fileUrl2}"
		_rawChat = []
		_rawMsg = []
		try:
				reply = requests.get(url1)
				rawChat = json.loads(reply.content)
				for item in rawChat:    # fixing html error in text
						item['msg'] = item['msg'].split('<color=')[0]
						item['msg'] = item['msg'].encode("ascii", "ignore").decode()
						item['time'] = self.timeFromMapLoaded()
				_rawChat += rawChat
		except:
				pass
		try:
				reply = requests.get(url2)
				rawMsg = json.loads(reply.content)
				fMsg = rawMsg['damage']
				for item in fMsg:       # fixing html error in text
						item['msg'] = item['msg'].encode("ascii", "ignore").decode()
						item['time'] = self.timeFromMapLoaded()
				_rawMsg += fMsg
		except:
				pass
		# formating chat
		output = []
		for r in _rawChat:
			index = 55
			if len(r['msg']) > index:
				while r['msg'][index] != ' ' and index != 0:
					index -= 1
				if index == 0: index = 55
				msg1 = r['msg'][:index]
				msg2 = r['msg'][index:]
				if len(msg2) > 55:
					msg2 = msg2[:52] + '...'
				output.append([r['time'], r['sender'], msg1, r['mode']])
				output.append(['     ', ' ', '   ' + msg2[:55], r['mode']])
			else:
				output.append([r['time'], r['sender'], r['msg'], r['mode']])
		if _rawChat: self.lastId[0] = _rawChat[-1]['id']	# update lastID
		self.chatBuffer += output
		# remove messages from start, if they are part of compound messages
		if self.chatBuffer:
			counter = 0
			while self.chatBuffer[counter][0] == '     ':
				self.chatBuffer[counter][0] = '00:00'
				counter += 1
		#formating messages
		output = []
		for r in _rawMsg:
			if '(' in r['msg']:
				username, remaining = r['msg'].split(' (', 1)
				if ') ' in r['msg']:
					rawVessel, remaining = remaining.split(') ', 1)
					vessel = '(' + rawVessel + ')'
					for a in msgActions:
						if a in remaining:
							action = a
							remaining = (remaining.split(a)[1]).strip()
					if '(' in remaining:
						directObject, vessel2 = remaining.split('(', 1)
						vessel2 = '(' + vessel2
					else:
						vessel2 = ''
						directObject = remaining
					if args.debug and action == '': print('MISING (in) ACTION:', directObject)												# DEBUG / DEV
				if len(r['msg']) > 75:
					output.append([r['time'], username, vessel, action, '', ''])
					output.append(['', '', '', '', directObject.strip(), vessel2])
				else:
					output.append([r['time'], username, vessel, action, directObject.strip(), vessel2])
			else:
				# service message from the server, ignored
				pass
		self.msgBuffer += output
		if _rawMsg: self.lastId[1] = _rawMsg[-1]['id']
		# trim both buffers
		self.chatBuffer = self.chatBuffer[-16:]
		self.msgBuffer = self.msgBuffer[-16:]
		return True



	def writeMsg(self):
		""" writes all strings from buffer in lower window """
		yPos = 547
		pygame.draw.rect(self.display, colors.darkGrey, (1048, 538, 860, 493))	# background
		for entry in self.msgBuffer:
			if currentUser:
				if entry[1] == currentUser:	userNameColor = colors.cyan
				else: 						userNameColor = colors.orange
				if entry[4] == currentUser:	remColor = colors.cyan
				else: 						remColor = colors.grey
			text1 = font20.render(entry[0], True, colors.red, colors.darkGrey)
			text2 = font20.render(entry[1],	True, userNameColor, colors.darkGrey)
			text3 = font20.render(entry[2],	True, colors.green, colors.darkGrey)
			text4 = font20.render(entry[3],	True, (255, 0, 255), colors.darkGrey)
			text5 = font20.render(entry[4],	True, remColor, colors.darkGrey)
			text6 = font20.render(entry[5],	True, colors.green, colors.darkGrey)
			textRect1 = text1.get_rect()
			textRect2 = text2.get_rect()
			textRect3 = text3.get_rect()
			textRect4 = text4.get_rect()
			textRect5 = text5.get_rect()
			textRect6 = text6.get_rect()
			textRect1.topleft = (1058, yPos)
			textRect2.topleft = (1120, yPos)
			textRect3.topleft = (1128 + textRect2.w, yPos)
			textRect4.topleft = (1138 + textRect2.w + textRect3.w, yPos)
			textRect5.topleft = (1148 + textRect2.w + textRect3.w + textRect4.w, yPos)
			textRect6.topleft = (1155 + textRect2.w + textRect3.w + textRect4.w + textRect5.w, yPos)
			if entry[0] != '00:00':
				self.display.blit(text1, textRect1)
				self.display.blit(text2, textRect2)
				self.display.blit(text3, textRect3)
				self.display.blit(text4, textRect4)
				self.display.blit(text5, textRect5)
				self.display.blit(text6, textRect6)
				yPos += 30
		return True



	def writeChat(self):
		""" writes all strings from buffer in upper window """
		yPos = 25
		pygame.draw.rect(self.display, colors.darkGrey, (1048, 19,  860, 493))	# background
		for time, sender, message, mode in self.chatBuffer:
			if mode == "Team": txtColor = colors.grey
			elif mode == "Squad": txtColor = colors.green
			else: txtColor = colors.blue
			if currentUser:
				if sender == currentUser:	userNameColor = colors.cyan
				else: 							userNameColor = colors.orange
			text1 = font20.render(time, True, colors.red, colors.darkGrey)
			text2 = font20.render(sender + ':', True, userNameColor, colors.darkGrey)
			text3 = font20.render(message, True, txtColor, colors.darkGrey)
			textRect1 = text1.get_rect()
			textRect2 = text2.get_rect()
			textRect3 = text3.get_rect()
			textRect1.topleft = (1058, yPos)
			textRect2.topleft = (1120, yPos)
			textRect3.topleft = (1128 + textRect2.w, yPos)
			if time != '00:00':
				self.display.blit(text1, textRect1)
				self.display.blit(text2, textRect2)
				self.display.blit(text3, textRect3)
				yPos += 30
		return True



	def timeFromMapLoaded(self):
		""" returns a texstring of minutes and seconds from when map was loaded """
		timePassed = time.time() - self.timeMapLoaded
		mins = str(timePassed / 60).split('.')[0]
		secs = str(timePassed % 60).split('.')[0]
		minsPad = mins if len(mins) > 1 else '0' + mins
		secsPad = secs if len(secs) > 1 else '0' + secs
		return minsPad + ':' + secsPad



	def calculateZoom(self):
		""" calculates and returns coordinates / height/width for the area to zoom to """
		allCoordinates = [[],[]]
		for item in self.drawList:
			if 0 < item.xPos < 1011:
				allCoordinates[0].append(item.xPos)
			if 0 < item.yPos < 1011:
				allCoordinates[1].append(item.yPos)
		if allCoordinates[0]:
			coords = [min(allCoordinates[0]), min(allCoordinates[1]), max(allCoordinates[0]), max(allCoordinates[1])]
			# adjusting values
			height = coords[3] - coords[1] + 50
			width = coords[2] - coords[0] + 50
			coords[0] -= 10
			coords[1] -= 10
			# make area square
			if width > height:
				coords[1] -= int((width - height) / 2)
				if coords[1] < 19: coords[1] = 19
				height = width
			elif width < height:
				coords[0] -= int((height - width) / 2)
				if coords[0] < 19: coords[0] = 19
				width = height
			height = self.mapHeight if height > self.mapHeight else height
			width = self.mapWidth if width > self.mapWidth else width
			if width + coords[0] > self.mapWidth:
				coords[0] = self.mapWidth - width
			if height + coords[1] > self.mapHeight:
				coords[1] = self.mapHeight - height
			# checking values do not exceed existing map size
			coords[0] = 0 if coords[0] < 0 else coords[0]
			coords[1] = 0 if coords[1] < 0 else coords[1]
			coords[2] = self.mapWidth if coords[2] > self.mapWidth else coords[2]
			return (coords[0], coords[1], height, width)
		else:
			return False

	def drawMapImage(self):
		""" querys map from server, draws main window """
#		fromUrl = requests.get(baseUrl + 'map.img', stream = True)     # fromUrl
#		decoded = io.BytesIO(fromUrl.content)
#		mapImage = pygame.image.load(decoded)
		self.prevMap = self.rawMap
		fileUrl = 'map.img'
		url = f"{baseUrl}/{fileUrl}"
		try:
			reply = requests.get(url, stream=True)
		except:
			self.rawMap = None
			return False
		self.rawMap = reply.content
		if self.rawMap == None:
			return False
		if self.rawMap != self.prevMap:		# only save and reload map if new map is found
			self.initiateNewMap()
			fromUrl = Image.open(BytesIO(self.rawMap))
			fromUrl.save('converted.gif', format='gif')
			self.pgImage = pygame.image.load('converted.gif')
			pgW, pgH = self.pgImage.get_size()
			self.scale = pgW / self.mapWidth
			# create two maps, one scaled and one zoomed, display on or the other
			self.zoomCoords = self.calculateZoom()
			self.mapScaled = pygame.transform.scale(self.pgImage, (self.mapWidth, self.mapWidth))
			_cutOut = self.pgImage.subsurface((self.zoomCoords[0] * self.scale, self.zoomCoords[1] * self.scale, self.zoomCoords[2] * self.scale, self.zoomCoords[3] * self.scale))
			self.mapZoomed = pygame.transform.scale(_cutOut, (self.mapWidth, self.mapWidth))
			self.zoomFactor = [-self.zoomCoords[0], -self.zoomCoords[1], self.mapWidth / self.zoomCoords[2]] if args.zoom else [0, 0, 1.0]
		# draw frames
		self.display.fill(colors.background)
		if args.updatezoom:
			self.zoomCoords = self.calculateZoom()
			self.mapScaled = pygame.transform.scale(self.pgImage, (self.mapWidth, self.mapWidth))
			_cutOut = self.pgImage.subsurface((self.zoomCoords[0] * self.scale, self.zoomCoords[1] * self.scale, self.zoomCoords[2] * self.scale, self.zoomCoords[3] * self.scale))
			self.mapZoomed = pygame.transform.scale(_cutOut, (self.mapWidth, self.mapWidth))
			self.zoomFactor = [-self.zoomCoords[0], -self.zoomCoords[1], self.mapWidth / self.zoomCoords[2]] if args.zoom else [0, 0, 1.0]
		if args.zoom and self.zoomCoords and self.zoomCoords != (19, 19, 1012, 1012):
			self.display.blit(self.mapZoomed, (19, 19))
		else:
			self.display.blit(self.mapScaled, (19, 19))
		return True



	def drawBorders(self):
		""" lastly drawn, adds the borders """
		pygame.draw.rect(self.display, colors.almostBlack, (16, 16, 1017, 1017), 4)							# map border
		pygame.draw.rect(self.display, colors.almostBlack, (1045, 16,  865, 498), 4)					# right upper border
		pygame.draw.rect(self.display, colors.almostBlack, (1045, 535, 865, 498), 4)						# right lower border
		# hide overflow
		pygame.draw.rect(self.display, colors.background, (0, 0, self.width, 15))							# window top
		pygame.draw.rect(self.display, colors.background, (0, 0, 15, self.height))						# window left
		pygame.draw.rect(self.display, colors.background, (0, self.height - 45, self.width, 45))			# window bottom
		pygame.draw.rect(self.display, colors.background, (self.width - 8, 0, 8, self.height))			# window right
		pygame.draw.rect(self.display, colors.background, (1035, 0, 5, self.height))						# middle
		if not args.zoom and args.showzoom:		# +/-2 on coordinates to counter rectangle line-width
			if args.updatezoom:
				self.zoomCoords = self.calculateZoom()
			pygame.draw.rect(self.display, colors.red, (self.zoomCoords[0] + 19 - 2, self.zoomCoords[1] + 19 - 2, self.zoomCoords[2] + 3, self.zoomCoords[3] + 3), 2)
		# print scale on map
		_scale = str(round(self.zoomCoords[2] / self.mapWidth, 4)) if args.zoom else '1'
		text = font20.render('scale: ' + _scale, True, colors.green)
		self.display.blit(text, (25, 1010))
		return True



	def initiateNewMap(self):
		""" called every time a new map is loaded """
		self.getMapInfo()
		self.timeMapLoaded = time.time()
		self.chatBuffer = []
		self.msgBuffer = []
		self.lastId[0] = 1



	def createMapObjects(self):
		""" Calculates players position on the map, creates obj and adds to a list """
		global zoneLetters
		self.blinkingInterval += 1
		if self.blinkingInterval == 6:
			self.blinkingInterval = 0
		self.drawList = []
		zoneLetters = ['A', 'B', 'C', 'D']
		if args.showcorners:
			self.drawList.append(MapObject(0, 0, 		(0, 255, 255), 150))
			self.drawList.append(MapObject(0, 1011, 	(0, 255, 255), 150))
			self.drawList.append(MapObject(1011, 0, 	(0, 255, 255), 150))
			self.drawList.append(MapObject(1011, 1011, 	(0, 255, 255), 150))
		for mo in self.mapObjects:
			# create list of objects, for develop
			_verified = False
			if not mo['icon'] in objTypes:
				objTypes.append(mo['icon'])
			# determine coords
			if 'x' in mo:
				xPos = int(mo['x'] * self.mapWidth)
				yPos = int(mo['y'] * self.mapHeight)
				# check coords
				if xPos < self.mapWidth and yPos < self.mapHeight and xPos >= 0 and yPos >= 0:
					_verified = True
			elif 'ex' in mo:
				xPos = int(mo['sx'] * self.mapWidth)
				yPos = int(mo['sy'] * self.mapHeight)
				# check coords
				if xPos + 60 < self.mapWidth and yPos + 60 < self.mapHeight and xPos >= 0 and yPos >= 0:
					_verified = True
			if _verified:
				# create objects
				if mo['type'] == 'airfield':
					color = tuple( mo['color[]'] )
					deltaX = mo['sx'] - mo['ex']
					deltaY = mo['sy'] - mo['ey']
					radians = math.atan2( deltaX, deltaY )
					angle = int( math.degrees(radians) )
					newObj = MapObject(xPos, yPos, color, 95, angle)
				elif mo['icon'] == 'Player':
					radians = math.atan2( mo['dx'], mo['dy'] )
					angle = int( math.degrees(radians) )
					newObj = MapObject(xPos + 10, yPos + 10, colors.white, 100, angle)
				else:
					color = tuple( mo['color[]'] ) if not mo['blink'] or self.blinkingInterval != 1 else (255,255,0)
					if mo['icon'] == 'capture_zone':
						newObj = MapObject(xPos, yPos, color, 99)
					elif mo['icon'] == 'respawn_base_bomber':
						if 'Boat' in objTypes or 'TorpedoBoat' in objTypes:
							newObj = MapObject(xPos, yPos, color, 5)
						else:
							newObj = MapObject(xPos, yPos, color, 2)
					elif mo['icon'] == 'respawn_base_fighter':
						if 'Boat' in objTypes or 'TorpedoBoat' in objTypes:
							newObj = MapObject(xPos, yPos, color, 6)
						else:
							newObj = MapObject(xPos, yPos, color, 3)
					elif mo['icon'] == 'respawn_base_tank':	newObj = MapObject(xPos, yPos, color, 4)
					elif mo['icon'] == 'SPAA':				newObj = MapObject(xPos, yPos, color, 7)
					elif mo['icon'] == 'Fighter':			newObj = MapObject(xPos, yPos, color, 8)
					elif mo['icon'] == 'Assault':			newObj = MapObject(xPos, yPos, color, 9)
					elif mo['icon'] == 'Bomber':			newObj = MapObject(xPos, yPos, color, 10)
					elif mo['icon'] == 'Airdefence':		newObj = MapObject(xPos, yPos, color, 11)
					elif mo['icon'] == 'LightTank':			newObj = MapObject(xPos, yPos, color, 12)
					elif mo['icon'] == 'MediumTank':		newObj = MapObject(xPos, yPos, color, 13)
					elif mo['icon'] == 'HeavyTank':			newObj = MapObject(xPos, yPos, color, 14)
					elif mo['icon'] == 'TankDestroyer':		newObj = MapObject(xPos, yPos, color, 15)
					elif mo['icon'] == 'Tracked':			newObj = MapObject(xPos, yPos, color, 16)
					elif mo['icon'] == 'Wheeled':			newObj = MapObject(xPos, yPos, color, 17)
					elif mo['icon'] == 'Ship':				newObj = MapObject(xPos, yPos, color, 18)
					elif mo['icon'] == 'Boat':				newObj = MapObject(xPos, yPos, color, 19)
					elif mo['icon'] == 'TorpedoBoat':		newObj = MapObject(xPos, yPos, color, 20)
					elif mo['icon'] == 'bombing_point':		newObj = MapObject(xPos, yPos, color, 21)
					elif mo['icon'] == 'defending_point':	newObj = MapObject(xPos, yPos, color, 22)
					elif mo['icon'] == 'ground_model':		print('NOT Drawing ground_model at', xPos, yPos)	# dunno what it is?
					elif args.debug:	# unknown object, shown by a colored circle/dot
						print('Drawing unknown object:\n', mo)
						newObj = MapObject(xPos, yPos, color, 0)
				self.drawList.append(newObj)
		self.drawList.sort(key=lambda x: x.type)



	def checkKey(self):
		global correction
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_ESCAPE:
					self.running = False
				elif event.key == pygame.K_z:
					args.zoom = False if args.zoom else True
					self.zoomCoords = self.calculateZoom()
					self.zoomFactor = [-self.zoomCoords[0], -self.zoomCoords[1], self.mapWidth / self.zoomCoords[2]] if args.zoom else [0, 0, 1.0]
				# for debug
				elif event.key == pygame.K_RIGHT:
					correction[0] += 1
					print(correction)
				elif event.key == pygame.K_LEFT:
					correction[0] -= 1
					print(correction)
				elif event.key == pygame.K_UP:
					correction[1] -= 1
					print(correction)
				elif event.key == pygame.K_DOWN:
					correction[1] += 1
					print(correction)


	def loop(self):
		""" Ensure that view runs until terminated by user """
		while self.running:
			if self.getMapObjects():
				self.createMapObjects()
				self.getTextObjects()
				self.drawMapImage()
				self.drawGrid()
				for obj in self.drawList:
					obj.draw(self.display, self.zoomFactor)
				self.writeChat()
				self.writeMsg()
				self.drawBorders()
				pygame.display.update()
			else:
				_clearScreen = pygame.Surface((self.width, self.height))
				_clearScreen.fill(colors.background)
				self.display.blit(_clearScreen, (0, 0) )
				text = font30.render('Waiting for War Thunder - server to reply...', True, colors.red, colors.background)
				w, h = text.get_size()
				self.display.blit(text, (int(self.width / 2) - int(w/2), int(self.height / 3) - int(h/2) ))
				pygame.display.flip()
			self.checkKey()
		pygame.quit()
		print('\n  Program terminated by user\n')


# --- Main  ---------------------------------------------------------------------------------------

#check arguments
parser = argparse.ArgumentParser(formatter_class=lambda prog: argparse.HelpFormatter(prog,max_help_position=120))
parser.add_argument("-d", "--debug",		action="store_true",	help="Enables debugging to console")
parser.add_argument("-z", "--zoom",			action="store_true",	help="Automatically zooms to a calculated area of action")
parser.add_argument("-s", "--showzoom",		action="store_true",	help="Shows a rectangle on the area of the calculated zoom area")
parser.add_argument("-c", "--showcorners",	action="store_true",	help="Shows the four corners of draw-area (for debugging)")
parser.add_argument("-u", "--updatezoom",	action="store_true",	help="Recalculate zoom for each frame")
parser.add_argument("-k", "--keys",			action="store_true",	help="Print key usage and exit")
parser.add_argument("-v", "--version",		action="store_true",	help="Print version and exit")
parser.add_argument("--username",			nargs=1,				help="Higlight selected username in game messages")
args = parser.parse_args()
if args.version:
	sys.exit('\n  Current version is ' + version + '\n')
if args.keys:
	sys.exit('\n  <ESC>:\t\tQuit program\n  <Z>:\t\t\tZoom/unzoom to calculated area\n  <Arrow Keys>:\t\tAdjust offset of objects"\n')
currentUser = None if args.username == None else args.username[0]

colors = colorList
obj = WarThunderMap()

# --- TODO ---------------------------------------------------------------------------------------
# - ?



# --- NOTES --------------------------------------------------------------------------------------
# http://127.0.0.1:8111/gamechat?lastId=1
# http://127.0.0.1:8111/hudmsg?lastEvt=0&lastDmg=1
# http://127.0.0.1:8111/map_info.json



