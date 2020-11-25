import pygame as pg
import random
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'

SIZE = WIDTH, HEIGHT = 800, 600

GREEN = (0, 128, 0)
GREY = (120, 120, 120)
WHI = (200, 200, 200)
G = (0, 255, 0)
R = (178, 34, 34)
D = (127, 255, 212)
O = (255, 125, 0)
BL = (0, 0, 0)
rgb = [0, 250, 0]

pg.init()
screen = pg.display.set_mode(SIZE)

FPS = 120
clock = pg.time.Clock()
car_accident = 0
block = False
life = 3
time = 0
bt = True
level = 40

#Изображения и т.п
tree = [pg.image.load('Image/wood1.png'), pg.image.load('Image/wood2.jpg')]

cars = [pg.image.load('Image/car1.png'), pg.image.load('Image/car2.png'),
        pg.image.load('Image/car3.png')]
sound_car_accident = pg.mixer.Sound('Sound/udar.wav')
font = pg.font.Font(None, 32)

can = pg.image.load('Image/fuel.png')
can_rect = can.get_rect(topleft=(695, 6))

fon = pg.image.load('Image/f.jpeg')
fon_rect = fon.get_rect(topleft=(-50, -50))

button_start = pg.image.load('Image/start_button.png')
button_stop = pg.image.load('Image/stop_button.png')

button_start_rect = button_start.get_rect(center=(630, 200))
button_stop_rect = button_stop.get_rect(center=(630, 400))


class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load('Image/car4.png')
        self.ori_image = self.image
        self.angle = 0
        self.speed = 2
        self.acceleration = 0.02
        self.x, self.y = WIDTH // 2, HEIGHT // 2
        self.rect = self.image.get_rect()
        self.position = pg.math.Vector2(self.x, self.y)
        self.velocity = pg.math.Vector2()

    def update(self):
        self.image = pg.transform.rotate(self.ori_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.position += self.velocity
        self.rect.center = self.position

        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT]:
            self.velocity.x = self.speed
            self.angle -= 1
            if self.angle < -25:
                self.angle = -25
        elif keys[pg.K_LEFT]:
            self.velocity.x = -self.speed
            self.angle += 1
            if self.angle > 25:
                self.angle = 25
        else:
            self.velocity.x = 0
            if self.angle < 0:
                self.angle += 1
            elif self.angle > 0:
                self.angle -= 1
        if keys[pg.K_UP]:
            self.velocity.y -= self.acceleration
            if self.velocity.y < -self.speed:
                self.velocity.y = -self.speed
        elif keys[pg.K_DOWN]:
            self.velocity.y += self.acceleration
            if self.velocity.y > self.speed:
                self.velocity.y = self.speed
        else:
            if self.velocity.y < 0:
                self.velocity.y += self.acceleration
                if self.velocity.y > 0:
                    self.velocity.y = 0
            elif self.velocity.y < 0:
                self.velocity.y -= self.acceleration
                if self.velocity.y < 0:
                    self.velocity.y = 0
        if self.rect.left < 38:
            self.rect.left = 40
            self.angle -= 1
            if self.angle >= 0:
                self.angle = 0
        elif self.rect.right > 758:
            self.rect.right = 756
            self.angle += 1
            if self.angle <= 0:
                self.angle = 0

        elif self.rect.top < 1:
            self.rect.top = 4

        elif self.rect.bottom > 599:
            self.rect.bottom = 596


class Road(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.Surface(screen.get_size())
        self.image.fill(GREY)
        pg.draw.line(self.image, GREEN, (20, 0), (20, 600), 40)
        pg.draw.line(self.image, GREEN, (780, 0), (780, 600), 40)
        for xx in range(10):
            for yy in range(10):
                pg.draw.line(
                    self.image, WHI,
                    (40 + xx * 80, 0 if xx == 0 or xx == 9 else 10 + yy * 60),
                    (40 + xx * 80, 600 if xx == 0 or xx == 9 else 50 + yy * 60), 5)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 1

    def update(self):
        self.rect.y += self.speed
        if self.rect.top >= HEIGHT:
            self.rect.bottom = 0


class Trees(pg.sprite.Sprite):
    def __init__(self, x, y, img):
        pg.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        pass
        '''
        list_x.remove(self.rect.x)
        while True:
            self.rect.y = random.randrange(0, 600, 88)
            self.rect.x = random.randrange(0, 800, 760)
            if self.rect.x in list_x:
                continue
            else:
                list_x.append(self.rect.x)
                break
            if self.rect.y in list_y:
                continue
            else:
                list_x.append(self.rect.y)
                break
        '''


class Car(pg.sprite.Sprite):
    def __init__(self, x, y, img):
        pg.sprite.Sprite.__init__(self)

        if img == can:
            self.image = img
            self.speed = 0
        else:
            self.image = pg.transform.flip(img, False, True)
            self.speed = random.randint(2, 3)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0

            list_x.remove(self.rect.centerx)
            while True:
                self.rect.centerx = random.randrange(80, WIDTH, 80)
                if self.rect.centerx in list_x:
                    continue
                else:
                    list_x.append(self.rect.centerx)
                    self.speed = random.randint(2, 3)
                    break


all_sprite = pg.sprite.Group()
cars_group = pg.sprite.Group()
for r in range(2):
    all_sprite.add(Road(0, 0 if r == 0 else -HEIGHT))

list_x = []
n = 0
while n < 6:
    x = random.randrange(80, WIDTH, 80)
    if x in list_x:
        continue
    else:
        list_x.append(x)
        cars_group.add(Car(x, -cars[0].get_height(), cars[n] if n < len(cars) else random.choice(cars)))
        n += 1

for j in range(len(tree)):
    treess = Trees(40, 100 * j + 100, tree[j])
    all_sprite.add(treess)
player = Player()
fuel = Car(720, 40, can)
all_sprite.add(player, cars_group, fuel)


def screen1():
    sc = pg.Surface(screen.get_size())
    sc.fill(pg.Color('navy'))
    oran = pg.Surface((350, 600))
    oran.fill(O)
    sc.blit(fon, fon_rect)
    sc.blit(oran, (450, 0))
    sc.blit(button_start, button_start_rect)
    sc.blit(button_stop, button_stop_rect)
    sc.blit(font.render('управление стрелками', True, O), (20, 10))
    screen.blit(sc, (0, 0))


game = True
while game:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            game = False
        elif e.type == pg.MOUSEBUTTONDOWN:
            if e.button == 1:
                if button_start_rect.collidepoint(e.pos):
                    bt = False
                elif button_stop_rect.collidepoint(e.pos):
                    game = False
        elif e.type == pg.KEYDOWN:
            if e.key == pg.K_ESCAPE:
                bt = True
    if bt is True:
        time = time
    else:
        time += 0.01

    if pg.sprite.spritecollideany(player, cars_group):
        if block is False:
            player.position[0] += 50 * random.randrange(-1, 2, 2)
            player.angle = 50 * random.randrange(-1, 2, 2)
            sound_car_accident.play()
            car_accident += 1
            life -= 1
            block = True
            print(car_accident)
            if life == 0:
                bt = True
                life = life + 3
                car_accident = 0
                time = 0
    else:
        block = False
    if bt:
        screen1()

    else:
        level -= 0.01
        if level <= 0:
            bt = True
        elif level <= 10:
            rgb[:2] = 250, 250
        elif level <= 20:
            rgb[0] = 250

        all_sprite.update()
        all_sprite.draw(screen)
        pg.draw.rect(
            screen, rgb,
            (fuel.rect.left + 10, fuel.rect.bottom - level - 8, 21, level))
        screen.blit(font.render(f'Жизни = {life}', True, BL), (50, 10))
        screen.blit(font.render(str(int(time)), True, D), (380, 10))

    pg.display.update()
    clock.tick(FPS)
    pg.display.set_caption(f'Rally          FPS: {int(clock.get_fps())}')
'''pg.image.save(screen, 'road.jpg')'''
