import pygame
import sys
import os
from os import path
from pygame.locals import*
from pygame import mixer
from gameFunc import *

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