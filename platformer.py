import pygame
import sys
import os
from os import path
from pygame.locals import*
from pygame import mixer
from gameFunc import *
from collision import *

# Initialize python module
pygame.init()

# Folders
mainPath = os.path.dirname(__file__)
resourcePath = os.path.join(mainPath, 'resources')
iconPath = os.path.join(resourcePath, 'icons')
charPath = os.path.join(resourcePath, 'character')
envPath = os.path.join(resourcePath, 'env')
bgPath = os.path.join(resourcePath, 'background')
soundPath = os.path.join(resourcePath, 'sound')
walkPath = os.path.join(charPath, 'walk')
idlePath = os.path.join(charPath, 'idle')

# File Names
iconFile = 'icon.png'
dirtFile = 'dirt.png'
darkDirtFile = 'dirt3.png'
grassFile = 'grass.png'
mapFile = 'map.txt'
bgFile = 'bg3.png'
bgmFile = 'bgm2.mp3'
walkFile1 = 'walk0.png'
walkFile2 = 'walk1.png'
idleFile1 = 'idle0.png'
idleFile2 = 'idle1.png'
idleFile3 = 'idle2.png'

# Grab Resources
gameIcon = pygame.image.load(os.path.join(iconPath, iconFile))
charIdle = pygame.image.load(os.path.join(idlePath, idleFile1))
grassIcon = pygame.image.load(os.path.join(envPath, grassFile))
dirtIcon = pygame.image.load(os.path.join(envPath, dirtFile))
darkDirtIcon = pygame.image.load(os.path.join(envPath, darkDirtFile))
bgIcon = pygame.image.load(os.path.join(bgPath, bgFile))
bgIcon = pygame.transform.scale(bgIcon, (1920,640))

# Game Variables
clientName = '2-D JumpQuest'
clock = pygame.time.Clock()
tileDimension = 50

# Game map
gameMap = []

# Window demnsions
winX = 1920
winY = 1080
winSize = [winX, winY]

# Window settings
pygame.display.set_caption(clientName)
pygame.display.set_icon(gameIcon)
screen = pygame.display.set_mode((winX, winY))
display = pygame.Surface(((winX/2), (winY/2)))
scroll = [0, 0]

# Character
playerStart = [700, 220]
playerGravity = 0
gravTimer = 0
jumpHeight = -6
movSpeed = 4
moveRight = False
moveLeft = False
playerRect = pygame.Rect(playerStart[0], playerStart[1], charIdle.get_width(), charIdle.get_height()) 	# rectangle used for collision
testRect = pygame.Rect(100, 700, 100, 50)

# Background music
mixer.music.load(os.path.join(soundPath, bgmFile))
mixer.music.set_volume(.1)
mixer.music.play(-1)

gameMap = getMap(os.path.join(envPath, mapFile))

# Loads all frames into a list
aniDb = {}
frames = {}
aniDb['idle'] = loadAnimation(idlePath, [17, 17, 17], 'idle', frames)
aniDb['walk'] = loadAnimation(walkPath, [10, 10], 'walk', frames)

# Char animation
playerAction = 'idle'
playerFrame = 0
dirChange = False

# Game Loops
while True:
	display.fill((0, 0, 0))
	display.blit(bgIcon, (0,0))
	tiles = []

	# Move camera with player (Centers camera on player)
	scroll[0] += (playerRect.x - scroll[0] - (winX/4))/10

	# Y camera only moves till char off map
	if scroll[1] <= winY - 720:
		scroll[1] += (playerRect.y - scroll[1] - (winY/4))/10
	
	# Prevent pixel vibration
	scrollValue = scroll.copy()
	scrollValue[0] = int(scroll[0])
	scrollValue[1] = int(scroll[1])

	# Setup game map
	yAxis = 0
	for rows in gameMap:
		xAxis = 0
		for tile in rows:
			# render dirt on display
			if tile == '1':
				display.blit(dirtIcon, (xAxis * tileDimension - scrollValue[0], yAxis * tileDimension - scrollValue[1]))
			# render grass on display
			if tile == '2':
				display.blit(grassIcon, (xAxis * tileDimension - scrollValue[0], yAxis * tileDimension - scrollValue[1]))
			if tile == '3':
					display.blit(darkDirtIcon, (xAxis * tileDimension - scrollValue[0], yAxis * tileDimension - scrollValue[1]))
			if tile != '0':
				tiles.append(pygame.Rect(xAxis * tileDimension, yAxis * tileDimension , tileDimension, tileDimension))
			xAxis += 1
		yAxis += 1

	# Character Movement & Gravity
	playerMov = [0,0]
	if moveRight == True:
		playerMov[0] += movSpeed
	
	if moveLeft == True:
		playerMov[0] -= movSpeed
	
	playerMov[1] += playerGravity
	playerGravity += .2
	
	if playerGravity > (jumpHeight + 13):
		playerGravity = (jumpHeight + 13)

	# Player image direction
	if playerMov[0] > 0:
		playerAction, playerFrame = changeAni(playerAction, playerFrame, 'walk')
		dirChange = False

	if playerMov[0] < 0:
		playerAction, playerFrame = changeAni(playerAction, playerFrame, 'walk')
		dirChange = True

	if playerMov[0] == 0:
		playerAction, playerFrame = changeAni(playerAction, playerFrame, 'idle')

	playerRect, collisions = movement(playerRect, playerMov, tiles)

	if collisions['bot'] == True:
		gravTimer = 0
		playerGravity = 0
	else:
		gravTimer += 1
	
	# Renders Character 
	playerFrame += 1											# Increments to next frame
	if playerFrame >= len(aniDb[playerAction]):					# Checks current Frame compared to limit for current animation
		playerFrame = 0											# If so, reset it (Allows for animations to loop)
	playerImg = frames[aniDb[playerAction][playerFrame]]
	display.blit(pygame.transform.flip(playerImg, dirChange, False), (playerRect.x - scrollValue[0], playerRect.y - scrollValue[1]))

	# Game Events
	for event in pygame.event.get():
		# Exit Functionality
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		# User Input
		if event.type == KEYDOWN:
			if event.key == K_RIGHT:
				moveRight = True
			if event.key == K_LEFT:
				moveLeft = True
			if event.key == K_UP:
				# Prevents double jump
				if gravTimer < (jumpHeight + 13):
					playerGravity = jumpHeight
		if event.type == KEYUP:
			if event.key == K_RIGHT:
				moveRight = False
			if event.key == K_LEFT:
				moveLeft = False
	# If player falls
	if playerRect.y > winY:
		playerRect.y = playerStart[1]
		playerRect.x = playerStart[0]
		scroll = [0, 0]

	screen.blit(pygame.transform.scale(display, winSize), (0,0))	# Scaling display to screen (surface, window size) to 0,0
	pygame.display.update()
	clock.tick(60) 													# Pauses script until 60 fps