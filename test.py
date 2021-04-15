import pygame as py  
import pygame


# define constants  
WIDTH = 500  
HEIGHT = 500  
FPS = 200

# define colors  
BLACK = (0 , 0 , 0)  
GREEN = (0 , 255 , 0)
YELLOW = (255 , 255 , 0)


screen = py.display.set_mode((WIDTH , HEIGHT))

image ='/home/klf/Desktop/WarThunderMap/icons/player.png'

def draw_leaves():
    leaf1 = pygame.Surface((70, 12))
    leaf1.fill((23,15,59))
    leaf1.set_colorkey((23,15,59))
    pygame.draw.ellipse(leaf1, (0 , 255 , 0), (0, 0, 7, 12))
    screen.blit(pygame.transform.rotate(leaf1, -70), (22, 15))
    screen.blit(pygame.transform.rotate(leaf1, -70), (7, 17))
    screen.blit(pygame.transform.rotate(leaf1, -70), (73, 40))
    screen.blit(pygame.transform.rotate(leaf1, -70), (75, 33))
    screen.blit(pygame.transform.rotate(leaf1, -70), (77, 30))
    screen.blit(pygame.transform.rotate(leaf1, -70), (60, 205))
    screen.blit(pygame.transform.rotate(leaf1, -70), (63, 190))
    screen.blit(pygame.transform.rotate(leaf1, -70), (66, 190))



# initialize pygame and create screen  
py.init()  



# for setting FPS  
clock = py.time.Clock()  


draw_leaves()


rot = 0  
rot_speed = 2  

# define a surface (RECTANGLE)  
image_orig = py.Surface((10 , 100))  
# for making transparent background while rotating an image  
image_orig.set_colorkey(BLACK)  
# fill the rectangle / surface with green color  
image_orig.fill(GREEN)  
# creating a copy of orignal image for smooth rotation  
image = image_orig.copy()  
image.set_colorkey(BLACK)  
# define rect for placing the rectangle at the desired position  
rect = image.get_rect()
x, y = py.mouse.get_pos()
rect.center = (x, y)  

image_orig = py.transform.rotate(image_orig , -25)  

# keep rotating the rectangle until running is set to False
running = True  
while running:  

    x, y = py.mouse.get_pos()
    # set FPS  
    clock.tick(FPS)  
    # clear the screen every time before drawing new objects  
    screen.fill((255, 255, 255))  
    # check for the exit  
    for event in py.event.get():  
        if event.type == py.QUIT:  
            running = False
    # making a copy of the old center of the rectangle  
    old_center =(x, y)
    # defining angle of the rotation  
    rot = (rot + rot_speed) % 360  
    # rotating the orignal image
    keys = py.key.get_pressed()
    rot_speed = .2 
    image_orig = py.transform.rotate(image_orig , 0)  
    rect = image_orig.get_rect()  
        # set the rotated rectangle to the old center  
    rect.center = (x, y)  
        # drawing the rotated rectangle to the screen  
    screen.blit(image_orig , rect)  

    pygame.draw.polygon(screen,BLACK,[(8, 0), (2, 0), (0, 2), (5, 30),  (10, 2)],True)

  #  image = pygame.image.load('icons/player.png')


        # flipping the display after drawing everything  
    py.display.flip()
    if(keys[py.K_a]):
        rot_speed = .2 
        image_orig = py.transform.rotate(image_orig , rot)  
        rect = image_orig.get_rect()  
        # set the rotated rectangle to the old center  
        rect.center = (x, y)  
        # drawing the rotated rectangle to the screen  
        screen.blit(image_orig , rect)  
        # flipping the display after drawing everything  
        py.display.flip()
    if(keys[py.K_d]):
        rot_speed = -.2 
        image_orig = py.transform.rotate(image_orig , rot)  
        rect = image_orig.get_rect()  
        # set the rotated rectangle to the old center  
        rect.center = (x, y)  
        # drawing the rotated rectangle to the screen  
        screen.blit(image_orig , rect)  
        # flipping the display after drawing everything  
        py.display.flip()
    rect.center = (x, y)

py.quit()  
