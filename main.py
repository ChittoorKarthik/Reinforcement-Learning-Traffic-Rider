import pygame
import time
import random
import numpy as np
import pickle
import os

pygame.init()
crash_sound = pygame.mixer.Sound("Sound Tracks/crash.wav")
m_sound = pygame.mixer.music.load("Sound Tracks/menusong.wav")
gray = (127, 127, 127)
black = (0, 0, 0)
red = (199, 38, 38)
green = (0, 200, 0)
blue = (52, 147, 201)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)
bright_blue = (0, 0, 255)
display_width = 800
display_height = 600
pause = False
gamedisplays = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("TraffIc RIder")
clock = pygame.time.Clock()
carimg = pygame.image.load('Vehicles/car1.jpg')
backgroundpic = pygame.image.load("Background images/download12.jpg")
yellow_strip = pygame.image.load("Background images/yellow strip.jpg")
strip = pygame.image.load("Background images/strip.jpg")
intro_background = pygame.image.load("Background images/intro_background.jpg")
instruction_background = pygame.image.load("Background images/instruction_background.jpg")
car_width = 56


# Define Q-table parameters
NUM_STATES = 3  # Car x-coordinate, obstacle x-coordinate, obstacle y-coordinate
NUM_ACTIONS = 3  # Left, Right, Stay
Q={}


# Define rewards
CRASH_REWARD = -10000000
PASS_REWARD = 1000      
NO_ACTION_REWARD = 1   # to make the car not move unncecessarily

# Check if the file exists
if os.path.exists('q_values.pkl'):
    # Load Q-values from the file
    with open('q_values.pkl', 'rb') as f:
        Q = pickle.load(f)
    print('Q-values loaded from the file')
    #print(Q[ (560, 470) ][ 0 ], " this is sample")
else:
    # Initialize Q-values
    Q = {}

    # Initialize Q-table with zeros
    for i in range(-display_width-10, display_width+10,5):
        for j in range(-display_width-10, display_width+10,5):
            #for k in range(-display_height-10, display_height+10,5):
            #    Q[(i, j, k)] = [0, 0, 0]  # Left, Right, Stay
            if i<=150:
                Q[(i, j)] = [CRASH_REWARD, 0, 0]  # Left, Right, Stay
            elif i>=550:
                Q[(i, j)] = [0, CRASH_REWARD, 0]  # Left, Right, Stay
            else:
                Q[(i, j)] = [0, 0, 0]  # Left, Right, Stay
    # Create the file and save the initial Q-values
    with open('q_values.pkl', 'wb') as f:
        pickle.dump(Q, f)
    print('Initial Q-values saved to the file')



# Define Q-learning parameters
LEARNING_RATE = 0.8
DISCOUNT_FACTOR = 0.9




def intro_loop():
    intro = True
    pygame.mixer.music.load("Sound Tracks/menusong.wav")
    pygame.mixer.music.play(-1)
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open('q_values.pkl', 'wb') as f:
                    print("Saved Q-values to file")
                    pickle.dump(Q, f)
                pygame.quit()
                quit()
                sys.exit()
        gamedisplays.blit(intro_background, (0, 0))
        largetext = pygame.font.SysFont('agencyfb', 115)
        textsurf, textrect = text_objects("TraffIC RIder", largetext)
        textrect.center = (400, 109)
        gamedisplays.blit(textsurf, textrect)
        button("START", 150, 520, 100, 50, green, bright_green, "play")
        button("QUIT", 550, 520, 100, 50, red, bright_red, "quit")
        button("INSTRUCTION", 300, 520, 200, 50, blue, bright_blue, "intro")
        pygame.display.update()
        clock.tick(50)


def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gamedisplays, ac, (x, y, w, h))
        if click[0] == 1 and action is not None:
            if action == "play":
                countdown()
            elif action == "quit":
                with open('q_values.pkl', 'wb') as f:
                    print("Saved Q-values to file")
                    pickle.dump(Q, f)
                pygame.quit()
                quit()
                sys.exit()
            elif action == "intro":
                introduction()
            elif action == "menu":
                intro_loop()
            elif action == "pause":
                paused()
            elif action == "unpause":
                unpaused()

    else:
        pygame.draw.rect(gamedisplays, ic, (x, y, w, h))
    smalltext = pygame.font.Font("freesansbold.ttf", 20)
    textsurf, textrect = text_objects(msg, smalltext)
    textrect.center = ((x + (w / 2)), (y + (h / 2)))
    gamedisplays.blit(textsurf, textrect)


def introduction():
    introduction = True
    while introduction:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open('q_values.pkl', 'wb') as f:
                    print("Saved Q-values to file")
                    pickle.dump(Q, f)
                pygame.quit()
                quit()
                sys.exit()
        gamedisplays.blit(instruction_background, (0, 0))
        largetext = pygame.font.Font('freesansbold.ttf', 80)
        smalltext = pygame.font.Font('freesansbold.ttf', 20)
        mediumtext = pygame.font.Font('freesansbold.ttf', 40)
        textSurf, textRect = text_objects("This is a car game in which you need to dodge the coming cars", smalltext)
        textRect.center = ((350), (200))
        TextSurf, TextRect = text_objects("INSTRUCTION", largetext)
        TextRect.center = ((400), (100))
        gamedisplays.blit(TextSurf, TextRect)
        gamedisplays.blit(textSurf, textRect)
        stextSurf, stextRect = text_objects("ARROW LEFT : LEFT TURN", smalltext)
        stextRect.center = ((150), (400))
        hTextSurf, hTextRect = text_objects("ARROW RIGHT : RIGHT TURN", smalltext)
        hTextRect.center = ((150), (450))
        atextSurf, atextRect = text_objects("ARROW UP : ACCELERATOR", smalltext)
        atextRect.center = ((150), (500))
        rtextSurf, rtextRect = text_objects("ARROW DOWN : BRAKE ", smalltext)
        rtextRect.center = ((150), (550))
        ptextSurf, ptextRect = text_objects("P : PAUSE  ", smalltext)
        ptextRect.center = ((150), (350))
        sTextSurf, sTextRect = text_objects("CONTROLS", mediumtext)
        sTextRect.center = ((350), (300))
        gamedisplays.blit(sTextSurf, sTextRect)
        gamedisplays.blit(stextSurf, stextRect)
        gamedisplays.blit(hTextSurf, hTextRect)
        gamedisplays.blit(atextSurf, atextRect)
        gamedisplays.blit(rtextSurf, rtextRect)
        gamedisplays.blit(ptextSurf, ptextRect)
        button("BACK", 600, 450, 100, 50, blue, bright_blue, "menu")
        pygame.display.update()
        clock.tick(30)


def paused():
    pygame.mixer.music.pause()
    pygame.mixer.music.load("Sound Tracks/menusong.wav")
    pygame.mixer.music.play(-1)
    global pause
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open('q_values.pkl', 'wb') as f:
                    print("Saved Q-values to file")
                    pickle.dump(Q, f)
                pygame.quit()
                quit()
                sys.exit()
        gamedisplays.blit(instruction_background, (0, 0))
        largetext = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("PAUSED", largetext)
        TextRect.center = ((display_width / 2), (display_height / 2))
        gamedisplays.blit(TextSurf, TextRect)
        button("CONTINUE", 150, 450, 150, 50, green, bright_green, "unpause")
        button("RESTART", 350, 450, 150, 50, blue, bright_blue, "play")
        button("MAIN MENU", 550, 450, 200, 50, red, bright_red, "menu")
        pygame.display.update()
        clock.tick(30)


def unpaused():
    global pause
    pygame.mixer.music.pause()
    pygame.mixer.music.load("Sound Tracks/backgroundmusic.wav")
    pygame.mixer.music.play(-1)
    pause = False


def countdown_background():
    font = pygame.font.SysFont(None, 25)
    x = (display_width * 0.45)
    y = (display_height * 0.8)
    gamedisplays.blit(backgroundpic, (0, 0))
    gamedisplays.blit(backgroundpic, (0, 200))
    gamedisplays.blit(backgroundpic, (0, 400))
    gamedisplays.blit(backgroundpic, (700, 0))
    gamedisplays.blit(backgroundpic, (700, 200))
    gamedisplays.blit(backgroundpic, (700, 400))
    gamedisplays.blit(yellow_strip, (400, 100))
    gamedisplays.blit(yellow_strip, (400, 200))
    gamedisplays.blit(yellow_strip, (400, 300))
    gamedisplays.blit(yellow_strip, (400, 400))
    gamedisplays.blit(yellow_strip, (400, 100))
    gamedisplays.blit(yellow_strip, (400, 500))
    gamedisplays.blit(yellow_strip, (400, 0))
    gamedisplays.blit(yellow_strip, (400, 600))
    gamedisplays.blit(strip, (120, 200))
    gamedisplays.blit(strip, (120, 0))
    gamedisplays.blit(strip, (120, 100))
    gamedisplays.blit(strip, (680, 100))
    gamedisplays.blit(strip, (680, 0))
    gamedisplays.blit(strip, (680, 200))
    gamedisplays.blit(carimg, (x, y))
    text = font.render("VEHICLE DODGED: 0", True, (0, 0, 255))
    score = font.render("SCORE: 0", True, (255, 0, 0))
    level = font.render("LEVEL: 0", True, (0, 255, 0))
    gamedisplays.blit(level, (0, 50))
    gamedisplays.blit(text, (0, 30))
    gamedisplays.blit(score, (0, 10))
    button("PAUSE", 650, 0, 150, 50, blue, bright_blue, "pause")


def countdown():
    countdown = True

    while countdown:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open('q_values.pkl', 'wb') as f:
                    print("Saved Q-values to file")
                    pickle.dump(Q, f)
                pygame.quit()
                quit()
                sys.exit()
        gamedisplays.fill(gray)
        countdown_background()
        largetext = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("3", largetext)
        TextRect.center = ((display_width / 2), (display_height / 2))
        gamedisplays.blit(TextSurf, TextRect)
        pygame.display.update()
        clock.tick(1)
        gamedisplays.fill(gray)
        countdown_background()
        largetext = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("2", largetext)
        TextRect.center = ((display_width / 2), (display_height / 2))
        gamedisplays.blit(TextSurf, TextRect)
        pygame.display.update()
        clock.tick(1)
        gamedisplays.fill(gray)
        countdown_background()
        largetext = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("1", largetext)
        TextRect.center = ((display_width / 2), (display_height / 2))
        gamedisplays.blit(TextSurf, TextRect)
        pygame.display.update()
        clock.tick(1)
        gamedisplays.fill(gray)
        countdown_background()
        largetext = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("GO!!!", largetext)
        TextRect.center = ((display_width / 2), (display_height / 2))
        gamedisplays.blit(TextSurf, TextRect)
        pygame.display.update()
        clock.tick(1)
        game_loop()


def obstacle(obs_startx, obs_starty, obs):
    if obs == 0:
        obs_pic = pygame.image.load("Vehicles/car.jpg")
    elif obs == 1:
        obs_pic = pygame.image.load("Vehicles/car1.jpg")

    elif obs == 2:
        obs_pic = pygame.image.load("Vehicles/car2.jpg")

    elif obs == 3:
        obs_pic = pygame.image.load("Vehicles/car4.jpg")

    elif obs == 4:
        obs_pic = pygame.image.load("Vehicles/car5.jpg")

    elif obs == 5:
        obs_pic = pygame.image.load("Vehicles/car6.jpg")

    elif obs == 6:
        obs_pic = pygame.image.load("Vehicles/car7.jpg")

    elif obs == 7:
        obs_pic = pygame.image.load("Vehicles/car8.jpg")

    elif obs == 8:
        obs_pic = pygame.image.load("Vehicles/bike1.jpg")

    elif obs == 9:
        obs_pic = pygame.image.load("Vehicles/bike2.jpg")

    elif obs == 10:
        obs_pic = pygame.image.load("Vehicles/bike3.jpg")

    elif obs == 11:
        obs_pic = pygame.image.load("Vehicles/car9.jpg")

    elif obs == 12:
        obs_pic = pygame.image.load("Vehicles/car10.jpg")

    elif obs == 13:
        obs_pic = pygame.image.load("Vehicles/car11.jpg")

    gamedisplays.blit(obs_pic, (obs_startx, obs_starty))


def score_system(passed, score, level):
    font = pygame.font.SysFont(None, 25)
    text = font.render("VEHICLE DODGED :" + str(passed), True, (0, 0, 255))
    score = font.render("SCORE :" + str(score), True, (255, 0, 0))
    level = font.render("LEVEL :" + str(level), True, (0, 255, 0))
    gamedisplays.blit(text, (0, 30))
    gamedisplays.blit(score, (0, 10))
    gamedisplays.blit(level, (0, 50))


def text_objects(text, font):
    textsurface = font.render(text, True, black)
    return textsurface, textsurface.get_rect()


def message_display(text):
    largetext = pygame.font.Font("freesansbold.ttf", 80)
    textsurf, textrect = text_objects(text, largetext)
    textrect.center = ((display_width / 2), (display_height / 2))
    gamedisplays.blit(textsurf, textrect)
    pygame.display.update()
    time.sleep(3)
    game_loop()


def crash():
    pygame.mixer.Sound.play(crash_sound)
    pygame.mixer.music.stop()
    message_display("YOU CRASHED")
    print("crashed")
    # Save updated Q-values back to the file
    with open('q_values.pkl', 'wb') as f:
        print("Saved Q-values to file")
        pickle.dump(Q, f)
    pygame.quit()
    quit()


def background():
    gamedisplays.blit(backgroundpic, (0, 0))
    gamedisplays.blit(backgroundpic, (0, 200))
    gamedisplays.blit(backgroundpic, (0, 400))
    gamedisplays.blit(backgroundpic, (700, 0))
    gamedisplays.blit(backgroundpic, (700, 200))
    gamedisplays.blit(backgroundpic, (700, 400))
    gamedisplays.blit(yellow_strip, (400, 0))
    gamedisplays.blit(yellow_strip, (400, 100))
    gamedisplays.blit(yellow_strip, (400, 200))
    gamedisplays.blit(yellow_strip, (400, 300))
    gamedisplays.blit(yellow_strip, (400, 400))
    gamedisplays.blit(yellow_strip, (400, 500))
    gamedisplays.blit(strip, (120, 200))
    gamedisplays.blit(strip, (120, 0))
    gamedisplays.blit(strip, (120, 100))
    gamedisplays.blit(strip, (680, 100))
    gamedisplays.blit(strip, (680, 0))
    gamedisplays.blit(strip, (680, 200))


def car(x, y):
    gamedisplays.blit(carimg, (x, y))

#############################################


def choose_action(state, epsilon):
        """
        Epsilon-greedy action selection
        """
    # if random.uniform(0, 1) < epsilon:
    #     return random.choice([0, 1, 2])  # Left, Right, Stay
    # else:
        max_q_value = max(Q[state])
        max_indices = [i for i, q_value in enumerate(Q[state]) if q_value == max_q_value]
        return random.choice(max_indices)
        return Q[state].index(max(Q[state]))


def get_state(car_x, obs_x):
    """
    Get the current state based on car x-coordinate, obstacle x-coordinate, and obstacle y-coordinate
    """
    car_x_rounded = round(car_x / 5) * 5
    obs_x_rounded = round(obs_x / 5) * 5
    return car_x_rounded, obs_x_rounded
    #return car_x, obs_x, obs_y

def update_q_table(state, action, reward, next_state):
    """
    Update Q-value in the Q-table
    """
    #print("got state: ", state)
    current_q_value = Q[state][action]
    max_future_q_value = max(Q[next_state])

    # Q-learning update rule - THE HEART OF THE ALGORITHM
    new_q_value = (1 - LEARNING_RATE) * current_q_value + LEARNING_RATE * (reward + DISCOUNT_FACTOR * max_future_q_value)

    Q[state][action] = new_q_value
    #print("updated Q[", state, "][", action, "] = ", new_q_value," l:",Q[state][0]," r:",Q[state][1]," S:",Q[state][2])

################################################

def game_loop():
    #global Q
    #print(Q[(360,450,-750)]," xxx")
    global pause
    pygame.mixer.music.load("Sound Tracks/backgroundmusic.wav")
    pygame.mixer.music.play(-1)
    x = (display_width * 0.45)
    y = (display_height * 0.8)
    x_change = 0
    obstacle_speed = 9
    obs = 0
    y_change = 0
    obs_startx = round(random.randrange(200, (display_width - 200)) / 5) * 5   #rounding off to ensure obstacles are in lanes

    obs_starty = -750
    obs_width = 56
    obs_height = 125
    passed = 0
    level = 0
    score = 0
    y2 = 7
    fps = 120
    bumped = False
    while not bumped:
        state=(0,0)
        reward=0
        next_state=(0,0)
        action=2
        
        # Choose action
        state = get_state(x, obs_startx)
        #print("sent state: ", state)
        action=1
        action = choose_action(state, epsilon=0.1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Save updated Q-values back to the file
                with open('q_values.pkl', 'wb') as f:
                    print("Saved Q-values to file")
                    pickle.dump(Q, f)

                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    action = 0
                if event.key == pygame.K_RIGHT:
                    action = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    action = 2

        # Perform action
        if action == 0:  # Left
                x_change = -50
        elif action == 1:  # Right
                x_change = 50
        else:  # Stay
                x_change = 0

        x += x_change

        x=min(x,display_width)
        x=max(x,-display_width)

        #print("car:(", x, ",", y, ") obstacle:(", obs_startx, ",", obs_starty, ")")

        reward = NO_ACTION_REWARD
        if bumped:
                reward = CRASH_REWARD
        elif passed > 0:
                reward = PASS_REWARD

        # Update Q-table
        next_state = get_state(x, obs_startx)
        update_q_table(state, action, reward, next_state)

        gamedisplays.fill(gray)
        rel_y = y2 % backgroundpic.get_rect().width
        gamedisplays.blit(backgroundpic, (0, rel_y - backgroundpic.get_rect().width))
        gamedisplays.blit(backgroundpic, (700, rel_y - backgroundpic.get_rect().width))
        if rel_y < 800:
            gamedisplays.blit(backgroundpic, (0, rel_y))
            gamedisplays.blit(backgroundpic, (700, rel_y))
            gamedisplays.blit(yellow_strip, (400, rel_y))
            gamedisplays.blit(yellow_strip, (400, rel_y + 100))
            gamedisplays.blit(yellow_strip, (400, rel_y + 200))
            gamedisplays.blit(yellow_strip, (400, rel_y + 300))
            gamedisplays.blit(yellow_strip, (400, rel_y + 400))
            gamedisplays.blit(yellow_strip, (400, rel_y + 500))
            gamedisplays.blit(yellow_strip, (400, rel_y - 100))
            gamedisplays.blit(strip, (120, rel_y - 200))
            gamedisplays.blit(strip, (120, rel_y + 20))
            gamedisplays.blit(strip, (120, rel_y + 30))
            gamedisplays.blit(strip, (680, rel_y - 100))
            gamedisplays.blit(strip, (680, rel_y + 20))
            gamedisplays.blit(strip, (680, rel_y + 30))

        y2 += obstacle_speed
        obs_starty -= (obstacle_speed / 4)
        obstacle(obs_startx, obs_starty, obs)
        obs_starty += obstacle_speed
        car(x, y)
        score_system(passed, score, level)
        if x > 690 - car_width or x < 110:
            update_q_table(state, action, CRASH_REWARD, next_state)
            crash()
            
        if x > display_width - (car_width + 110) or x < 110:
            update_q_table(state, action, CRASH_REWARD, next_state)
            crash()
            
        if obs_starty > display_height:
            obs_starty = 0 - obs_height
            obs_startx = random.randrange(170, (display_width - 170))
            obs = random.randrange(0, 14)
            passed = passed + 1
            score = passed * 10
            if int(passed) % 10 == 0:
                level = level + 1
                obstacle_speed = obstacle_speed + 2
                largetext = pygame.font.Font("freesansbold.ttf", 80)
                textsurf, textrect = text_objects("LEVEL" + str(level), largetext)
                textrect.center = ((display_width / 2), (display_height / 2))
                gamedisplays.blit(textsurf, textrect)
                pygame.display.update()
                time.sleep(3)
        if y < obs_starty + obs_height:
            if x > obs_startx and x < obs_startx + obs_width or x + car_width > obs_startx and x + car_width < obs_startx + obs_width:
                update_q_table(state, action, CRASH_REWARD, next_state)
                crash()
                
        pygame.display.update()
        clock.tick(60)


intro_loop()
# Save updated Q-values back to the file
with open('q_values.pkl', 'wb') as f:
    print("Saved Q-values to file")
    pickle.dump(Q, f)

pygame.quit()
quit()