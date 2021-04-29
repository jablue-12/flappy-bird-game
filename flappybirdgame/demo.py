import pygame
import sys

#NOTE: Top Left is at (0,0) coordinate
#canvas size
WIDTH = 576
HEIGHT = 720

#animation
FPS = 120 #frames per second
GRAVITY = 0.25 #gravity for the bird
MOVE_BIRD_UP = 10 #speed of the bird going up

#draw_floor function
#function that draws the floor of the background.
#floorX_pos parameter is the x position of the floor
#floor_surface parameter is the image of the floor surface.
def draw_floor(floorX_pos,floor_surface):
    #draw 2 floor surfaces. The first floor appears on the window while the second floor appears at the end of the window.
    screen.blit(floor_surface,(floorX_pos, (HEIGHT / 2) + (HEIGHT / 3)))  # floor image. position close to the bottom of the screen.
    screen.blit(floor_surface,(floorX_pos + WIDTH, (HEIGHT / 2) + (HEIGHT / 3)))  # floor image. position close to the bottom of the screen.
#end draw_floor function

#initiates pygame
pygame.init()

screen = pygame.display.set_mode((WIDTH,HEIGHT)) #created canvas
clock = pygame.time.Clock() #used for framerate

#get the images
background_surface = pygame.image.load('assets/background-day.png').convert() #display surface
floor_surface = pygame.image.load('assets/base.png').convert() #floor image
bird_image = pygame.image.load('assets/bluebird-midflap.png').convert() # bird image

#scale the image
background_surface = pygame.transform.scale(background_surface, (WIDTH, HEIGHT))
floor_surface = pygame.transform.scale2x(floor_surface) #scale the image twice
bird_image = pygame.transform.scale2x(bird_image) #scale the image twice

bird_rect = bird_image.get_rect(center= (100,HEIGHT/2)) #puts a rectangle around the image of the bird

#x and y position
floorX_pos = 0

#variables for the Bird animation
bird_movement = 0

while True: #run foreva
    for event in pygame.event.get(): #check what event is happening
        if event.type == pygame.QUIT:
            #exit pygame
            pygame.quit()
            sys.exit() # shuts down the game

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: #spacebar is clicked
                #want to move the bird up. Decrease value of bird_movement
                bird_movement = 0 #ignore the gravity so that the speed going up is constant.
                bird_movement -= MOVE_BIRD_UP
                #print("move up bird!")

    screen.blit(background_surface,(0,0)) #background image position at origin

    screen.blit(bird_image,bird_rect) #bird image
    bird_movement+= GRAVITY
    bird_rect.centery += bird_movement #change the y position of the bird

    #draw the floor surface
    draw_floor(floorX_pos,floor_surface)
    floorX_pos -= 1  # move to the left

    if floorX_pos <= -WIDTH: #keep moving the floor foreva
        floorX_pos = 0


    pygame.display.update() #simply redraws the image
    clock.tick(FPS) #runs 120 fps or slower