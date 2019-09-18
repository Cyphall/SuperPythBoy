from lib import *


class Screen():
	def __init__(self, title, pos, size, wflags, rflags):
		self.window = SDL_CreateWindow(title.encode(), *pos, *size, wflags)
		self.renderer = SDL_CreateRenderer(self.window, -1, rflags)
		self.clearColor = (0, 0, 0)
	
	def copy(self, sprite):
		SDL_RenderCopy(self.renderer, sprite.texture, None, sprite.getRect())
	
	def render(self):
		SDL_RenderPresent(self.renderer)
	
	def clear(self):
		SDL_SetRenderDrawColor(self.renderer, *self.clearColor, 255)
		SDL_RenderClear(self.renderer)
	
	def setClearColor(self, color):
		self.clearColor = color