import threading, itertools, serial
from pygame import *
from math import *
from random import *
from pytmx import *
from real_shit import *
import pickle as p

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

init()
mixer.pre_init(44100,-16,1,512)
mixer.init()
mixer.music.load("music/music.ogg")#loads the song
mixer.music.play(-1)
# try:
ser = serial.Serial('COM9', 9600)
# except: pass
width, height = size = (min(1920,display.Info().current_w), min(1080,display.Info().current_h))
screen = display.set_mode(size, FULLSCREEN)
running = True
myClock = time.Clock()
fname = load_pygame("Maps/64.tmx")
# f = font.SysFont("Times New Roman", 20)
f1 = font.Font("Font/TheGodfather-v2.ttf", 250)
f2 = font.Font("Font/TheGodfather-v2.ttf", 115)
mode = 'menu'
energy = 100
def randomize():
	global fname
	make_new_random_thing()
	fname = load_pygame("Maps/64.tmx")

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
	images["enemy1"] = image.load("Sprites/PNG/Man Blue/manBlue_hold.png")
	images["enemy2"] = image.load("Sprites/PNG/Man Brown/manBrown_hold.png")
	images["enemy3"] = image.load("Sprites/PNG/Man Old/manOld_hold.png")
	images["enemy4"] = image.load("Sprites/PNG/Soldier 1/soldier1_hold.png")
	images["enemy5"] = image.load("Sprites/PNG/Survivor 1/survivor1_hold.png")
	images["back"] = transform.scale(image.load("Sprites/menu/back.jpg").convert_alpha(), (width, height))

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

def load():
	HighScore = p.load(open("HighScore.dat", 'rb'))
	return HighScore
def save():
	p.dump(HighScore, open("HighScore.dat", "wb"))	
HighScore = load()
weapons = {"machine gun": 5, "shotgun": 40}

class Player(sprite.Sprite):
	def __init__(self):
		sprite.Sprite.__init__(self)
		all_sprites.add(self)
		self.health = 100
		self.inPosition = False
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
		self.real_image = images["enemy%d"%randint(1,5)]
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
				save()

			if evt.key == K_s:
				player.switch_weapon()
			if evt.key == K_q:
				randomize()	
				MapLoad(load_pygame("Maps/64.tmx"))
			if evt.key == K_r:
				randomize()
			if evt.key == K_y:
				score += 39
		if evt.type == MOUSEBUTTONUP:
			if evt.button == 1 and mode == 'menu' and playRect.collidepoint(mx,my):
				mode = 'play'
			elif evt.button == 1 and mode == 'game over' and play_Again_Rect.collidepoint(mx,my):
				mode = 'menu'	
	mx, my = mouse.get_pos()
	mb = mouse.get_pressed()
	kp = key.get_pressed()
	if mode == 'menu':
		score = 0
		playRect = Rect(width / 2 - 58, 500, 130, 80) # 520, 480
		screen.blit(images["back"], (0,0))
		screen.blit(f1.render("Mafia Defenders", True, (255,0,0)), (width/2 - 475,0))
		screen.blit(f2.render("Start", True, (255,0,0)), (width / 2 - 58, 480))
		
		display.flip()

	elif mode == "play":	
		try:
			s = str(ser.readline())[2:-5].split(",")
			flux = s[0]
			axis = s[1]
			print(s)
			# if 900 < int(s) < 1000:
			# 	player.inPosition = False
			# else:
			# 	if not player.inPosition:
			# 		player.switch_weapon()
			# 		print("SWITCH")
			# 	player.inPosition = True
		except: pass

		screen.fill(WHITE)
		MapLoad(fname)

		while (len(enemies) < 2):
			Enemy()
		if kp[K_SPACE]:
			if energy >= 1:
				player.shoot_bullet()
				energy -= .4
			screen.blit(f2.render(str(int(energy)), True, (0,0,0)), (100,100))
		else:
			if energy < 100:
				energy += .2	

		screen.blit(f2.render(str(int(energy)), True, (0,0,0)), (100,100))
		draw.rect(screen, BLACK, (98, 60, 204, 40), 4)
		draw.rect(screen, GREEN, (100, 62, int(energy*2), 36))	
		for s in all_sprites:
			s.update()

		hits = sprite.groupcollide(enemies, bullets, True, True)
		if hits:
			score += 1
			if score % 40 == 0:
				randomize()	
		if player.health <= 0:
			HighScore = max(score, HighScore)
			mode = 'game over'
		all_sprites.draw(screen)
		screen.blit(f2.render(str(int(score)), True, BLACK), (0, 0))
		draw.rect(screen, BLACK, (98, 10, 204, 40), 4)
		draw.rect(screen, GREEN, (100, 12, int(player.health*2), 36))
	elif mode == 'game over':
		screen.blit(images["back"], (0,0))	
		play_Again_Rect = Rect(width / 2 - 58, 500, 300, 95) #520, 480
		screen.blit(f2.render("Play Again", True, (255,0,0)), (width / 2 - 125, 480))
		screen.blit(f2.render("Score: " + str(int(score)), True, (255,0,0)), (width / 2 - 125, 0))
		screen.blit(f2.render("High Score: " + str(int(HighScore)), True, (255,0,0)), (width / 2 - 125, 150))
		display.flip()
		player.health = 100
		for i in enemies:
			i.kill()

	display.flip()
	myClock.tick(60)
quit()
