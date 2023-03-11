import random
import time
from config import xsize,ysize
from spraites  import *

try:
    import pygame
    from pygame.transform import scale
except:
    import pip
    pip.main(["install","pygame"])


pygame.init()
screen = pygame.display.set_mode((xsize, ysize))
pygame.display.set_caption("Asteroids")

sky = scale(pygame.image.load("sky.jpg"), (xsize, ysize))
# создаем корабль в точке 400 400
ship = Spaceship(xsize / 2, ysize / 2 - 50)

# заведем переменные, чтобы помнить, какие клавиши нажаты
left = False
right = False
down = False
up = False
ammo = False

l_ammo = time.time()

asteroids = pygame.sprite.Group()
ammos = pygame.sprite.Group()

pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 30)
clock = pygame.time.Clock()
dfs = True
while dfs:
    with open('scored', 'r') as file:
        text = file.read()
    sads = text.split('\n')
    best = max(sads)
    d = font.render(f'THE BEST SCORE: {best}', False, (255, 255, 255))
    screen.blit(d, (xsize/4, ysize/4*1.5))
    d = font.render('PRESS SPACE FOR START', False, (255, 255, 255))
    screen.blit(d, (xsize / 4, ysize / 4 * 2.5))
    pygame.display.update()
    for e in pygame.event.get():
        # если нажата клавиша - меняем переменную
        if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
            dfs = False
        if e.type == pygame.QUIT:
            raise SystemExit("QUIT")


while True:
    if random.randint(1, 100) < 25:
        asteroid_x = random.randint(-100, xsize + 100)
        asteroid_y = -100
        asteroid = Asteroid(asteroid_x, asteroid_y)
        asteroids.add(asteroid)

    for e in pygame.event.get():
        # если нажата клавиша - меняем переменную
        if e.type == pygame.KEYDOWN and e.key == pygame.K_LEFT:
            left = True
        if e.type == pygame.KEYDOWN and e.key == pygame.K_RIGHT:
            right = True
        if e.type == pygame.KEYDOWN and e.key == pygame.K_UP:
            up = True
        if e.type == pygame.KEYDOWN and e.key == pygame.K_DOWN:
            down = True

        # если отпущена клавиша - меняем переменную
        if e.type == pygame.KEYUP and e.key == pygame.K_LEFT:
            left = False
        if e.type == pygame.KEYUP and e.key == pygame.K_RIGHT:
            right = False
        if e.type == pygame.KEYUP and e.key == pygame.K_UP:
            up = False
        if e.type == pygame.KEYUP and e.key == pygame.K_DOWN:
            down = False

        if e.type == pygame.KEYDOWN and e.key == pygame.K_x:
            ammo = True
        if e.type == pygame.KEYUP and e.key == pygame.K_x:
            ammo = False

        if e.type == pygame.QUIT:
            raise SystemExit("QUIT")

    if ammo and time.time() > l_ammo+0.1:
        amm = Ammo(ship.rect.x +12.5, ship.rect.y - 12.5)
        ammos.add(amm)
        l_ammo = time.time()

    # рисуем небо
    screen.blit(sky, (0, 0))

    ammos.update()
    ammos.draw(screen)

    asteroids.update()
    asteroids.draw(screen)

    # перемещаем корабль
    ship.update(left, right, up, down, asteroids, ammos)
    # просим корабль нарисоваться
    ship.draw(screen)

    for asteroid in asteroids:
        asteroid.update()
        asteroid.draw(screen)

    clock.tick(60)
    FPS = font.render(f'FPS: {int(clock.get_fps())}', False, (255, 255, 255))
    screen.blit(FPS, (0, 0))

    life = font.render(f'HP: {ship.life}', False, (255, 255, 255))
    screen.blit(life, (0, 30))

    sc = font.render(f'SCORE: {ship.score}', False, (255, 255, 255))
    screen.blit(sc, (0, 60))

    if ship.life <= 0:
        break

    pygame.display.update()

over = scale(pygame.image.load("wasted.png"), (xsize, 500))
pygame.display.update()
with open("scored", "a") as file:
    file.write('\n'+str(ship.score))

while True:
    screen.blit(over, (0, ysize / 2 - 250))
    pygame.display.update()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            raise SystemExit("QUIT")
