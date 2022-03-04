import random, pygame, sys
from pygame.locals import *

FPS = 15
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # syntactic sugar: index of the worm's head

APPLE_IMAGE = pygame.transform.scale(pygame.image.load(r'./apple.png'), (CELLSIZE, CELLSIZE))
ORANGE_IMAGE = pygame.transform.scale(pygame.image.load(r'./orange.png'), (CELLSIZE, CELLSIZE))
FRUITS_IMAGES = [APPLE_IMAGE, ORANGE_IMAGE]
BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load(r'./background.png'), (WINDOWWIDTH, WINDOWHEIGHT))
SCREEN_IMAGE = pygame.transform.scale(pygame.image.load(r'./screen.png'), (WINDOWWIDTH, WINDOWHEIGHT))
START_IMAGE = pygame.transform.scale(pygame.image.load(r'./snake.png'), (WINDOWWIDTH, WINDOWHEIGHT))

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Wormy')

    show_start_screen()
    while True:
        run_game()
        show_game_over_screen()


def run_game():
    # Set a random start point.
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    worm_coords = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction = RIGHT

    # Start the fruit in a random place.
    fruit_location = get_random_location()
    fruit_image = FRUITS_IMAGES[random.randint(0,FRUITS_IMAGES.__len__()-1)]

    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        # check if the worm has hit itself or the edge
        if worm_coords[HEAD]['x'] == -1 or worm_coords[HEAD]['x'] == CELLWIDTH or worm_coords[HEAD]['y'] == -1 or worm_coords[HEAD]['y'] == CELLHEIGHT:
            return # game over
        for worm_body in worm_coords[1:]:
            if worm_body['x'] == worm_coords[HEAD]['x'] and worm_body['y'] == worm_coords[HEAD]['y']:
                return # game over

        # check if worm has eaten an apply
        if worm_coords[HEAD]['x'] == fruit_location['x'] and worm_coords[HEAD]['y'] == fruit_location['y']:
            # don't remove worm's tail segment
            fruit_location = get_random_location() # set a new fruit somewhere
            fruit_image = FRUITS_IMAGES[random.randint(0,FRUITS_IMAGES.__len__()-1)]
        else:
            del worm_coords[-1] # remove worm's tail segment

        # move the worm by adding a segment in the direction it is moving
        if direction == UP:
            new_head = {'x': worm_coords[HEAD]['x'], 'y': worm_coords[HEAD]['y'] - 1}
        elif direction == DOWN:
            new_head = {'x': worm_coords[HEAD]['x'], 'y': worm_coords[HEAD]['y'] + 1}
        elif direction == LEFT:
            new_head = {'x': worm_coords[HEAD]['x'] - 1, 'y': worm_coords[HEAD]['y']}
        elif direction == RIGHT:
            new_head = {'x': worm_coords[HEAD]['x'] + 1, 'y': worm_coords[HEAD]['y']}
        worm_coords.insert(0, new_head)
        DISPLAYSURF.fill(BGCOLOR)
        draw_grid()
        draw_worm(worm_coords)
        draw_fruit(fruit_location, fruit_image)
        draw_score(len(worm_coords) - 3)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def draw_press_key_msg():
    press_key_surf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    press_key_rect = press_key_surf.get_rect()
    press_key_rect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(press_key_surf, press_key_rect)


def check_for_key_press():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    key_up_events = pygame.event.get(KEYUP)
    if len(key_up_events) == 0:
        return None
    if key_up_events[0].key == K_ESCAPE:
        terminate()
    return key_up_events[0].key


def show_start_screen():
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        bg_recr = pygame.Rect(0, 0, WINDOWHEIGHT, WINDOWWIDTH)
        DISPLAYSURF.blit(SCREEN_IMAGE, bg_recr)
        draw_press_key_msg()
        if check_for_key_press():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def get_random_location():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


def show_game_over_screen():
    game_over_font = pygame.font.Font('freesansbold.ttf', 120)
    game_surf = game_over_font.render('GAME', True, WHITE)
    over_surf = game_over_font.render('OVER', True, WHITE)
    game_ect = game_surf.get_rect()
    over_rect = over_surf.get_rect()
    game_ect.midtop = (WINDOWWIDTH / 2, WINDOWHEIGHT/4)
    over_rect.midtop = (WINDOWWIDTH / 2, WINDOWHEIGHT/2)

    DISPLAYSURF.blit(game_surf, game_ect)
    DISPLAYSURF.blit(over_surf, over_rect)
    draw_press_key_msg()
    pygame.display.update()
    pygame.time.wait(500)
    check_for_key_press() # clear out any key presses in the event queue

    while True:
        if check_for_key_press():
            pygame.event.get() # clear event queue
            return

def draw_score(score):
    score_surf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    score_rect = score_surf.get_rect()
    score_rect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(score_surf, score_rect)


def draw_worm(worm_coords):
    for coord in worm_coords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        worm_segment_rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, worm_segment_rect)
        worm_inner_segment_rect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, GREEN, worm_inner_segment_rect)

def draw_fruit(coord, fruit_image):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    fruit_rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    DISPLAYSURF.blit(fruit_image, fruit_rect)


def draw_grid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))
    bg_rect = pygame.Rect(0, 0, WINDOWWIDTH, WINDOWHEIGHT)
    DISPLAYSURF.blit(BACKGROUND_IMAGE, bg_rect)


if __name__ == '__main__':
    main()