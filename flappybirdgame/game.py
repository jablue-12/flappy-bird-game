import pygame,sys,random,sqlite3

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
PIPE_DISTANCE = 200 #gap where the bird has to go through
PIPE_SPAWN_TIME = 1500 #in mseconds

#Mouse event
LEFT = 1 #left click


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
            #print("collision occured against the pipe")
            return True

        if bird_rect.top<= -50 or bird_rect.bottom >= 600:
            #-50 so that bird can still go above the origin.
            #(HEIGHT / 2) + (HEIGHT / 3) is the height of the floor
            #print("collision occured against the ceiling or bottom")
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

#score_display function
#function that displays the current score of the user.
#game_font parameter is the font style of the game.
#score parameter is the current score in integer.
#high_score parameter is the highest score displayed once the game is over.
#is_game_over parameter is a boolean variable. If its true then we display the high score.
def score_display(game_font,score,high_score,is_game_over):

    if is_game_over:
        #current score
        score_surface = game_font.render("Score:" + str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(WIDTH/2, 150))  # 100 px away from the screen
        screen.blit(score_surface, score_rect)  # display the score

        #display play again image
        game_over_surface = pygame.image.load('assets/message.png').convert_alpha()
        game_over_rect = game_over_surface.get_rect(center=(WIDTH/2,HEIGHT/2))
        #game_over_surface = pygame.transform.scale(game_over_surface, (WIDTH, HEIGHT))
        screen.blit(game_over_surface, game_over_rect)

        # highest score
        high_score_surface = game_font.render("High score: " + str(int(high_score)), True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(WIDTH / 2, 550))  # 100 px away from the screen
        screen.blit(high_score_surface, high_score_rect)  # display the score


    else:
        # current score
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(WIDTH/2, 100))  # 100 px away from the screen
        screen.blit(score_surface, score_rect)  # display the score

#end score_display function

#update_high_score function
#function that compares the current score and highest score and return which score is the highest.
def update_high_score(new_score,current_high_score):
    if new_score > current_high_score:
        return new_score
    else:
        return current_high_score
#end update_high_score function

#add_score function
#function that adds the score to the database. (need to modify such that there are users in the db)
def add_score(user,score):

    try:
        connection = sqlite3.connect("game-scores.db") #connect to db
        #create a table if it has not been created yet.
        connection.execute("""
            Create table if not exists scores(
            score_id integer primary key autoincrement,
            user_name text,
            user_score integer
            );""")
        # Add the data
        connection.execute("insert into scores(user_name, user_score) values (?,?)", (user, score))
        #write to disk
        connection.commit()
        #close the connection
        connection.close()
    except Exception as e:
        print(e)
#end add_score function

#get_high_scrore function
#function that gets the highest score from the database.
def get_high_score():
    highest_score = 0

    try:
        connection = sqlite3.connect("game-scores.db")  # connect to db
        # create a table if it has not been created yet.
        connection.execute("""
            Create table if not exists scores(
            score_id integer primary key autoincrement,
            user_name text,
            user_score integer
            );""")

        # read the data
        print("Reading db...")
        for row in connection.execute("select score_id,user_name,MAX(user_score) from scores"):
            if row[2] != None:
                score_id = row[0]
                username = row[1]
                highest_score = row[2]
                print(score_id,username,highest_score)

        print("done reading..")
        # close the connection
        connection.close()
    except Exception as e:
        print(e)

    return highest_score
#end get_high_Score function

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
score = 0 #current score
high_score = 0 #highest score
game_font = pygame.font.Font('04B_19.TTF',40)

while True: #run foreva
    for event in pygame.event.get(): #check what event is happening
        if event.type == pygame.QUIT:
            #exit pygame
            pygame.quit()
            sys.exit() # shuts down the game

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_game_over: #spacebar is clicked
                #want to move the bird up. Decrease value of bird_movement
                bird_movement = 0 #ignore the gravity so that the speed going up is constant.
                bird_movement -= MOVE_BIRD_UP
                #print("move up bird!")

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT and is_game_over:
            #press left button of the mouse to restart the game.
            #add scores to db first before resetting the variables
            #add_score("jared",int(score))

            #reset variables
            is_game_over = False
            pipe_list.clear() #empty the pipes
            bird_rect.center = (BIRD_X_LOCATION,HEIGHT/2) #recenter the bird
            bird_movement = 0
            score = 0  # reset current score to 0

        if event.type == SPAWNPIPE:
            #create a new pipe and add it to the pipe_list
            pipe_list.extend(new_pipe(pipe_image,pipe_height))
            #print(pipe_list)
            #print("pipe" + str(i))

        if event.type == BIRDFLAP:
            #wings animation for the bird.
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
        score += 0.01
        is_game_over = is_collision(bird_rect,pipe_list)
        #score_display(game_font,score,high_score,is_game_over)
    else:
        print("in the else")
        high_score = get_high_score()  # get the highest score from the db.
        if high_score == 0: #nothing in db yet, then set high_score to the current score
            high_score = score

    #drawing the floor must be after drawing the bird and pipes so that the floor covers the pipe images.
    # draw the floor surface
    draw_floor(floorX_pos, floor_surface)
    floorX_pos -= 1  # move to the left

    if floorX_pos <= -WIDTH:  # keep moving the floor foreva
        floorX_pos = 0

    # display the score after the game is over to show the highest score

    high_score = update_high_score(score, high_score) #compare the new score to the highest score
    score_display(game_font, score, high_score, is_game_over)

    pygame.display.update() #simply redraws the image
    clock.tick(FPS) #runs 120 fps or slower

#end while