import ctypes
from lib import *


class Menu():
	def __init__(self, screen):
		self.screen = screen
		self.widgets = list()
		self.cursor = sprite.Sprite(screen, "choice.png")
		self.currentChoice = 0
		self.maxChoice = -1
		self.running = True
	
	def addButton(self, button):
		if (self.maxChoice < 0):
			button.setLeft(200)
			button.setTop(100)
		else:
			button.setLeft(200)
			button.setTop(self.widgets[-1].getTop() + 64)
		self.maxChoice += 1
		
		self.widgets.append(button)
	
	def start(self):
		self.cursor.setLeft(self.widgets[0].getLeft() - 60)
		self.cursor.setTop(self.widgets[0].getTop() + self.currentChoice * 64)
		event = SDL_Event()
		while (self.running):
			while (SDL_PollEvent(ctypes.byref(event))):
				if (event.type == SDL_QUIT):
					TTF_Quit()
					SDL_Quit()
					quit()
				if (event.type == SDL_KEYDOWN):
					if (event.key.keysym.scancode == SDL_SCANCODE_W):
						self.currentChoice -= 1
						if (self.currentChoice < 0):
							self.currentChoice = self.maxChoice
					elif (event.key.keysym.scancode == SDL_SCANCODE_S):
						self.currentChoice += 1
						if (self.currentChoice > self.maxChoice):
							self.currentChoice = 0
					elif (event.key.keysym.scancode == SDL_SCANCODE_SPACE):
						self.actionPerformed(self.widgets[self.currentChoice])
					elif (event.key.keysym.scancode == SDL_SCANCODE_ESCAPE):
						self.running = False
			
			self.cursor.setTop(100 + self.currentChoice * 64)
			
			self.screen.clear()
			self.screen.copy(self.cursor)
			for wid in self.widgets:
				self.screen.copy(wid)
			self.screen.render()
	
	def actionPerformed(self, source):
		pass


class MenuMain(Menu):
	def __init__(self, screen):
		super().__init__(screen)
		self.btSTART = sprite.TextSprite(screen, "upheavtt.ttf", 70, "start game", (255, 255, 255))
		self.btQUIT = sprite.TextSprite(screen, "upheavtt.ttf", 70, "quit game", (255, 255, 255))
		self.addButton(self.btSTART)
		self.addButton(self.btQUIT)
		self.start()
	
	def actionPerformed(self, source):
		if (source == self.btSTART):
			MenuLevelSelect(self.screen)
		elif (source == self.btQUIT):
			self.running = False


class MenuLevelSelect(Menu):
	def __init__(self, screen):
		super().__init__(screen)
		self.btLEVEL1 = sprite.TextSprite(screen, "upheavtt.ttf", 70, "level 1", (255, 255, 255))
		self.btLEVEL2 = sprite.TextSprite(screen, "upheavtt.ttf", 70, "level 2", (255, 255, 255))
		self.btLEVEL3 = sprite.TextSprite(screen, "upheavtt.ttf", 70, "level 3", (255, 255, 255))
		self.btLEVEL4 = sprite.TextSprite(screen, "upheavtt.ttf", 70, "level 4", (255, 255, 255))
		self.btLEVEL5 = sprite.TextSprite(screen, "upheavtt.ttf", 70, "level 5", (255, 255, 255))
		self.addButton(self.btLEVEL1)
		self.addButton(self.btLEVEL2)
		self.addButton(self.btLEVEL3)
		self.addButton(self.btLEVEL4)
		self.addButton(self.btLEVEL5)
		self.start()
	
	def actionPerformed(self, source):
		if (source == self.btLEVEL1):
			level.run(self.screen, 1)
		elif (source == self.btLEVEL2):
			level.run(self.screen, 2)
		elif (source == self.btLEVEL3):
			level.run(self.screen, 3)
		elif (source == self.btLEVEL4):
			level.run(self.screen, 4)
		elif (source == self.btLEVEL5):
			level.run(self.screen, 5)