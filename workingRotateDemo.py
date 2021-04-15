import pygame as pg


pg.init()
screen = pg.display.set_mode((640, 480))
clock = pg.time.Clock()
BG_COLOR = pg.Color('gray12')
IMAGE = pg.image.load("/home/klf/Desktop/WarThunderMap/icons/player.png")
pivot = [200, 200]
offset = pg.math.Vector2(0, 10) # move rotaion 10 up from center
angle = 0

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    keys = pg.key.get_pressed()
    if keys[pg.K_d] or keys[pg.K_RIGHT]:
        angle += 5
    elif keys[pg.K_a] or keys[pg.K_LEFT]:
        angle -= 5
    if keys[pg.K_f]:
        pivot[0] += 2


    rotated_image = pg.transform.rotozoom(IMAGE, angle, 1)  # Rotate the image.
    rotated_offset = offset.rotate(-angle)  # Rotate the offset vector the other way (-angle)
    rect = rotated_image.get_rect(center=pivot+rotated_offset)






    # Drawing.
    screen.fill(BG_COLOR)
    screen.blit(rotated_image, rect)  # Blit the rotated image.

    pg.draw.circle(screen, (30, 250, 70), pivot, 2)  # Pivot point.
    pg.draw.rect(screen, (30, 250, 70), rect, 1)  # The rect.
    pg.display.set_caption('Angle: {}'.format(angle))
    pg.display.flip()
    clock.tick(30)

pg.quit()
