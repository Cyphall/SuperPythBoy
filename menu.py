from sdl2 import *
from sdl2.sdlttf import *

import ctypes
import sprite
import display
import level


class Menu:
	def __init__(self, screen: display.Screen):
		self.screen = screen
		self.buttons = list()
		self.cursor = sprite.Sprite(screen, "choice.png")
		self.currentChoice = 0
		self.running = True
	
	def add_button(self, button: sprite.TextSprite):
		self.buttons.append(button)
		
		total_height = 0
		for button in self.buttons:
			total_height += button.height + 20
		total_height -= 20
		
		starting_height = int(self.screen.size[1]/2 - total_height/2)
		
		for i in range(len(self.buttons)):
			self.buttons[i].top = starting_height + i*84
			self.buttons[i].left = int(self.screen.size[0]/2 - self.buttons[i].width/2)
	
	def start(self):
		event = SDL_Event()
		while self.running:
			while SDL_PollEvent(ctypes.byref(event)):
				if event.type == SDL_QUIT:
					TTF_Quit()
					SDL_Quit()
					quit()
				if event.type == SDL_KEYDOWN:
					if event.key.keysym.scancode == SDL_SCANCODE_W:
						self.currentChoice = (self.currentChoice-1) % len(self.buttons)
					elif event.key.keysym.scancode == SDL_SCANCODE_S:
						self.currentChoice = (self.currentChoice+1) % len(self.buttons)
					elif event.key.keysym.scancode == SDL_SCANCODE_SPACE:
						self.action_performed(self.buttons[self.currentChoice])
					elif event.key.keysym.scancode == SDL_SCANCODE_ESCAPE:
						self.running = False
			
			self.cursor.left = self.buttons[self.currentChoice].left - 60
			self.cursor.top = self.buttons[self.currentChoice].top
			
			self.screen.clear()
			self.screen.copy(self.cursor)
			for button in self.buttons:
				self.screen.copy(button)
			self.screen.render()
	
	def action_performed(self, source):
		pass


class MenuMain(Menu):
	def __init__(self, screen):
		super().__init__(screen)
		self.btSTART = sprite.TextSprite(screen, "upheavtt.ttf", 70, "start game", (255, 255, 255))
		self.btQUIT = sprite.TextSprite(screen, "upheavtt.ttf", 70, "quit game", (255, 255, 255))
		self.add_button(self.btSTART)
		self.add_button(self.btQUIT)
		self.start()
	
	def action_performed(self, source):
		if source == self.btSTART:
			MenuLevelSelect(self.screen)
		elif source == self.btQUIT:
			self.running = False


class MenuLevelSelect(Menu):
	def __init__(self, screen):
		super().__init__(screen)
		self.btLEVEL1 = sprite.TextSprite(screen, "upheavtt.ttf", 70, "level 1", (255, 255, 255))
		self.btLEVEL2 = sprite.TextSprite(screen, "upheavtt.ttf", 70, "level 2", (255, 255, 255))
		self.btLEVEL3 = sprite.TextSprite(screen, "upheavtt.ttf", 70, "level 3", (255, 255, 255))
		self.btLEVEL4 = sprite.TextSprite(screen, "upheavtt.ttf", 70, "level 4", (255, 255, 255))
		self.btLEVEL5 = sprite.TextSprite(screen, "upheavtt.ttf", 70, "level 5", (255, 255, 255))
		self.add_button(self.btLEVEL1)
		self.add_button(self.btLEVEL2)
		self.add_button(self.btLEVEL3)
		self.add_button(self.btLEVEL4)
		self.add_button(self.btLEVEL5)
		self.start()
	
	def action_performed(self, source):
		if source == self.btLEVEL1:
			level.run(self.screen, 1)
		elif source == self.btLEVEL2:
			level.run(self.screen, 2)
		elif source == self.btLEVEL3:
			level.run(self.screen, 3)
		elif source == self.btLEVEL4:
			level.run(self.screen, 4)
		elif source == self.btLEVEL5:
			level.run(self.screen, 5)
