import pygame as pg

def changColor(image, color):
    colouredImage = pg.Surface(image.get_size())
    colouredImage.fill(color)

    finalImage = image.copy()
    finalImage.blit(colouredImage, (0, 0), special_flags=pg.BLEND_MULT)
    return finalImage


pg.init()
window = pg.display.set_mode((300, 160))

image = pg.transform.scale(pg.image.load('res/car_mask.png').convert_alpha(), (50, 50))
hue = 0

clock = pg.time.Clock()
nextColorTime = 0
run = True
while run:
    clock.tick(60)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    color = pg.Color(0)
    color.hsla = (hue, 100, 50, 100)
    hue = hue + 1 if hue < 360 else 0

    color_image = changColor(image, color)

    window.blit(color_image, color_image.get_rect(center=window.get_rect().center))
    pg.display.flip()

pg.quit()
exit()