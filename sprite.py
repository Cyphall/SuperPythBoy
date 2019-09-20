from sdl2 import *
from sdl2.sdlttf import *
from sdl2.sdlimage import *

import level


class SpriteRaw:
	def __init__(self, screen, surface):
		self._rect = Rect(0, 0, surface.contents.w, surface.contents.h)
		self._texture = SDL_CreateTextureFromSurface(screen.renderer, surface)
	
	def tick(self):
		pass
	
	@property
	def sdl_rect(self):
		return SDL_Rect(int(self._rect.x), int(self._rect.y), int(self._rect.w), int(self._rect.h))
	
	@property
	def texture(self):
		return self._texture
	
	@property
	def left(self):
		return self._rect.x
	
	@left.setter
	def left(self, value):
		self._rect.x = value
	
	@property
	def right(self):
		return self._rect.x + self._rect.w
	
	@right.setter
	def right(self, value):
		self._rect.x = value - self._rect.w
	
	@property
	def top(self):
		return self._rect.y
	
	@top.setter
	def top(self, value):
		self._rect.y = value
	
	@property
	def bottom(self):
		return self._rect.y + self._rect.h
	
	@bottom.setter
	def bottom(self, value):
		self._rect.y = value - self._rect.h
	
	@property
	def width(self):
		return self._rect.w
	
	@property
	def height(self):
		return self._rect.h


class Sprite(SpriteRaw):
	def __init__(self, screen, filename):
		surface = IMG_Load(("resources/" + filename).encode())
		super().__init__(screen, surface)
		SDL_FreeSurface(surface)


class TextSprite(SpriteRaw):
	def __init__(self, screen, font_family, font_size, string, color):
		font = TTF_OpenFont(("resources/" + font_family).encode(), font_size)
		surface = TTF_RenderText_Solid(font, string.encode(), SDL_Color(*color))
		super().__init__(screen, surface)
		TTF_CloseFont(font)
		SDL_FreeSurface(surface)


class Player(Sprite):
	def __init__(self, screen, map_objects):
		super().__init__(screen, "player2.png")
		self.space_was_pressed = False
		self.map_objects = map_objects
		self.has_gravity = True
		self.has_collision = True
		self.vector = [0, 0]
		self.is_grounded = False
		self.is_on_wall = 0
		self.flying_since = 0
		self.is_dead = False
	
	# 0 = Non
	# 1 = Gauche
	# 2 = Droite
	
	def move(self, direction, speed):
		if direction == "left":
			if self.vector[0] > -1200:
				self.vector[0] -= speed
		if direction == "right":
			if self.vector[0] < 1200:
				self.vector[0] += speed
	
	def tick(self):
		if self.has_gravity:
			self.vector[1] += 60
		
		if self.is_grounded:
			self.flying_since = 0
			if self.vector[0] > 0:
				self.vector[0] -= 10
			elif self.vector[0] < 0:
				self.vector[0] += 10
		
		inputs = SDL_GetKeyboardState(None)
		if inputs[SDL_SCANCODE_A]:  # Gauche
			self.move("left", 70)
		elif inputs[SDL_SCANCODE_D]:  # Droite
			self.move("right", 70)
		else:
			if self.is_grounded:
				self.vector[0] = 0
		if inputs[SDL_SCANCODE_SPACE]:  # Espace
			if not self.space_was_pressed:
				if self.flying_since < 5:
					self.jump()
					self.flying_since = 5
				elif self.is_on_wall == 1:
					self.jump()
					self.vector[0] = 1200
				elif self.is_on_wall == 2:
					self.jump()
					self.vector[0] = -1200
		
		if self.vector[1] < 0:
			if not inputs[SDL_SCANCODE_SPACE]:
				self.vector[1] = 0
		
		if self.has_collision:
			collision = self.collision_detection_x(self.vector[0] / 100)
			if collision is not None:
				if collision.type == level.Type.MECHANT:
					self.is_dead = True
				if self.vector[0] > 0:
					self.right = collision.sprite.left
				else:
					self.left = collision.sprite.right
				self.vector[0] = 0
			else:
				self.left += self.vector[0] / 100
		else:
			self.left += self.vector[0] / 100
		
		if self.has_collision:
			self.is_grounded = False
			collision = self.collision_detection_y(self.vector[1] / 100)
			if collision is not None:
				if collision.type == level.Type.MECHANT:
					self.is_dead = True
				if self.vector[1] > 0:
					self.bottom = collision.sprite.top
					self.is_grounded = True
				else:
					self.top = collision.sprite.bottom
				self.vector[1] = 0
			else:
				self.top += self.vector[1] / 100
		else:
			self.top += self.vector[1] / 100
		
		if self.collision_detection_x(-1):  # Test is_on_wall gauche
			self.is_on_wall = 1
		elif self.collision_detection_x(1):  # Test is_on_wall droite
			self.is_on_wall = 2
		else:
			self.is_on_wall = 0
		
		self.flying_since += 1
		
		self.space_was_pressed = inputs[SDL_SCANCODE_SPACE]
	
	def jump(self):
		self.vector[1] = -1800
	
	def collision_detection_x(self, offset):
		for obj in self.map_objects:
			if obj.sprite == self or obj.type == level.Type.MECHANT:
				continue
			if self.collides(obj, (offset, 0)):
				return obj
		for obj in self.map_objects:
			if obj.sprite == self or obj.type == level.Type.GENTIL:
				continue
			if self.collides(obj, (offset, 0)):
				return obj
		return None
	
	def collision_detection_y(self, offset):
		for obj in self.map_objects:
			if obj.sprite == self or obj.type == level.Type.MECHANT:
				continue
			if self.collides(obj, (0, offset)):
				return obj
		for obj in self.map_objects:
			if obj.sprite == self or obj.type == level.Type.GENTIL:
				continue
			if self.collides(obj, (0, offset)):
				return obj
		return None
	
	def collides(self, target, offset=(0, 0)):
		if self.right + offset[0] <= target.sprite.left:
			return False
		if self.left + offset[0] >= target.sprite.right:
			return False
		if self.top + offset[1] >= target.sprite.bottom:
			return False
		if self.bottom + offset[1] <= target.sprite.top:
			return False
		return True


class Rect:
	def __init__(self, x, y, w, h):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
