import pygame as pg
import pygame
import math


class Airfield():

	def __init__(self, display, color, length, angle):
		self.display = display
		self.image = pygame.Surface((4 , length))  
		self.image.set_colorkey((0,0,0))  
		self.image.fill(color)
		self.rotImage = pygame.transform.rotate(self.image , angle) 


	def update(self, xPos, yPos):
		self.display.blit(self.rotImage, (xPos, yPos))

class Player():
    """ Player icon and its transformations """
#                                                       1. koordinat er X-AKSEN!!
    def __init__(self, display):
        self.display = display
        self.image = pygame.Surface((22, 22), pygame.SRCALPHA)
        self.image.set_colorkey((0, 0, 0))
        self.image.fill((255, 255, 255))
        color = (255,0,255)
        self.image = pygame.Surface((13, 9), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, (0,0,0),	[(0, 4), (6, 0), (12, 4), (6, 8)], False)
        pygame.draw.polygon(self.image, color,		[(1, 4), (6, 1), (11, 4), (6, 7)], False)



 #       pygame.draw.ellipse(self.image, (255, 255, 255), (10, 0, 6, 20))
  #      pygame.draw.ellipse(self.image, (255, 255, 255), (0, 6, 4, 8))
#        pygame.draw.ellipse(self.image, (255, 255, 255), (0, 7, 20, 7))
 #       pygame.draw.rect(self.image, (0, 0, 0), (0, 13, 20, 5))
  #      pygame.draw.circle(self.image, (255, 255, 255), (10, 7), 4)
   #     pygame.draw.rect(self.image, (255, 255, 255), (10, 4, 8, 2))
#        pygame.draw.rect(self.image, (0, 0, 0),	(0, 5, 15, 20))



    #    pygame.draw.polygon(self.image, (0, 0, 0),       [(0, 12), (20, 12), (15, 20), (5, 20)], False)
#        pygame.draw.polygon(self.image, (255, 255, 255), [(3, 13), (17, 13), (13, 18), (7, 18)], False)
 #       pygame.draw.circle(self.image,(0, 0, 0), (10, 16), 3)

    def update(self, xPos, yPos, dx, dy, angle):
        radians = math.atan2( dx, dy )
 #       angle = int( math.degrees(radians) )
        self.rotImage = pg.transform.rotozoom(self.image, -angle, 1)
        offset = pg.math.Vector2(0, -10)  # move pivot point up from center
        rotated_offset = offset.rotate(angle)
        self.rect = self.rotImage.get_rect(center=(xPos, yPos) - rotated_offset)
        self.display.blit(self.rotImage, self.rect)  # Blit the rotated image




pg.init()
screen = pg.display.set_mode((640, 480))
clock = pg.time.Clock()
angle = 0

obj = Player(screen)
af = Airfield(screen, (255,0,255),40,115)
posX = 30
posY = 30

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    keys = pg.key.get_pressed()
    if keys[pg.K_RIGHT]:
        angle += 5
    elif keys[pg.K_LEFT]:
        angle -= 5
    elif keys[pg.K_w]:
        posY -= 5
    elif keys[pg.K_s]:
        posY += 5
    elif keys[pg.K_a]:
        posX -= 5
    if keys[pg.K_d]:
        posX += 5


    screen.fill((100,100,100))
    af.update(100,100)
    obj.update(posX, posY, 10, 11, angle)
    pg.display.set_caption('Angle: {}'.format(angle))
    pg.display.flip()
    clock.tick(30)

pg.quit()






