from config import xsize,ysize

try:
    import pygame
    from pygame.transform import scale
except:
    import pip
    pip.main(["install","pygame"])

EXPLOSION_IMAGES = []

EXPLOSION_IMAGES.append(scale(pygame.image.load(f"explosion/tile000.png"), (100, 100)))
EXPLOSION_IMAGES.append(scale(pygame.image.load(f"explosion/tile001.png"), (120, 120)))
EXPLOSION_IMAGES.append(scale(pygame.image.load(f"explosion/tile002.png"), (140, 140)))
EXPLOSION_IMAGES.append(scale(pygame.image.load(f"explosion/tile003.png"), (160, 160)))
EXPLOSION_IMAGES.append(scale(pygame.image.load(f"explosion/tile004.png"), (170, 170)))
EXPLOSION_IMAGES.append(scale(pygame.image.load(f"explosion/tile005.png"), (180, 180)))
EXPLOSION_IMAGES.append(scale(pygame.image.load(f"explosion/tile006.png"), (190, 190)))
EXPLOSION_IMAGES.append(scale(pygame.image.load(f"explosion/tile007.png"), (200, 200)))

class Ammo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x, y, 25, 25)
        self.image = scale(pygame.image.load("ammo.png"), (25, 25))
        self.index = 0

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.rect.y -= 5

        if self.rect.y < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x, y, 40, 40)
        self.images = EXPLOSION_IMAGES.copy()
        self.index = 0

    def draw(self, screen):
        if self.index < 32:
            screen.blit(self.images[self.index // 4], (self.rect.x, self.rect.y))
            self.index += 1


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = scale(pygame.image.load("asteroid.png"), (50, 50))
        self.rect = pygame.Rect(x, y, 50, 50)
        self.yvel = 5

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.rect.y += self.yvel

        if self.rect.y > ysize:
            self.kill()


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.rect = pygame.Rect(x, y, 50, 100)
        self.image = scale(pygame.image.load("ship.png"), (50, 100))
        self.xvel = 0
        self.yvel = 0
        self.life = 10
        self.explosions = []
        self.score = 0

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        for explosion in self.explosions:
            explosion.draw(screen)

    def update(self, left, right, up, down, asteroids, ammos):

        # для каждого астероида
        for asteroid in asteroids:
            # если область, занимаемая астероидом пересекает область корабля
            if self.rect.colliderect(asteroid.rect):
                # уменьшаем жизнь
                self.life -= 1
                explosion = Explosion(self.rect.x- 25, self.rect.y - 50)
                self.explosions.append(explosion)

                asteroid.kill()
            for am in ammos:
                # если область, занимаемая астероидом пересекает область корабля
                if asteroid.rect.colliderect(am.rect):
                    # уменьшаем жизнь
                    explosion = Explosion(am.rect.x-37.5, am.rect.y)
                    self.explosions.append(explosion)
                    self.score += 1
                    asteroid.kill()
                    am.kill()

        if left:
            self.xvel -= 3
        if right:
            self.xvel += 3
        if down:
            self.yvel += 3
        if up:
            self.yvel -= 3
        if not (left or right):
            self.xvel = 0
        if not (up or down):
            self.yvel = 0
        self.rect.x += self.xvel
        self.rect.y += self.yvel
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > xsize - 50:
            self.rect.x = xsize - 50
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > ysize - 50:
            self.rect.y = ysize - 100