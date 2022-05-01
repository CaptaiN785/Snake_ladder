import pygame
import random

# Initializing pygame
pygame.init()

# displaying the screen.
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Snake Ladder")

# Loading board image
board = pygame.image.load('image1.jpg') # loading background image of snake ladder
board = pygame.transform.smoothscale(board, (600, 600))

# Loading red button
red_button = pygame.image.load('red.png')
red_button = pygame.transform.smoothscale(red_button, (50, 50))
red_position = 1
last_blue_position = 1

# Loading blue button
blue_button = pygame.image.load('blue.png')
blue_button = pygame.transform.smoothscale(blue_button, (50, 50))
blue_position = 1
last_red_position = 1

# Loading side panel background
side_background = pygame.image.load('cityskyline.png')

# dice_rolll image 
dice_roll_image = pygame.image.load('roll_dice.png')
dice_roll_image = pygame.transform.smoothscale(dice_roll_image, (100, 40))

# Loading sounds 
dice_roll_sound = pygame.mixer.Sound('dice_roll.mp3')
snake_bite_sound = pygame.mixer.Sound('hiss.mp3')
ladder_up_sound = pygame.mixer.Sound('ladder.wav')



# Defining font
font = pygame.font.Font('freesansbold.ttf', 32)
big_font = pygame.font.Font('freesansbold.ttf', 100)

# Defining snake head and tails
head = [17, 54, 62, 64, 87, 93, 95, 98]
tail = [7, 34, 19, 60, 36, 73, 75, 79] 

# Defining ladder top and bottom

top = [99, 91, 84, 67, 42, 38, 31, 14]
bottom = [80, 72, 28, 51, 21, 1, 9, 4]

# Definining path of buttons
path = [0]
startX = 0      # x = 0
startY = 540    # y = 540 so that it starts from 0 of board.
unit = 60  
for i in range(10):
    if i%2 == 0: # when in 0, 2, 4, 6, 8 go right 
        for _ in range(10):
            path.append((startX+5, startY+5))
            startX += unit
        startX = 540
    else:
        for _ in range(10):
            path.append((startX+5, startY+5))
            startX -= unit
        startX = 0
    startY -= unit


running = True
############################################################################
# Loading dice image
dice = []
dice.append(0)
for i in range(1, 7):
    d = pygame.image.load('dices/'+str(i)+'.png')
    dice.append(d)

#######################################################################

def draw_user_dice(index):
    screen.blit(dice[index], (668, 440))

def draw_comp_dice(index):
    screen.blit(dice[index], (668, 90))

def draw_comp_outcome(tt):
    txt = font.render(str(tt), False, (255, 0, 255), None)
    screen.blit(txt, (680, 160))

def draw_user_outcome(tt):
    txt = font.render(str(tt), False, (255, 0, 255), None)
    screen.blit(txt, (680, 400))

def comp_turn():
    pygame.draw.rect(screen, (0, 255, 0), (650, 10, 100, 40))

def user_turn():
    screen.blit(dice_roll_image, (650, 550))
    rect = dice_roll_image.get_rect()
    rect.topleft = (650, 550)

    total = 0
    clicked = False

    # mouse position
    mouse_pressed = False
    pos = pygame.mouse.get_pos()
    if rect.collidepoint(pos) == 1 and mouse_pressed == False:
        if pygame.mouse.get_pressed()[0] == 1:
            mouse_pressed = True
            dice_roll_sound.play()
            clicked = True
            total = random.randint(1, 6)

        if pygame.mouse.get_pressed()[0] == False:
            mouse_pressed = False
    
    return clicked, total

def draw_red(pos):
    screen.blit(red_button, pos)

def draw_blue(pos):
    screen.blit(blue_button, pos)

def draw_both(red_position, blue_position):
    if blue_position == red_position:
        draw_red((path[red_position][0]+5, path[red_position][1]))
        draw_blue((path[red_position][0]-5, path[red_position][1]))
    else:
        draw_red(path[red_position])
        draw_blue(path[blue_position])

def comp_roll_dice():
    draw_both(red_position, blue_position)
    dice_roll_sound.play()

    number = random.randint(1, 6)
    total = number
    draw_comp_dice(number)

    pygame.display.update()
    pygame.time.wait(500)
    while number == 6:
        dice_roll_sound.play()
        number = random.randint(1, 6)
        total += number
        draw_comp_dice(number)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.time.wait(400) # waiting for next turns.

    total = total%18
    draw_comp_outcome(total)
    pygame.display.update()
    return total

def draw_text(txt, x, y):
    string = font.render(txt, False, (255, 0, 255), None)   
    screen.blit(string, (x, y))

userTurn = True
compTurn = True

# initialy inside the cage.
red_open = False
blue_open = False

user_dice_rolled = 0
dice_number = 0
outcome = 1
while running:
    # drawing board on screen
    screen.fill((0, 0, 0))
    screen.blit(board, (0, 0))
    screen.blit(side_background, (600, 0))
    
    draw_text("Computer", 620, 50)
    draw_text("You", 670, 520)

    if compTurn:
        comp_turn()
        draw_both(red_position, blue_position)
        pygame.display.update()
        pygame.time.delay(1000)
        dice_number = comp_roll_dice()

        if red_open == False and dice_number >= 6:
            dice_number -= 6
            red_open = True

        if red_position+dice_number <= 100 and red_open:
            red_position += dice_number
            if blue_position == red_position:
                draw_red((path[red_position][0]+5, path[red_position][1]))
            else:
                draw_red(path[red_position])
            
            pygame.display.update()
            pygame.time.delay(400)

            for i, val in enumerate(head):
                if val == red_position:
                    snake_bite_sound.play()
                    red_position = tail[i]

            for i, val in enumerate(bottom):
                if val == red_position:
                    ladder_up_sound.play()
                    red_position = top[i]

            draw_both(red_position, blue_position)
            pygame.display.update()
            pygame.time.delay(500)
        userTurn = True
        compTurn = False

    if userTurn:
        draw_both(red_position, blue_position)
        clicked, dice_number = user_turn()
        user_dice_rolled += dice_number
        
        if clicked:
            outcome = dice_number

        if user_dice_rolled > 0:
            draw_user_dice(outcome)
            draw_user_outcome(user_dice_rolled)
            pygame.display.update()
            if clicked:
                pygame.time.delay(500)

        if clicked and dice_number != 6:
            dice_number = user_dice_rolled%18
            if blue_open == False and dice_number >= 6:
                dice_number -= 6
                blue_open = True

            if blue_position+dice_number <= 100 and blue_open: # checking if it is out of range
                blue_position += dice_number
                if red_position == blue_position:
                    draw_blue((path[blue_position][0]-5, path[blue_position][1]))
                else:
                    draw_blue(path[blue_position])
                
                pygame.time.delay(500)

                for i, val in enumerate(head):
                    if val == blue_position:
                        snake_bite_sound.play()
                        blue_position = tail[i]

                for i, val in enumerate(bottom):
                    if val == blue_position:
                        ladder_up_sound.play()
                        blue_position = top[i]
                
                draw_both(red_position, blue_position)
            pygame.display.update()
            pygame.time.delay(500)
            user_dice_rolled = 0
            userTurn = False
            compTurn = True



    # Checking the events in pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_both(red_position, blue_position)

    if blue_position == 100 or red_position == 100:
        running = False

    last_blue_position = blue_position
    last_red_position = red_position
    pygame.display.update()

##################  After match over    #######################

running = True
while running:
    screen.fill((0, 0, 0))
    if red_position > blue_position:
        txt = big_font.render("Computer won.", False, (255, 0, 0), None)
        screen.blit(txt, (50, 250))
    else:
        txt = big_font.render("You won.", False, (0, 255, 0), None)
        screen.blit(txt, (200,250))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False