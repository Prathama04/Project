import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 640, 640
TOWER_WIDTH = 20
TOWER_HEIGHT = 200
DISK_WIDTH = 50
DISK_HEIGHT = 20
FPS = 60

# Colors for Light Mode
LIGHT_MODE_BACKGROUND = (255, 255, 255)
LIGHT_MODE_TEXT = (0, 0, 0)
LIGHT_MODE_TOWER = (77, 206, 145)
LIGHT_MODE_PEG = (170, 170, 170)
LIGHT_MODE_DISK = (78, 162, 196)
LIGHT_MODE_POINTER = (255, 0, 0)

# Colors for Dark Mode
DARK_MODE_BACKGROUND = (0, 0, 0)
DARK_MODE_TEXT = (255, 255, 255)
DARK_MODE_TOWER = (0, 128, 0)
DARK_MODE_PEG = (80, 80, 80)
DARK_MODE_DISK = (255, 165, 0)
DARK_MODE_POINTER = (255, 255, 0)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Towers of Hanoi")
clock = pygame.time.Clock()

# Game variables
game_done = False
framerate = 60

# Game state
steps = 0
n_disks = 3
disks = []
towers_midx = [120, 320, 520]
pointing_at = 0
floating = False
floater = 0

# Fonts
font = pygame.font.SysFont("monospace", 30)

# Mode
current_mode = "light"

def draw_text(text, midtop, color):
    font_surface = font.render(text, True, color)
    font_rect = font_surface.get_rect()
    font_rect.midtop = midtop
    screen.blit(font_surface, font_rect)

def toggle_mode():
    global current_mode
    current_mode = "dark" if current_mode == "light" else "light"

def menu_screen():
    global n_disks, game_done, current_mode
    menu_done = False

    while not menu_done:
        if current_mode == "light":
            screen.fill(LIGHT_MODE_BACKGROUND)
            draw_text("Light Mode", (WIDTH // 2, 440), LIGHT_MODE_TEXT)
        else:
            screen.fill(DARK_MODE_BACKGROUND)
            draw_text("Dark Mode", (WIDTH // 2, 440), DARK_MODE_TEXT)

        draw_text('Towers of Hanoi', (WIDTH // 2, 120), LIGHT_MODE_TEXT if current_mode == "light" else DARK_MODE_TEXT)
        draw_text('Use arrow keys to select difficulty:', (WIDTH // 2, 220), LIGHT_MODE_TEXT if current_mode == "light" else DARK_MODE_TEXT)
        draw_text(str(n_disks), (WIDTH // 2, 260), LIGHT_MODE_TEXT if current_mode == "light" else DARK_MODE_TEXT)
        draw_text('Press ENTER to continue', (WIDTH // 2, 320), LIGHT_MODE_TEXT if current_mode == "light" else DARK_MODE_TEXT)
        draw_text('Press T to toggle mode', (WIDTH // 2, 380), LIGHT_MODE_TEXT if current_mode == "light" else DARK_MODE_TEXT)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    menu_done = True
                    game_done = True
                if event.key == pygame.K_RETURN:
                    menu_done = True
                if event.key in [pygame.K_RIGHT, pygame.K_UP]:
                    n_disks += 1
                    if n_disks > 6:
                        n_disks = 6
                if event.key in [pygame.K_LEFT, pygame.K_DOWN]:
                    n_disks -= 1
                    if n_disks < 1:
                        n_disks = 1
                if event.key == pygame.K_t:  # Toggle mode
                    toggle_mode()
                
            if event.type == pygame.QUIT:
                menu_done = True
                game_done = True

        pygame.display.flip()
        clock.tick(60)

def game_over():
    global steps
    if current_mode == "light":
        screen.fill(LIGHT_MODE_BACKGROUND)
    else:
        screen.fill(DARK_MODE_BACKGROUND)

    min_steps = 2**n_disks - 1
    draw_text('You Won!', (WIDTH // 2, 200), LIGHT_MODE_TEXT if current_mode == "light" else DARK_MODE_TEXT)
    draw_text('Your Steps: ' + str(steps), (WIDTH // 2, 360), LIGHT_MODE_TEXT if current_mode == "light" else DARK_MODE_TEXT)
    draw_text('Minimum Steps: ' + str(min_steps), (WIDTH // 2, 390), LIGHT_MODE_TEXT if current_mode == "light" else DARK_MODE_TEXT)
    if min_steps == steps:
        draw_text('You finished in minimum steps!', (WIDTH // 2, 300), LIGHT_MODE_TEXT if current_mode == "light" else DARK_MODE_TEXT)

    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    sys.exit()

def draw_towers():
    for xpos in range(40, 460+1, 200):
        pygame.draw.rect(screen, LIGHT_MODE_TOWER if current_mode == "light" else DARK_MODE_TOWER, pygame.Rect(xpos, 400, 160, 20))
        pygame.draw.rect(screen, LIGHT_MODE_PEG if current_mode == "light" else DARK_MODE_PEG, pygame.Rect(xpos+75, 200, 10, 200))
    draw_text('Start', (towers_midx[0], 403), LIGHT_MODE_TEXT if current_mode == "light" else DARK_MODE_TEXT)
    draw_text('Finish', (towers_midx[2], 403), LIGHT_MODE_TEXT if current_mode == "light" else DARK_MODE_TEXT)

def make_disks():
    global n_disks, disks
    disks = []
    height = 20
    ypos = 397 - height
    width = n_disks * 23
    for i in range(n_disks):
        disk = {'rect': pygame.Rect(0, 0, width, height),
                'val': n_disks - i,
                'tower': 0}
        disk['rect'].midtop = (120, ypos)
        disks.append(disk)
        ypos -= height + 3
        width -= 23

def draw_disks():
    for disk in disks:
        pygame.draw.rect(screen, LIGHT_MODE_DISK if current_mode == "light" else DARK_MODE_DISK, disk['rect'])

def draw_ptr():
    ptr_points = [(towers_midx[pointing_at]-7, 440),
                  (towers_midx[pointing_at]+7, 440),
                  (towers_midx[pointing_at], 433)]
    pygame.draw.polygon(screen, LIGHT_MODE_POINTER if current_mode == "light" else DARK_MODE_POINTER, ptr_points)

def check_won():
    over = all(disk['tower'] == 2 for disk in disks)
    if over:
        time.sleep(0.2)
        game_over()

def reset():
    global steps, pointing_at, floating, floater
    steps = 0
    pointing_at = 0
    floating = False
    floater = 0
    menu_screen()
    make_disks()

menu_screen()
make_disks()

while not game_done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                reset()
            if event.key == pygame.K_q:
                game_done = True
            if event.key == pygame.K_RIGHT:
                pointing_at = (pointing_at+1) % 3
                if floating:
                    disks[floater]['rect'].midtop = (towers_midx[pointing_at], 100)
                    disks[floater]['tower'] = pointing_at
            if event.key == pygame.K_LEFT:
                pointing_at = (pointing_at-1) % 3
                if floating:
                    disks[floater]['rect'].midtop = (towers_midx[pointing_at], 100)
                    disks[floater]['tower'] = pointing_at
            if event.key == pygame.K_UP and not floating:
                for disk in disks[::-1]:
                    if disk['tower'] == pointing_at:
                        floating = True
                        floater = disks.index(disk)
                        disk['rect'].midtop = (towers_midx[pointing_at], 100)
                        break
            if event.key == pygame.K_DOWN and floating:
                for disk in disks[::-1]:
                    if disk['tower'] == pointing_at and disks.index(disk) != floater:
                        if disk['val'] > disks[floater]['val']:
                            floating = False
                            disks[floater]['rect'].midtop = (towers_midx[pointing_at], disk['rect'].top - 23)
                            steps += 1
                        break
                else:
                    floating = False
                    disks[floater]['rect'].midtop = (towers_midx[pointing_at], 400-23)
                    steps += 1

            if event.key == pygame.K_t:  # Toggle mode
                toggle_mode()

    if current_mode == "light":
        screen.fill(LIGHT_MODE_BACKGROUND)
    else:
        screen.fill(DARK_MODE_BACKGROUND)

    draw_towers()
    draw_disks()
    draw_ptr()
    draw_text('Steps: ' + str(steps), (320, 20), LIGHT_MODE_TEXT if current_mode == "light" else DARK_MODE_TEXT)
    pygame.display.flip()

    if not floating:
        check_won()

    clock.tick(FPS)

