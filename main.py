# main.py
from pygame import *
init()
screen = display.set_mode((display.Info().current_w, display.Info().current_h), FULLSCREEN)
running = True

def load_images():
	global images
	images = {}
	images["player1"] = image.load("Sprites/")
while running:
	for evt in event.get():
		if evt.type == QUIT:
			running = False
		if evt.type == KEYDOWN:
			if evt.key == K_ESCAPE:
				running = False
	mx,my = mouse.get_pos()
	mb = mouse.get_pressed()

	display.flip()
quit()
