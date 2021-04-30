import pygame
import sys
import random

#NOTE: Top Left is at (0,0) coordinate
#canvas size
WIDTH = 576
HEIGHT = 720

#animation
FPS = 100 #frames per second
GRAVITY = 0.25 #gravity for the bird
MOVE_BIRD_UP = 10 #speed of the bird going up
BIRD_X_LOCATION = 100 #center.x of the bird image
BIRDFLAP_TIME = 200 #in mseconds
PIPE_DISTANCE = 200
PIPE_SPAWN_TIME = 1500 #in mseconds


#draw_floor function
#function that draws the floor of the background.
#floorX_pos parameter is the x position of the floor
#floor_surface parameter is the image of the floor surface.
def draw_floor(floorX_pos,floor_surface):
    #draw 2 floor surfaces. The first floor appears on the window while the second floor appears at the end of the window.
    screen.blit(floor_surface,(floorX_pos, (HEIGHT / 2) + (HEIGHT / 3)))  # floor image. position close to the bottom of the screen.
    screen.blit(floor_surface,(floorX_pos + WIDTH, (HEIGHT / 2) + (HEIGHT / 3)))  # floor image. position close to the bottom of the screen.
#end draw_floor function

#new_pipe function
#function that creates a new pipe to be added to the pipe list
#image_pipe parameter is the image of the pipe.
#pipe_height parameter is a list of possible heights for the pipe to be created.
#it will return the created two pipes.
def new_pipe(image_pipe,pipe_height):
    random_height = random.choice(pipe_height)
    bot_pipe = image_pipe.get_rect(midtop=(WIDTH,random_height)) #points upwards so bottom pipe
    top_pipe = image_pipe.get_rect(midbottom=(WIDTH,random_height-PIPE_DISTANCE)) #points downwards so top pipe
    #print("random_height = " + str(random_height))
    return bot_pipe,top_pipe
#end new_pipe function

#move_pipes function
#function that moves all the pipes from the list to the left by 5
#it will return the changed pipes.
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5 #move each pipe from the list to the left (5)
    return pipes
#end move_pipes function

#draw_pipes function
#function that draws the pipes either pointing upward or downward.
def draw_pipes(screen,image_pipe,pipes):
    for pipe in pipes:
        if pipe.bottom >= HEIGHT-100: #100 so that all the heights will not be upside down.
            screen.blit(image_pipe,pipe)
        else:
            flip_pipe_image = pygame.transform.flip(image_pipe,False,True) #flip y direction
            screen.blit(flip_pipe_image,pipe)
#end draw_pipes function

#is_collision function
#function that checks if there is a collision between the bird and any pipes
#bird_rect parameter is the bird rectangle.
#pipes parameter is the list of pipes (tuple).
#It will return True if there is a collision. Otherwise, false.
def is_collision(bird_rect,pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            print("collision occured against the pipe")
            return True

        if bird_rect.top<= -50 or bird_rect.bottom>= (HEIGHT / 2) + (HEIGHT / 3):
            #-50 so that bird can still go above the origin.
            #(HEIGHT / 2) + (HEIGHT / 3) is the height of the floor
            print("collision occured against the ceiling or bottom")
            return True

    return False
#end is_collision function

#rotate_bird function
#function that rotates the image of the bird
#image_bird paramater is the image of the bird to be rotated.
#bird_movement parameter is the movement of the bird.
def rotate_bird(image_bird,bird_movement):
    new_bird = pygame.transform.rotozoom(image_bird,-bird_movement * 3,1) #rotates the image using rotozoom
    return new_bird
#end rotate_bird function


#bird_animation function
#function that animates the wings of the bird.
#bird_frames parameter is a list of bird images.
#index parameter is the index that chooses which bird frame will be used.
#prev_bird_rect parameter is the previous bird rectangle that will be used to get the location of the y coordinate.
#it will return a tuple of the chosen bird frame and a rectangle around it.
def bird_animation(bird_frames,index,prev_bird_rect):
    new_bird = bird_frames[index]
    new_bird_rect = new_bird.get_rect(center = (BIRD_X_LOCATION,prev_bird_rect.centery))
    return new_bird,new_bird_rect
#end bird_animation function

#initiates pygame
pygame.init()

screen = pygame.display.set_mode((WIDTH,HEIGHT)) #created canvas
clock = pygame.time.Clock() #used for framerate

#get the images
background_surface = pygame.image.load('assets/background-day.png').convert() #display surface
floor_surface = pygame.image.load('assets/base.png').convert() #floor image
pipe_image = pygame.image.load('assets/pipe-green.png').convert() #obstacle image

#bird images/animation
bird_downflap_surface = pygame.image.load('assets/redbird-downflap.png').convert_alpha()
bird_midflap_surface = pygame.image.load('assets/redbird-midflap.png').convert_alpha()
bird_upflap_surface = pygame.image.load('assets/redbird-upflap.png').convert_alpha()
bird_frames = [bird_downflap_surface,bird_midflap_surface,bird_upflap_surface] #used for animation
bird_index = 0

bird_image = bird_frames[bird_index]
bird_rect = bird_image.get_rect(center = (BIRD_X_LOCATION,HEIGHT/2))

BIRDFLAP = pygame.USEREVENT + 1 # +1 so that its different from SPAWNPIPE
pygame.time.set_timer(BIRDFLAP,BIRDFLAP_TIME)

#scale the image
background_surface = pygame.transform.scale(background_surface, (WIDTH, HEIGHT))
floor_surface = pygame.transform.scale2x(floor_surface) #scale the image twice


#x and y position
floorX_pos = 0

#variables for the Bird animation
bird_movement = 0

#pipes
pipe_list = [] #contains a list of pipes
pipe_height = [300,400,500] #possible heights of the pipe
SPAWNPIPE = pygame.USEREVENT #triggered by timer
pygame.time.set_timer(SPAWNPIPE,PIPE_SPAWN_TIME) #SPAWN TIME in milliseconds

#game logic
is_game_over = False

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

            if event.key == pygame.K_SPACE and is_game_over:
                is_game_over = False
                pipe_list.clear() #empty the pipes
                bird_rect.center = (BIRD_X_LOCATION,HEIGHT/2) #recenter the bird
                bird_movement = 0

        if event.type == SPAWNPIPE:
            #create a new pipe and add it to the pipe_list
            pipe_list.extend(new_pipe(pipe_image,pipe_height))
            #print(pipe_list)
            #print("pipe" + str(i))

        if event.type == BIRDFLAP:
            if bird_index <2:
                bird_index+=1
            else:
                bird_index = 0

            bird_image,bird_rect = bird_animation(bird_frames,bird_index,bird_rect)

    # background
    screen.blit(background_surface, (0, 0))  # background image position at origin

    if not is_game_over:
        #bird
        bird_movement+= GRAVITY
        rotated_bird = rotate_bird(bird_image,bird_movement) #rotate the image of the bird
        bird_rect.centery += bird_movement #change the y position of the bird
        screen.blit(rotated_bird,bird_rect) #bird image

        #pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(screen,pipe_image,pipe_list)

        is_game_over = is_collision(bird_rect,pipe_list)

    #drawing the floor must be after drawing the bird and pipes so that the floor covers the pipe images.
    # draw the floor surface
    draw_floor(floorX_pos, floor_surface)
    floorX_pos -= 1  # move to the left

    if floorX_pos <= -WIDTH:  # keep moving the floor foreva
        floorX_pos = 0


    pygame.display.update() #simply redraws the image
    clock.tick(FPS) #runs 120 fps or slower

#end while