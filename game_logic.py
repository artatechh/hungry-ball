# ARTATECHH
import pygame
import random
import sys
import time
import copy 
pygame.init()
pygame.display.set_caption("hungry ball")

# Screen
width, height = 700 , 800
main_screen = pygame.display.set_mode((width, height))

# All Variable


sound, sound2 = True, True
back_sound = pygame.mixer.Sound('data/back.wav')
point_sound = pygame.mixer.Sound('data/25.wav')
over_sound = pygame.mixer.Sound('data/gameover.wav')
eat_sound = pygame.mixer.Sound('data/eat.wav')
wall_l = []
foodl = []
score = 0
high_score = 0
game_status = True
x = 600
y = 339
font = pygame.font.Font('data/font.otf', 50)
active = True
speed = 130

# All image
background_img = pygame.image.load('data/backgame.png')
wall = pygame.image.load('data/wall.png')
food = pygame.image.load('data/food.png')
game_over = pygame.image.load('data/gameover.png')

# timer wall
wall_timer = pygame.USEREVENT
pygame.time.set_timer(wall_timer, 1000)
food_timer = pygame.USEREVENT + 1
pygame.time.set_timer(food_timer, 400)

# wall 
def generate_wall_rect():
    randomx = random.randrange(100, 600)
    wall_rect_left = wall.get_rect(midleft=(randomx, 0))
    wall_rect_right = wall.get_rect(midright=(randomx - 170, 0))
    return wall_rect_right, wall_rect_left


def move_wall(wall_l):
    for wall in wall_l:
        wall.centery += 4
    inside_wall = [wall for wall in wall_l if wall.bottom > 1]
    return inside_wall

def generate_food():
    randomx = random.randrange(100, 600)
    food_rect = food.get_rect(center=(randomx, 80))
    return food_rect

def move_food(foodl):
    for food in foodl:
        food.centery += 4
    inside_food = [food for food in foodl if food.centery < 650]
    return inside_food

# change character
def char(score : int) -> int:
    global sound, sound2
    if score >= 0 and score < 25:
        character_img = pygame.image.load('data/ct1.png')
    elif score >= 25 and score < 50 :
        character_img = pygame.image.load('data/ct2.png')
        if sound:
            point_sound.play()
            sound = False
    elif score >= 50 :
        character_img = pygame.image.load('data/ct3.png')
        if sound2:
            point_sound.play()
            sound2 = False

    return character_img
        
def checkgame():
    global active
    for wall in wall_l:
        if character_rect.colliderect(wall):
            over_sound.play()
            time.sleep(0.5)
            active = True
            return False
        if character_rect.centerx > 698 or character_rect.centerx < 6:
            over_sound.play()
            time.sleep(0.5)
            active = True
            return False
    return True

def display_score():
    global score, active, high_score, datas
    if foodl:
        for foods in foodl:
            if character_rect.colliderect(foods) and active == True:
                eat_sound.play()
                score += 1
                active = False 
            elif foods.centery > 640:
                active = True
    if score > high_score :
        high_score = score
        
    return score

# Game Timer
clock = pygame.time.Clock()
back_sound.play(-1)
# Game Logic

while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == wall_timer:
            wall_l.extend(generate_wall_rect())
        if event.type == food_timer:
            foodl.append(generate_food())

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and game_status == False:
                game_status = True
                foodl.clear()
                wall_l.clear() 
                speed = 130
                score = 0
                y = 339
    
    # Displaying background image
    main_screen.blit(background_img, (0, 0))
    
    if game_status:

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            y += 7.5
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            y -= 7.5
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if keys[pygame.K_SPACE] or keys[pygame.K_w]:
                y += 4
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if keys[pygame.K_SPACE] or keys[pygame.K_w]:
                y -= 4

        # displaying wall
        wall_l = move_wall(wall_l)
        for i in wall_l:
            main_screen.blit(wall, i)
        
        
        foodl = move_food(foodl)
        for i in foodl:
            main_screen.blit(food, i)


        character_img = char(score)
        character_rect = character_img.get_rect(center=(y, x))
        main_screen.blit(character_img, character_rect)
        text1 = font.render(f'{score}', False, (255, 255, 255))
        text1_rect = text1.get_rect(center=(345, 100))
        main_screen.blit(text1, text1_rect)
        if score >= 50 and score < 100:
            speed = 160
        elif score >= 100:
            speed = 170
        game_status = checkgame()
        display_score()
        
            
        

    else:
        main_screen.blit(game_over, (0, 0))
        text2 = font.render(f'high score {high_score}', False, (255, 255, 255))
        text2_rect = text2.get_rect(center=(345, 700))
        main_screen.blit(text2, text2_rect)
    pygame.display.update()
    # speed FPS
    clock.tick(speed)