#Создай собственный Шутер!
import pygame
from pygame import *
from random import randint


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

font.init()
font_interface = font.Font(None, 36)

win_w = 700
win_h = 500
FPS = 60

lost = 0
score = 0

clock = time.Clock()
window = display.set_mode((win_w, win_h))
display.set_caption('Shooter')
background = transform.scale(image.load('galaxy.jpg'),(win_w, win_h))

finish = False
run = True

class GameSprite(sprite.Sprite):
    def __init__(self, speed, size_x, size_y, x, y, sprite_image):
        super().__init__()
        self.image = transform.scale(image.load(sprite_image), (size_x, size_y))
        self.speed = speed

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_w-85:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(15, 15, 20, self.rect.centerx, self.rect.top, 'bullet.png')
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_h:
            lost += 1
            self.rect.x = randint(80, win_w-80)
            self.rect.y = 0


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

ship = Player(10, 80, 100, 5,win_h-100, 'rocket.png')
monsters = sprite.Group()
for i in range(1, 6):
    monstr = Enemy(randint(1, 5), 80, 50, randint(80, win_w-80), -10, 'ufo.png')
    monsters.add(monstr)

bullets = sprite.Group()
counter = 0
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False


    window.blit(background,(0,0))

    if not finish:
        text_score = font_interface.render('Score: ' + str(score), True, (255,255,255))
        text_lost = font_interface.render('Lost: ' + str(lost), True, (255, 255, 255))
        window.blit(text_score, (10, 20))
        window.blit(text_lost, (10, 50))

        monsters.draw(window)
        monsters.update()

        ship.reset()
        ship.update()

        bullets.draw(window)
        bullets.update()

        keys = key.get_pressed()
        if keys[K_SPACE]:
            counter += 1
            if counter > 5:
                mixer.Sound('fire.ogg').play()
                ship.fire()
                counter = 0

        collaides = sprite.groupcollide(monsters, bullets, True, True)
        for col in collaides:
            col.kill()
            score += 1
            monstr = Enemy(randint(1, 5), 80, 50, randint(80, win_w - 80), -10, 'ufo.png')
            monsters.add(monstr)

        if score > 20:
            finish = True
            window.blit(font.Font(None, 80).render('WIN', True, (255,255,255)), (200, 200))

        if lost > 20:
            finish = True
            window.blit(font.Font(None, 80).render('LOSE', True, (255,0,0)), (200, 200))

        display.update()
    clock.tick(FPS)