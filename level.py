import ctypes
from lib import *


def run(screen, level):
	# Init
	levelObjects = list()
	player = sprite.Player(screen, levelObjects)
	player.setBottom(900 - 100)
	for i in range(10):
		levelObjects.append(sprite.Sprite(screen, "test.png"))
		levelObjects[-1].setTop(900-64)
		levelObjects[-1].setLeft(64*i)
	for i in range(2, 10):
		levelObjects.append(sprite.Sprite(screen, "test.png"))
		levelObjects[-1].setTop(900 - 64*i)
		levelObjects[-1].setLeft(64 * 9)
	
	# Game loop
	running = True
	event = SDL_Event()
	while running:
		while (SDL_PollEvent(ctypes.byref(event))):
			if (event.type == SDL_QUIT):
				TTF_Quit()
				SDL_Quit()
				quit()
			if (event.type == SDL_KEYDOWN):
				if (event.key.keysym.scancode == SDL_SCANCODE_ESCAPE):  # Quitter
					running = False
		
		for sp in levelObjects:
			sp.tick()
		player.tick()
		
		screen.clear()
		for sp in levelObjects:
			screen.copy(sp)
		screen.copy(player)
		screen.render()