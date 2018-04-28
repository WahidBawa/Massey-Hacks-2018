# main.py
from pygame import *
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
init()
width, height = size = (display.Info().current_w, display.Info().current_h)
screen = display.set_mode(size, FULLSCREEN)
running = True

def load_images():
	global images
	images = {}
	# images["player1"] = image.load("Sprites/")

class Player(sprite.Sprite):
	def __init__(self):
		sprite.Sprite.__init__(self)
		self.image = images["player1"]
		self.rect = self.image.get_rect()
		self.rect.center = width/2, height/2

while running:
	for evt in event.get():
		if evt.type == QUIT:
			running = False
		if evt.type == KEYDOWN:
			if evt.key == K_ESCAPE:
				running = False
	mx,my = mouse.get_pos()
	mb = mouse.get_pressed()

	screen.fill(WHITE)

	display.flip()
quit()
