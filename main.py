import threading, itertools
from pygame import *
from math import *
from random import *
from pytmx import *
from randomize import *
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
init()
myClock = time.Clock()
width, height = size = (min(1920,display.Info().current_w), min(1080,display.Info().current_h))
screen = display.set_mode(size, FULLSCREEN)
running = True
fname = load_pygame("Maps/64.tmx")
f = font.SysFont("Times New Roman", 20)
def MapLoad(Map_Name):
	for layer in Map_Name.visible_layers:
		if isinstance(layer, TiledTileLayer):
			for x, y, gid in layer:
				tile = Map_Name.get_tile_image_by_gid(gid)
				if tile:
					screen.blit(tile, ((x * Map_Name.tilewidth), (y * Map_Name.tileheight)))

def load_images():
	global images
	images = {}
	images["player1"] = image.load("Sprites/PNG/Hitman 1/hitman1_machine.png")
	images["bullet"] = image.load("Sprites/PNG/weapon_gun.png")
	images["enemy"] = image.load("Sprites/PNG/Zombie 1/zoimbie1_hold.png")

ani_pics = []
for i in range(445):
	ani_pics.append(image.load("loading/frame_%03d_delay-0.02s.png" % i))
def loading_animation(delay):
	for c in itertools.cycle(ani_pics):
		if loading_images_done:
			break
		screen.fill(WHITE)
		tmpRect = c.get_rect()
		tmpRect.center = width/2, height/2
		screen.blit(c, tmpRect)
		display.flip()
		time.wait(delay)

def do_loading(target, args=[]):
	global loading_images_done
	loading_images_done = False
	l = threading.Thread(target=target, args=args)
	l.start()
	t = threading.Thread(target=loading_animation, args=[1])
	t.start()

	while not loading_images_done:
		if not l.isAlive():
			loading_images_done = True

do_loading(load_images)

weapons = {"machine gun": 5, "shotgun": 40}

class Player(sprite.Sprite):
	def __init__(self):
		sprite.Sprite.__init__(self)
		all_sprites.add(self)
		self.health = 100
		self.real_image = images["player1"]
		self.ang = 0
		self.image = self.real_image
		self.rect = self.image.get_rect()
		self.rect.center = width/2, height/2

		self.weapon = "machine gun"
		self.bullet_counter = weapons[self.weapon]

	def update(self):
		self.ang = atan2(height/2 - my, width/2 - mx)
		self.image = transform.rotate(self.real_image, 180-degrees(self.ang))
		self.rect = self.image.get_rect()
		self.rect.center = width/2, height/2
		for i in sprite.spritecollide(self, enemies, False):
			self.health -= 0.2

	def shoot_bullet(self):
		self.bullet_counter += 1
		if self.bullet_counter > weapons[self.weapon]:
			self.bullet_counter = 0
			if self.weapon == "machine gun":
				Bullet(self.rect.centerx, self.rect.centery, self.ang+radians(randint(-5,5)))
			elif self.weapon == "shotgun":
				for i in range(5):
					Bullet(self.rect.centerx, self.rect.centery, self.ang+radians(randint(-20,20)))
	def switch_weapon(self):
		l = list(weapons)
		self.weapon = l[len(weapons)-1 - l.index(self.weapon)]

class Bullet(sprite.Sprite):
	def __init__(self, x, y, ang):
		sprite.Sprite.__init__(self)
		all_sprites.add(self)
		bullets.add(self)
		self.real_image = images["bullet"]
		self.rect = self.real_image.get_rect()
		self.x, self.y = x, y
		self.rect.center = self.x, self.y
		self.ang = ang

	def update(self):
		SPEED = 10
		self.x -= SPEED*cos(self.ang)
		self.y -= SPEED*sin(self.ang)
		self.rect.center = self.x, self.y
		self.image = transform.rotate(self.real_image, 180-degrees(self.ang))
		if self.rect.right < 0 or self.rect.left > width or self.rect.top < 0 or self.rect.bottom > height:
			self.kill()

class Enemy(sprite.Sprite):
	def __init__(self):
		sprite.Sprite.__init__(self)
		all_sprites.add(self)
		enemies.add(self)
		self.SPEED = randint(10,30)/10
		self.real_image = images["enemy"]
		self.x, self.y = self.get_rand_pos()
		self.image = self.real_image
		self.rect = self.image.get_rect()
		self.x, self.y = self.get_rand_pos()
		self.rect.center = self.x, self.y
		self.ang = self.get_ang()

	def get_rand_pos(self):
		x, y = 0, 0
		while True:
			x, y = randint(0,width), randint(0,height)
			dist = hypot(player.rect.centerx-x, player.rect.centery-y)
			if dist > 500:
				return x, y

	def get_ang(self):
		return atan2(player.rect.centery-self.y, player.rect.centerx-self.x)

	def update(self):
		self.ang = self.get_ang()
		self.x += self.SPEED * cos(self.ang)
		self.y += self.SPEED * sin(self.ang)
		self.rect.center = self.x, self.y
		self.image = transform.rotate(self.real_image, 360-degrees(self.ang))

score = 0
all_sprites = sprite.Group()
bullets = sprite.Group()
enemies = sprite.Group()

player = Player()

while running:
	for evt in event.get():
		if evt.type == QUIT:
			running = False
		if evt.type == KEYDOWN:
			if evt.key == K_ESCAPE:
				running = False

			if evt.key == K_s:
				player.switch_weapon()
	mx, my = mouse.get_pos()
	mb = mouse.get_pressed()
	kp = key.get_pressed()

	screen.fill(WHITE)
	MapLoad(fname)

	while (len(enemies) < 2):
		Enemy()
	if kp[K_SPACE]:
		player.shoot_bullet()

	for s in all_sprites:
		s.update()

	hits = sprite.groupcollide(enemies, bullets, True, True)
	if hits:
		score += 1

	all_sprites.draw(screen)
	screen.blit(f.render(str(score), True, BLACK), (0, 0))
	draw.rect(screen, BLACK, (98, 10, 204, 40), 4)
	draw.rect(screen, GREEN, (100, 12, int(player.health*2), 36))
	display.flip()
	myClock.tick(60)
quit()
