#Создай собственный Шутер!
from pygame  import * 
from random import *
from time import sleep
win_width = 700
win_height = 500 
window = display.set_mode((win_width,win_height))
display.set_caption('SHOOTER')
background = transform.scale(image.load('galaxy.jpg'),(win_width,win_height))
clock = time.Clock()
FPS = 120
mixer.init()
mixer.music.load('space.ogg')
font.init()
font=font.SysFont('Arial',24)
mixer.music.play()

lost = 0
hit = 0
t1 = font.render('Счёт:'+ str(hit),True,(255,255,255))
t2 = font.render('Пропущено:'+ str(lost),True,(255,255,255))
t3 = font.render('МЕГАХАРОШ',True,(200,222,0))
t4 = font.render('ЛОХ',True,(4,100,48))
#mixer.music.play()
#########################################################
class GameSprite(sprite.Sprite):
	def __init__(self, img, x, y, speed, width, height):
		super().__init__()
		self.height=height
		self.width=width
		self.speed = speed
		self.image = transform.scale(image.load(img),(self.width,self.height))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
	def reset(self):
		window.blit(self.image,(self.rect.x,self.rect.y))
class Player(GameSprite):
	def __init__(self, img, x, y, speed, width, height):
		super().__init__(img, x, y, speed, width, height)
	def update(self):
		keys = key.get_pressed()
		if keys[K_LEFT] and self.rect.x>0:
			self.rect.x-=self.speed
		elif keys[K_RIGHT] and self.rect.x+self.width<win_width:
			self.rect.x+=self.speed
	def fire(self):
		bullet =Bullet('bullet.png',self.rect.x + 35,self.rect.y,3,20,20)
		bullets.add(bullet)
class UFO(GameSprite):
	def __init__(self, img, x, y, speed, width, height):
		super().__init__(img, x, y, speed, width, height)
	def update(self):
		self.rect.y+=self.speed
		global lost,t2
		if self.rect.y>=win_height:
			self.rect.y = 0
			self.rect.x = randint(0 , win_width-self.width)
			lost += 1 
			t2 = font.render('Пропущено:'+ str(lost),True,(255,255,255))
class Bullet(GameSprite):
	def __init__(self, img, x, y, speed, width, height):
		super().__init__(img, x, y, speed, width, height)
	def update(self):
		self.rect.y-=self.speed
		if self.rect.y<=0:
			self.kill()
#########################################################
rocket = Player('rocket.png',win_width//2,win_height-80,3,80,80)
bullets = sprite.Group()
enemies = sprite.Group()
sprite.groupcollide(bullets,enemies, True, True)
for i in range(5):
	enemy = UFO('ufo.png',randint(0,win_width-80),0,1,80,80)
	enemies.add(enemy)

while True:
	window.blit(background,(0,0))
	window.blit(t1,(20,20))
	window.blit(t2,(20,50))
	enemies.update()
	enemies.draw(window)
	bullets.update()
	bullets.draw(window)
	rocket.update()
	rocket.reset()
	display.update()
	hits =	sprite.groupcollide(bullets,enemies, True, True)
	for i in hits:
		enemy = UFO('ufo.png',randint(0,win_width-80),0,1,80,80)
		enemies.add(enemy)
		hit += 1 
		t1 = font.render('Счёт:'+ str(hit),True,(255,255,255))

	for i in event.get():
		if i.type==QUIT:
			quit()
		if hit >= 20 :
			window.blit(t3,(300,200))
			display.update()
			sleep(2)
			quit()
		if lost >= 3 :
			window.blit(t4,(300,200))
			display.update()
			sleep(2)
			quit()
		if i.type==KEYDOWN:
			if i.key==K_SPACE:
				rocket.fire( )
				print('0')	
	clock.tick(FPS)