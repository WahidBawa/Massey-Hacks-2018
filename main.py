# main.py
from pygame import *
from math import *
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
init()
width, height = size = (display.Info().current_w, display.Info().current_h)
screen = display.set_mode(size, FULLSCREEN)
running = True

f = font.SysFont("Times New Roman", 20)

def load_images():
	global images
	images = {}
	images["player1"] = image.load("Sprites/PNG/Man Blue/manBlue_stand.png")

load_images()

class Player(sprite.Sprite):
	def __init__(self):
		sprite.Sprite.__init__(self)
		all_sprites.add(self)
		self.real_image = images["player1"]
		self.ang = 0
		self.image = self.real_image
		self.rect = self.image.get_rect()
		self.rect.center = width/2, height/2

	def update(self):
		self.ang = atan2(height/2 - my, width/2 - mx)
		print(self.ang)
		self.image = transform.rotate(self.real_image, 180-degrees(self.ang))
		self.rect = self.image.get_rect()
		self.rect.center = width/2, height/2

all_sprites = sprite.Group()
player = Player()

while running:
	for evt in event.get():
		if evt.type == QUIT:
			running = False
		if evt.type == KEYDOWN:
			if evt.key == K_ESCAPE:
				running = False
	mx, my = mouse.get_pos()
	mb = mouse.get_pressed()

	screen.fill(WHITE)

	player.update()
	# for s in all_sprites:
	# 	s.update()

	all_sprites.draw(screen)

	screen.blit(f.render(str(player.ang), True, BLACK), (0, 0))
	display.flip()
quit()
