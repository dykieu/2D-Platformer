import pygame
import sys
import os
from os import path
from pygame.locals import*
from pygame import mixer
from gameFunc import *

def loadAnimation(path, time, folderName, frames):
	# Images for each frame
	aniData = []
	i = 0

	# grabs each image for the animation
	for frame in time:
		print (frame)
		print (time)
		# Starting file name + iteration
		aniId = folderName + str(i)
		location = os.path.join(path, aniId + '.png')
		print(aniId)
		loadAni = pygame.image.load(location)

		# Copys image under aniID name
		frames[aniId] = loadAni.copy()
		#print (location)
		# Iterates for run animation (For how many frames should be in that animation)
		for j in range(frame):
			aniData.append(aniId)
		i += 1
		print(i)

	return aniData

# Detect player movement change change
def changeAni(oldAction, frame, newAction):
	if oldAction != newAction:
		oldAction = newAction
		frame = 0
	return oldAction, frame

# Obtains map from file
def getMap(path):
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