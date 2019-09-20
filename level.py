from sdl2 import *
from sdl2.sdlttf import *

import ctypes
import sprite
import display
from enum import Enum


class Type(Enum):
	GENTIL = 0
	MECHANT = 1


class TerrainObject:
	def __init__(self, screen: display.Screen, filename: str, type: Type):
		self.sprite = sprite.Sprite(screen, filename)
		self.type = type


def run(screen, level):
	while start(screen, level):
		pass


def start(screen, level):
	# Init
	level_objects = []
	lines = []
	with open(f"levels/{level}.txt") as file:
		for line in file:
			lines.append(line)
	
	for i in range(len(lines)-1, -1, -1):
		for j in range(len(lines[0])-1):
			if lines[i][j] == "0":
				continue
			elif lines[i][j] == "1":
				level_objects.append(TerrainObject(screen, "ground.png", Type.GENTIL))
			elif lines[i][j] == "2":
				level_objects.append(TerrainObject(screen, "saw.png", Type.MECHANT))
			level_objects[-1].sprite.left = j * 64
			level_objects[-1].sprite.bottom = screen.size[1] - (len(lines)-1-i) * 64
	
	player = sprite.Player(screen, level_objects)
	player.bottom = screen.size[1] - 80
	player.left = 80
	
	# Game loop
	event = SDL_Event()
	while True:
		if player.is_dead:
			player = sprite.Player(screen, level_objects)
			player.bottom = screen.size[1] - 80
			player.left = 80
		while SDL_PollEvent(ctypes.byref(event)):
			if event.type == SDL_QUIT:
				TTF_Quit()
				SDL_Quit()
				quit()
			if event.type == SDL_KEYDOWN:
				if event.key.keysym.scancode == SDL_SCANCODE_ESCAPE:  # Quitter
					return False
				elif event.key.keysym.scancode == SDL_SCANCODE_R:
					return True
		
		for sp in level_objects:
			sp.sprite.tick()
		player.tick()
		
		screen.clear()
		for sp in level_objects:
			screen.copy(sp.sprite)
		screen.copy(player)
		screen.render()
