import pygame
from sys import exit
from random import randint
from pygame import mixer

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Space Invader')
icon = pygame.image.load(r"ufo.png").convert()
pygame.display.set_icon(icon)

space = pygame.image.load(r"space2.png").convert()

play = pygame.image.load(r"play5.png").convert_alpha()
play = pygame.transform.scale(play, (250, 125))
play_rect = play.get_rect(center = (400, 450))

#mixer.music.load(r"spaceinvaders_background.wav")
#mixer.music.play(-1)

player = pygame.image.load(r"spaceship1.png").convert_alpha()
player_rect = player.get_rect(topleft = (370, 480))
playerX_change = 0
playerY_change = 0

player_still = pygame.image.load(r"spaceship_bg.png").convert_alpha()
player_still = pygame.transform.scale(player_still, (300, 300))
player_still_rect = player_still.get_rect(center = (400, 300))

enemy = pygame.image.load(r"enemy.png").convert_alpha()
enemy_rect, enemyX_change, enemyY_change = [], [], []
num_enemies = 6

def enemy_pos (num_enemies):
    for i in range(num_enemies):
        enemy_rect.append(enemy.get_rect(topleft = (randint(0, 735), randint(50, 150))))
        enemyX_change.append(4)
        enemyY_change.append(40)

bullet = pygame.image.load(r"bullet.png").convert_alpha()
bullet_rect = bullet.get_rect(topleft = (-100, -100))
bulletY_change = 10
bullet_state = 'Ready'

text_font = pygame.font.Font('freesansbold.ttf', 40)

game_font = pygame.font.Font('freesansbold.ttf', 60)
game_name = game_font.render('SPACE INVADERS', True, (255, 255, 255))
game_name_rect = game_name.get_rect(center = (400, 50))

score_value = 0
rounds = 0
num_lives = 3

game_active = False
need_help = False

def display_score(x, y):
    score = text_font.render(f'Score : {score_value}', True, (255, 255, 255))
    screen.blit(score, (x, y))

def display_lives(x, y):
    lives = text_font.render(f'Lives : {num_lives}', True, (255, 255, 255))
    screen.blit(lives, (x, y))

def game_over_text():
    game_over = game_font.render(f'GAME OVER', True, (255, 255, 255))
    game_over_rect = game_over.get_rect(center = (400, 60))
    screen.blit(game_over, game_over_rect)

def player_movement ():
    screen.blit(player, player_rect)

def enemy_movement (i):
    screen.blit(enemy, enemy_rect[i])

def fire_bullet (x, y):
    global bullet_state
    bullet_state = 'Fire'
    screen.blit(bullet, (x + 16, y + 10))

def end_of_game(enemy_rect, player_rect):
    for i in range(num_enemies):
        if enemy_rect[i].colliderect(player_rect):
            return True
    return False

while True:

    screen.fill((0, 0, 0))
    screen.blit(space, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit
            exit()
        
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -5
                if event.key == pygame.K_RIGHT:
                    playerX_change = 5
                if event.key == pygame.K_UP:
                    playerY_change = -5
                if event.key == pygame.K_DOWN:
                    playerY_change = 5
                if event.key == pygame.K_SPACE: 
                    if bullet_state == 'Ready':
                        bullet_rect.topleft = player_rect.topleft
                        #bullet_sound = mixer.Sound(r"bullet.wav")
                        #bullet_sound.play()
                        fire_bullet(bullet_rect.left, bullet_rect.top)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    playerY_change = 0

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_rect.collidepoint(event.pos):
                game_active = True
                player_rect.topleft = (370, 480)
                enemy_rect.clear()
                enemyX_change.clear()
                enemyY_change.clear()
                enemy_pos(num_enemies)
                bullet_state = 'Ready'
                rounds = 0
                playerX_change = 0
                playerY_change = 0
                score_value = 0
            
    if game_active:
        rounds += 1
        player_movement()

        player_rect.left += playerX_change  
        if player_rect.left <= 0:
            player_rect.left = 0
        elif player_rect.right >= 800:
            player_rect.right = 800

        player_rect.top += playerY_change 
        if player_rect.top <= 0:
            player_rect.top = 0
        elif player_rect.bottom >= 600:
            player_rect.bottom = 600   

        for i in range(num_enemies):
            enemy_rect[i].left += enemyX_change[i]  
            if enemy_rect[i].left <= 0:
                enemyX_change[i] = 4
                enemy_rect[i].top += enemyY_change[i]
            elif enemy_rect[i].right >= 800:
                enemyX_change[i] = -4 
                enemy_rect[i].top += enemyY_change[i] 

            if enemy_rect[i].colliderect(bullet_rect):
                #collision_sound = mixer.Sound(r"explosion.wav")
                #collision_sound.play()
                bullet_rect.topleft = (-100, -100)
                bullet_state = 'Ready'
                enemy_rect[i].topleft = (randint(0, 735), randint(50, 150))
                score_value += 1

            enemy_movement(i)

        if bullet_rect.bottom < 0:
            bullet_rect.topleft = (-100, -100)
            if bullet_state == 'Fire':
                num_lives -= 1
            bullet_state = 'Ready'

        if bullet_state == 'Fire':
            fire_bullet(bullet_rect.left, bullet_rect.top)  
            bullet_rect.top -= bulletY_change

        display_score(10, 10)
        display_lives(600, 10)

        if end_of_game (enemy_rect, player_rect) or num_lives == 0:
            game_active = False

    elif not game_active and not need_help:
        screen.blit(player_still, player_still_rect)
        screen.blit(play, play_rect)
        if rounds == 0:
            screen.blit(game_name, game_name_rect)
        else:
            game_over_text()
            display_score(300, 90)

    pygame.display.update()
    clock.tick(60)
