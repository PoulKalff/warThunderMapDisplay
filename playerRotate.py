import io
import os
import sys
import math
import time
import json
import pygame
import requests
import pygame.locals
from io import BytesIO
from PIL import Image


angle = 0
ox = 0
oy = 0
xPos = 320
yPos = 240
xPos2 = 430
yPos2 = 430




class MapObject():

    def __init__(self, xPos, yPos, color, oType, angle = False):
        self.xPos = xPos
        self.yPos = yPos
        self.type = oType
        if oType == 100:      # player
            _image = pygame.image.load("/home/klf/Desktop/WarThunderMap/icons/player2.png")
            self.image = pygame.transform.rotozoom(_image, angle, 1)
            self.rect = _image.get_rect(center = [int(i) for i in (xPos, yPos)])
            self.xPos = self.rect.x
            self.yPos = self.rect.y
        elif oType == 200:      # player
            _image = pygame.image.load("/home/klf/Desktop/WarThunderMap/icons/player.png")
            self.image = pygame.transform.rotozoom(_image, angle, 1)

            offset = pygame.math.Vector2(ox, oy)  # move pivot point up from center
            rotated_offset = offset.rotate(angle)


      #      rect = rotated_image.get_rect(center=pivot+rotated_offset)
       #     return rotated_image, rect  # Return the rotated image and shifted rect.


            self.rect = _image.get_rect(center = (xPos, yPos) + rotated_offset)
            self.xPos = self.rect.x
            self.yPos = self.rect.y
        else:
            self.image = pygame.Surface((7, 7), pygame.SRCALPHA)
            pygame.draw.circle(self.image,(0, 0, 0), (3, 3), 3)
            pygame.draw.circle(self.image, color, (3, 3), 2)
        # corrections for objects



    def draw(self, _display):
        w, h = self.image.get_size()
        xPos = self.xPos + 24 - int(w / 2)
        yPos = self.yPos + 24 - int(h / 2)
        print('                    ',  int(w / 2), int(h / 2))
        _display.blit(self.image, (xPos, yPos)) 



pygame.init()
display = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        angle += 1
    elif keys[pygame.K_DOWN]:
        angle -= 1
    if keys[pygame.K_RIGHT]:
        angle += 5
    elif keys[pygame.K_LEFT]:
        angle -= 5
    elif keys[pygame.K_w]:
        ox -= 1
    elif keys[pygame.K_s]:
        ox += 1
    elif keys[pygame.K_a]:
        oy -= 1
    if keys[pygame.K_d]:
        oy += 1
    if angle > 360 or angle < -360: angle = 0
#    print(xPos, yPos)
    angle += 5


    pygame.display.set_caption('Angle: {}'.format(angle))
    display.fill((0, 0, 255))
    pygame.draw.line(display, (0, 0, 0), (320, 0), (320, 480))
    pygame.draw.line(display, (0, 0, 0), (0, 240), (640, 240))
    pygame.draw.line(display, (255, 0, 0), (430, 0), (430, 480))
    pygame.draw.line(display, (255, 0, 0), (0, 430), (640, 430))



#    radians = math.atan2(0 , 0)
 #   angle = int( math.degrees(radians) )
    obj = MapObject(xPos, yPos, (255, 255, 255), 100, angle)
    obj.draw(display)
    obj2 = MapObject(yPos2, yPos2, (255, 255, 255), 200, angle)
    obj2.draw(display)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()






