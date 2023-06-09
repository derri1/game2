from pygame import *
from random import randint
from time import time as timer

#Consts
img_enemy = 'ufo22.png'
img_hero = 'tennis2.png'
img_bg = 'tennis_bg.jpg'
img_bullet = 'ball2.png'
img_asteroid = 'football2.png'
score = 0
lost = 0
goal = 20
max_lost = 10
life = 3

#Main Game Window
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Shooter')
background = transform.scale(image.load(img_bg), (win_width, win_height))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (80, 80))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        elif keys[K_RIGHT] and self.rect.x < win_width - 70:
            self.rect.x += self.speed
        elif keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        elif keys[K_DOWN] and self.rect.y < win_height - 75:
            self.rect.y += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx - 30, self.rect.top, 115, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
    
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
#Characters
player = Player(img_hero, 5, win_height - 100, 80, 100, 7)
monsters = sprite.Group()
asteroids = sprite.Group()

for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_height - 80), -40, 80, 50, randint(1,2))
    monsters.add(monster)

for i in range(1, 2):
    asteroid = Asteroid(img_asteroid, randint(30, win_height - 30), -40, 80, 50, randint(1, 2))
    asteroids.add(asteroid)

bullets = sprite.Group()

#Sounds
mixer.init()
mixer.music.load('background_music.mp3')
mixer.music.play()
fire = mixer.Sound('sound.ogg')
hit = mixer.Sound('rock.ogg')

#Text
font.init()
font1 = font.SysFont('Arial', 80)
win = font1.render('GG!!!', True, (255,255,255))
lose = font1.render('get the L', True, (180,0,0))
font2 = font.SysFont('Arial', 36)

#Game
FPS = 60
game = True
finish = False
real_time = False
num_fire = 0
#clock = time.Clock()

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and real_time == False:
                    num_fire = num_fire + 1
                    fire.play()
                    player.fire()
                
                if num_fire  >= 5 and real_time == False:
                    last_time = timer()
                    real_time = True

    if finish != True:
        window.blit(background, (0, 0))
        text = font2.render('Счёт: ' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        player.update()
        monsters.update()
        bullets.update()
        asteroids.update()

        player.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        if real_time == True:
            now_time = timer()
            if now_time - last_time < 1:
                reload = font2.render('ПЕРЕЗАРЯДКА', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                real_time = False

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 2))
            monsters.add(monster)

        #Collide with asteroids
        if sprite.spritecollide(player, asteroids, False) or sprite.spritecollide(player, monsters, False) or lost >= max_lost:
            hit.play()
            sprite.spritecollide(player, monsters, True)
            sprite.spritecollide(player, asteroids, True)
            life = life - 1

        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)

        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))
    
        display.update()

    else:
        finish = False
        score = 0
        lose = 0
        num_fire = 3
        life = 3
        for b in bullets:
            b.kill()
        for t in monsters:
            t.kill()
        for x in asteroids:
            x.kill()

        time.delay(3000)
        for u in range(1,6):
            monster = Enemy(img_enemy, randint(80, win_height - 80), -40, 80, 50, randint(1,2))
            monsters.add(monster)

    time.delay(2)

