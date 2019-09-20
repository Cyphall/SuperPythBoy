from sdl2 import *

import time


class Screen:
	def __init__(self, title, pos, size, wflags, rflags):
		self.window = SDL_CreateWindow(title.encode(), *pos, *size, wflags)
		self.renderer = SDL_CreateRenderer(self.window, -1, rflags)
		self.clearColor = (0, 0, 0)
		self._size = size
		self.timeAtLastTick = 0
	
	def copy(self, sprite):
		SDL_RenderCopy(self.renderer, sprite.texture, None, sprite.sdl_rect)
	
	def render(self):
		waitUntil = self.timeAtLastTick + 1000000000 / 60
		while time.perf_counter_ns() < waitUntil:
			pass
		self.timeAtLastTick = time.perf_counter_ns()
		SDL_RenderPresent(self.renderer)
	
	def clear(self):
		SDL_SetRenderDrawColor(self.renderer, *self.clearColor, 255)
		SDL_RenderClear(self.renderer)
	
	def set_clear_color(self, color):
		self.clearColor = color
	
	@property
	def size(self):
		return self._size
