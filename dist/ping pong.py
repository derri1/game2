from pygame import *

#Main Game Window
back = (200,255,255)
win_width = 600
win_height = 500
window = display.set_mode((win_width, win_height))
window.fill(back)
display.set_caption('Ping-Pong')

#consts
game = True
finish = False
clock = time.Clock()
FPS = 60
speed_x = 3
speed_y = 3


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y,  player_speed, size_x, size_y,):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (80, 80))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        elif keys[K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        elif keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

racket1 = Player('tennis2.png', 30, 200, 4, 50, 150)
racket2 = Player('tennis2.png', 520, 200, 4, 50, 150)
ball = GameSprite('ufo.png', 200, 200, 4, 50, 50)

#Text
font.init()
font = font.Font(None, 35)
lose_1 = font.render('1 player lose', True, (180, 0, 0))
lose_2 = font.render('2 player lose', True, (180, 0, 0))

#Music
mixer.init()
#mixer.music.load('bg_music.ogg')
#mixer.music.play('bg_music.ogg')

#punch = mixer.Sound('punch.mp3')

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish != True:
        window.fill(back)
        racket1.reset()
        racket2.reset()
        ball.reset()
    
        racket1.update_l()
        racket2.update_r()
        ball.update()

        ball.rect.x += speed_x
        ball.rect.y += speed_y

        if sprite.collide_rect(racket1, ball) or sprite.collide_rect(racket2, ball):
            speed_x *= -1
            speed_y *= 1
            punch.play()

        if ball.rect.y > win_height - 50 or ball.rect.y < 0:
            speed_y *= -1

        if ball.rect.x < 0:
            finish = True
            window.blit(lose_1, (200, 200))
            game_over = True

        if ball.rect.x > win_width:
            finish = True
            window.blit(lose_2, (200, 200))
            game_over = True


    display.update()
    clock.tick(FPS)