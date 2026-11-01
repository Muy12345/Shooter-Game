from pygame import *
from random import randint
win_height = 500
win_width = 700
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load('galaxy.jpg'),(win_width, win_height))

font.init()
font = font.Font(None, 36)

score = 0
health = 10

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y,player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image),(size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 100:
            self.rect.y += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(100,600)
            self.rect.y = 0
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

rocket = Player('rocket.png', 5,400, 80, 100, 10)
bullets = sprite.Group()
clock = time.Clock()
enemies = sprite.Group()
for i in range(1,6):
    ufo = Enemy('ufo.png', randint(80,600), 0, 80, 50, randint(1,5))
    asteroid = Enemy('asteroid.png', randint(80,600), 0, 80, 50, randint(1,5))
    enemies.add(ufo)
    enemies.add(asteroid)

text_lose = font.render("You lose!", 1, (255, 255, 255))
text_win = font.render("You win!", 1, (255, 255, 255))

game_over = False

while True:
    for e in event.get():
        if e.type == QUIT:
            exit()
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                rocket.fire()
    if not game_over:
        window.blit(background, (0, 0))
        rocket.reset()
        rocket.update()
        enemies.draw(window)
        enemies.update()
        bullets.draw(window)
        bullets.update()
        score_text = font.render("Score:" + str(score), 1, (255, 255, 255))
        health_text = font.render("Health:" + str(health), 1, (255, 255, 255))
        window.blit(score_text, (10, 10))
        window.blit(health_text, (10, 50))

        collides = sprite.groupcollide(enemies, bullets, True, True)
        for c in collides:
            score += 1
            random_choice = randint(0,1)
            if random_choice == 0:
                asteroid = Enemy('asteroid.png', randint(30,600), 0, 80, 50, randint(1,5))
                enemies.add(asteroid)
            else:
                ufo = Enemy('ufo.png', randint(30,600), 0, 80, 50, randint(1,5))
                enemies.add(ufo)
        collide_2 = sprite.spritecollide(rocket, enemies, True)
        for c in collide_2:
            health -= 1
            random_choice = randint(0,1)
            if random_choice == 0:
                asteroid = Enemy('asteroid.png', randint(30,600), 0, 80, 50, randint(1,5))
                enemies.add(asteroid)
            else:
                ufo = Enemy('ufo.png', randint(30,600), 0, 80, 50, randint(1,5))
                enemies.add(ufo)
        if health <= 0:
            window.blit(text_lose, (250, 250))
            game_over = True
        if score >= 10:
            window.blit(text_win, (250, 250))
            game_over = True

    display.update()
    clock.tick(60)