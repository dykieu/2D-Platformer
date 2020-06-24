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

# File Names
iconFile = 'icon.png'
charIdleFile = 'charIdle.png'

# Game Variables
clientName = '2-D platformer'
clock = pygame.time.Clock()
moveRight = False
moveLeft = False

# Window demnsions
winX = 1920
winY = 1080

# Window settings
pygame.display.set_caption(clientName)
gameIcon = pygame.image.load(os.path.join(iconPath, iconFile))
pygame.display.set_icon(gameIcon)
screen = pygame.display.set_mode((winX, winY))

# Character
charIdle = pygame.image.load(os.path.join(charPath, charIdleFile))


# Game Loops
while True:
	for event in pygame.event.get():
		# Exit Functionality
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		# Movement
		if event.type == K_DOWN:
			if event.key == K_RIGHT:
				moveRight = True
			if event.key == K_LEFT:
				moveLeft = False
		if event.type == K_UP:
			if event.key == K_RIGHT:
				moveRight = False
			if event.key == K_LEFT:
				moveLeft = False
	screen.blit(charIdle, (-100, 440))

	pygame.display.update()
	
	# Pauses script until 60 fps
	clock.tick(60)