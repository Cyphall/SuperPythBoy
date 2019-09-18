from lib import *


class SpriteRaw():
	def __init__(self, screen, surface):
		self.rect = Rect(0, 0, surface.contents.w, surface.contents.h)
		self.texture = SDL_CreateTextureFromSurface(screen.renderer, surface)
	
	def tick(self):
		pass
	
	def getRect(self):
		return SDL_Rect(int(self.rect.x), int(self.rect.y), int(self.rect.w), int(self.rect.h))
	
	def getTexture(self):
		return self.texture
	
	def getLeft(self):
		return self.rect.x
	
	def getRight(self):
		return self.rect.x+self.rect.w
	
	def getTop(self):
		return self.rect.y
	
	def getBottom(self):
		return self.rect.y+self.rect.h
	
	def setLeft(self, value):
		self.rect.x = value
	
	def setRight(self, value):
		self.rect.x = value-self.rect.w
	
	def setTop(self, value):
		self.rect.y = value
	
	def setBottom(self, value):
		self.rect.y = value - self.rect.h


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
		super().__init__(screen, "player.png")
		self.space_was_pressed = False
		self.map_objects = map_objects
		self.has_gravity = True
		self.has_collision = True
		self.vector = [0, 0]
		self.is_grounded = False
		self.is_on_wall = 0
		# 0 = Non
		# 1 = Gauche
		# 2 = Droite
	
	def move(self, direction, speed):
		if (direction == "left"):
			if (self.vector[0] > -1200):
				self.vector[0] -= speed
		if (direction == "right"):
			if (self.vector[0] < 1200):
				self.vector[0] += speed
	
	def tick(self):
		if (self.has_gravity):
			self.vector[1] += 60
		
		if (self.is_grounded):
			if (self.vector[0] > 0):
				self.vector[0] -= 10
			elif (self.vector[0] < 0):
				self.vector[0] += 10
		
		inputs = SDL_GetKeyboardState(None)
		if (inputs[SDL_SCANCODE_A]):  # Gauche
			self.move("left", 70)
		if (inputs[SDL_SCANCODE_D]):  # Droite
			self.move("right", 70)
		if (inputs[SDL_SCANCODE_SPACE]):  # Espace
			if (not self.space_was_pressed):
				if (self.is_grounded):
					self.jump()
				elif (self.is_on_wall == 1):
					self.jump()
					self.vector[0] = 1200
				elif (self.is_on_wall == 2):
					self.jump()
					self.vector[0] = -1200
		
		if (self.vector[1] < 0):
			if (not inputs[SDL_SCANCODE_SPACE]):
				self.vector[1] = 0
		
		if (self.has_collision):
			collision = self.collisionDetectionX(self.vector[0] / 100)
			if (collision is not None):
				if (self.vector[0] > 0):
					self.setRight(collision.getLeft())
				else:
					self.setLeft(collision.getRight())
				self.vector[0] = 0
			else:
				self.rect.x += self.vector[0] / 100
		else:
			self.rect.x += self.vector[0] / 100
		
		if (self.has_collision):
			self.is_grounded = False
			collision = self.collisionDetectionY(self.vector[1] / 100)
			if (collision is not None):
				if (self.vector[1] > 0):
					self.setBottom(collision.getTop())
					self.is_grounded = True
				else:
					self.setTop(collision.getBottom())
				self.vector[1] = 0
			else:
				self.rect.y += self.vector[1] / 100
		else:
			self.rect.y += self.vector[1] / 100
		
		if (self.collisionDetectionX(-1)):  # Test is_on_wall gauche
			self.is_on_wall = 1
		elif (self.collisionDetectionX(1)):  # Test is_on_wall droite
			self.is_on_wall = 2
		else:
			self.is_on_wall = 0
		
		self.space_was_pressed = inputs[SDL_SCANCODE_SPACE]
	
	def jump(self):
		self.vector[1] = -1800
	
	def collisionDetectionX(self, offset):
		for obj in self.map_objects:
			if (obj == self):
				continue
			if (self.collides(obj, (offset, 0))):
				return obj
		return None
	
	def collisionDetectionY(self, offset):
		for obj in self.map_objects:
			if (obj == self):
				continue
			if (self.collides(obj, (0, offset))):
				return obj
		return None
	
	def collides(self, target, offset=(0, 0)):
		if (self.getRight()+offset[0] <= target.getLeft()):
			return False
		if (self.getLeft()+offset[0] >= target.getRight()):
			return False
		if (self.getTop()+offset[1] >= target.getBottom()):
			return False
		if (self.getBottom()+offset[1] <= target.getTop()):
			return False
		return True


class Rect():
	def __init__(self, x, y, w, h):
		self.x = x
		self.y = y
		self.w = w
		self.h = h