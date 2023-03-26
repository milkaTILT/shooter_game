from pygame import *
from random import randint
import time as Timer

width, height = 700, 500
window = display.set_mode((width, height))
display.set_caption('Shooter | шутер')

background = transform.scale(image.load('rar.jpg'), (width, height))


#mixer.init()
#mixer.music.load('space.ogg')
#mixer.music.play()
#fire = mixer.Sound('fire.ogg')

class GameSprite(sprite.Sprite):
    def __init__(self, _image, x, y, width, height, speed):
        super().__init__()
        self.speed = speed
        self.image = transform.scale(image.load(_image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
  
    def clear(self):
        window.blit(self.image, (self.rect.x, self.rect.y))   

class Player(GameSprite):
    health = 3
    num_fire = 0
    rel_flag = False
    prev_time = Timer.time()

    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < (width - self.rect.width - 5):
            self.rect.x += self.speed
        if keys_pressed[K_SPACE]:
            self.fire()
    def fire(self):
        if Timer.time() - self.prev_time < 1 and self.rel_flag:
            return
        if Timer.time() - 0.3 >self.prev_time:
            #fire_sound.play()
            x = self.rect.centerx
            y = self.rect.top                                     
            bullet = Bullet('bullet.png', x, y, 10, 20, 5)
            bullet.rect.x -= bullet.rect.width // 2
            bullets.add(bullet)
            self.prev_time = Timer.time()
            self.num_fire += 1
            if self.num_fire >= 5:
                self.rel_flag = True

    def clear(self):
        super().clear()
        if Timer.time() - self.prev_time > 1 and self.rel_flag:
            self.rel_flag = False
            self.num_fire = 0
        if self.rel_flag:
            reload_time = round(2 - (Timer.time() - self.prev_time), 1)
            reload_text = 'Перезарядка ещё ' + str(reload_time) + 'с'
            reload = my_font.render('Перезарядка', True, (171, 0, 255))
            reload_rect = reload.get_rect()
            reload_rect.centerx = width // 2
            reload_rect.centery = height // 2
            window.blit(reload, (reload_rect.x, reload_rect.y))
        health = my_font.render(str(self.health), True, (255, 50, 50))
        window.blit(health, (width - 50, 20))

        
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > height:
            self.rect.y = -60
            self.speed = randint(1, 3 )
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > height:
            self.rect.y = -self.rect.height
            self.rect.x = randint(0, width - self.rect.width)
            self.speed = randint(1, 5)


sprite1 = Player(('roc.png'), 340, 435, 60, 60, 8)


monsters = sprite.Group()
for i in range(5):
    enemy = Enemy('ufo.png', randint(0, width), -100, 60, 60, randint(1, 3))
    monsters.add(enemy)

asteroids = sprite.Group()
for i in range(3):
    asteroid = Asteroid('asteroid.png', randint(0,  width), -100, 50, 50, randint(1, 5))
    asteroids.add(asteroid)

bullets = sprite.Group()

font.init()
my_font = font.SysFont('Arial', 34)
# my_font = font.Font('20179.otf', 34)

clock = time.Clock()
FPS = 60
lost = 0
score = 0

game = True
finish = False
while game:
    if not finish:
        window.blit(background, (0, 0))
        sprite1.update()
        sprite1.clear()
        monsters.update()
        monsters.draw(window)
        asteroids.update()
        asteroids.draw(window)
        
        missed_text = my_font.render('Пропущено: ' + str(lost), True, (171, 0, 255))
        killed_text = my_font.render('Уничтожено: ' + str(score), True, (171, 0, 255))
        window.blit(missed_text, (7, 7))
        window.blit(killed_text, (7, 40))
        bullets.update()
        bullets.draw(window)

        collided = sprite.groupcollide(monsters, bullets, True, True)
        if len(collided) > 0: 
            for i in range(len( collided)):
                enemy = Enemy('ufo.png', randint(0, width), -100, 60, 60, randint(1, 3))
                monsters.add(enemy)
                score += 1  

        

        if lost >= 3:
            finish = True
            result_text = my_font.render('Вы проиграли!', True, (255, 30, 30))
        if score >= 10:
            finish = True
            result_text = my_font.render('Вы выиграли!', True, (30, 255, 30))
        last_tick_time = Timer.time()
    else:

        window.blit(background, (0, 0))
        text_rect = result_text.get_rect()
        bg_rect = background.get_rect()
        text_rect.center = bg_rect.center
        window.blit(result_text, (text_rect.x, text_rect.y))
        if Timer.time() - last_tick_time > 3:
            score = 0
            lost = 0
            finish = False
            monsters.empty()
            for i in range(5):
                enemy = Enemy('ufo.png', randint(0, width), -100, 100, 100, randint(1, 8))
                monsters.add(enemy)
            sprite1.rect.x = bg_rect.centerx

    for e in event.get():
        if e.type == QUIT:
            game = False

    display.update()
    clock.tick(FPS)
