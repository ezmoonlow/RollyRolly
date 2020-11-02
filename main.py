import pygame as pg

SIZE = WIDTH, HEIGHT = 800, 600

GREEN = (0, 128, 0)
GREY = (120, 120, 120)
WHI = (200, 200, 200)

pg.init()
screen = pg.display.set_mode(SIZE)

FPS = 120
clock = pg.time.Clock()

bg_image = pg.image.load('Image/road.jpg')
bg_image_rect = bg_image.get_rect(topleft=(0, 0))
bg_image2_rect = bg_image.get_rect(topleft=(0, -HEIGHT))


def bg():
    pg.draw.line(screen, GREEN, (WIDTH - 780, HEIGHT - HEIGHT), (WIDTH - 780, HEIGHT), 40)
    pg.draw.line(screen, GREEN, (WIDTH - 20, HEIGHT - HEIGHT), (WIDTH - 20, HEIGHT), 40)
    for xx in range(10):
        for yy in range(10):
            pg.draw.line(
                screen, WHI,
                (40 + xx * 80, 0 if xx == 0 or xx == 9 else 10 + yy * 60),
                (40 + xx * 80, 600 if xx == 0 or xx == 9 else 50 + yy * 60), 5)  


class Car(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('Image/car1.png')


car1 = Car()
car1_image = car1.image
car1_w, car1_h = car1.image.get_width(), car1.image.get_height()
car1.x, car1.y = (WIDTH - car1_w) // 2, (HEIGHT - car1_h) // 2

game = True
while game:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            game = False

    car1.y -= 1
    if car1.y < -car1_h:
        car1.y = HEIGHT

    bg_image_rect.y += 1
    if bg_image_rect.y > HEIGHT:
        bg_image_rect.y = 0
    
    bg_image2_rect.y += 1
    if bg_image2_rect.y > 0:
        bg_image2_rect.y = -HEIGHT
    

    screen.fill(GREY)
    #bg()
    screen.blit(bg_image, bg_image_rect)
    screen.blit(bg_image, bg_image2_rect)
    screen.blit(car1_image, (car1.x, car1.y))
    pg.display.update()
    clock.tick(FPS)
    pg.display.set_caption(f'Rally          FPS: {int(clock.get_fps())}')


#pg.image.save(screen, 'road.jpg')
