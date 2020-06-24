import pygame
import sys
import os
from os import path
from pygame.locals import*
from pygame import mixer

# Initialize python module
pygame.init()

# Folders
mainPath = os.path.dirname(__file__)
resourcePath = os.path.join(mainPath, 'resources')
iconPath = os.path.join(resourcePath, 'icons')
charPath = os.path.join(resourcePath, 'character')
envPath = os.path.join(resourcePath, 'env')

# File Names
iconFile = 'icon.png'
charIdleFile = 'model.png'
dirtFile = 'dirt.png'
grassFile = 'grass.png'
mapFile = 'map.txt'

# Grab Resources
gameIcon = pygame.image.load(os.path.join(iconPath, iconFile))
charIdle = pygame.image.load(os.path.join(charPath, charIdleFile))
grassIcon = pygame.image.load(os.path.join(envPath, grassFile))
dirtIcon = pygame.image.load(os.path.join(envPath, dirtFile))

# Game Variables
clientName = '2-D platformer'
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
scrollValue = [0, 0]

# Character
playerStart = [0, 220]
playerGravity = 0
gravTimer = 0
jumpHeight = -6
movSpeed = 4
moveRight = False
moveLeft = False
playerRect = pygame.Rect(playerStart[0], playerStart[1], charIdle.get_width() - 50, charIdle.get_height()) 	# rectangle used for collision
testRect = pygame.Rect(100, 700, 100, 50)

def getMap(path):
	print (path)
	# Opens file grabs data and then splits on every newline
	openFile = open(path, 'r')
	data = openFile.read()
	openFile.close()
	data = data.split('\n')
	temp = []
	# convert each line into a list
	for line in data:
		temp.append(list(line))
	return temp

gameMap = getMap(os.path.join(envPath, mapFile))

# Collision Function
def collision (rectObj, tiles):
	collided = []

	# Iterates through all tiles and tests if obj collided with it
	for tile in tiles:
		if rectObj.colliderect(tile):
			collided.append(tile)
	return collided

# Movement Function (Whats moving, how many moves, on what)
def movement (rectObj, move, tiles):
	collisionTypes = {
		'top': False,
		'bot': False,
		'right': False,
		'left': False
	}

	# Make x movement and test for collision
	rectObj.x += move[0]
	collided = collision(rectObj, tiles)

	for tile in collided:
		# Test positive x movement collision
		if move[0] > 0:
			rectObj.right = tile.left
			collisionTypes['right'] = True
		# Test negative x movement collision
		elif move[0] < 0:
			rectObj.left = tile.right
			collisionTypes['left'] = True
	
	# Make y movement and test for collision
	rectObj.y += move[1]
	collided = collision(rectObj, tiles)

	for tile in collided:
		# test bottom collision
		if move[1] > 0:
			rectObj.bottom = tile.top
			collisionTypes['bot'] = True
		# test top collision
		elif move[1] < 0:
			rectObj.top = tile.bottom
			collisionTypes['top'] = True
	return rectObj, collisionTypes



# Game Loops
while True:
	display.fill((0, 0, 0))
	tiles = []

	# Move camera with player (Centers camera on player)
	scrollValue[0] += (playerRect.x - scrollValue[0] - (winX/4))
	scrollValue[1] += (playerRect.y - scrollValue[1] - (winY/4))
	
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

	playerRect, collisions = movement(playerRect, playerMov, tiles)

	if collisions['bot'] == True:
		gravTimer = 0
		playerGravity = 0
	else:
		gravTimer += 1
	
	# Renders Character 
	display.blit(charIdle, (playerRect.x - scrollValue[0], playerRect.y - scrollValue[1]))

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

	screen.blit(pygame.transform.scale(display, winSize), (0,0))	# Scaling display to screen (surface, window size) to 0,0
	pygame.display.update()
	clock.tick(60) 													# Pauses script until 60 fps