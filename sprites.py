import pygame
import spritesheet

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Spritesheets')

sprite_sheet_image = pygame.image.load('snake-graphics.png').convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)

BG = (50, 50, 50)
BLACK = (0, 0, 0)

#
frames = [sprite_sheet.get_image(0, 0, 64, 64, 1, BLACK),
sprite_sheet.get_image(1, 0, 64, 64, 1, BLACK),
sprite_sheet.get_image(2, 0, 64, 64, 1, BLACK),
sprite_sheet.get_image(3, 0, 64, 64, 1, BLACK),
sprite_sheet.get_image(4, 0, 64, 64, 1, BLACK),
sprite_sheet.get_image(0, 1, 64, 64, 1, BLACK),
sprite_sheet.get_image(1, 1, 64, 64, 1, BLACK),
sprite_sheet.get_image(2, 1, 64, 64, 1, BLACK),
sprite_sheet.get_image(3, 1, 64, 64, 1, BLACK),
sprite_sheet.get_image(4, 1, 64, 64, 1, BLACK),
sprite_sheet.get_image(0, 2, 64, 64, 1, BLACK),
sprite_sheet.get_image(1, 2, 64, 64, 1, BLACK),
sprite_sheet.get_image(2, 2, 64, 64, 1, BLACK),
sprite_sheet.get_image(3, 2, 64, 64, 1, BLACK),
sprite_sheet.get_image(4, 2, 64, 64, 1, BLACK),
sprite_sheet.get_image(0, 3, 64, 64, 1, BLACK),
sprite_sheet.get_image(1, 3, 64, 64, 1, BLACK),
sprite_sheet.get_image(2, 3, 64, 64, 1, BLACK),
sprite_sheet.get_image(3, 3, 64, 64, 1, BLACK),
sprite_sheet.get_image(4, 3, 64, 64, 1, BLACK),
sprite_sheet.get_image(0, 4, 64, 64, 1, BLACK),
sprite_sheet.get_image(1, 4, 64, 64, 1, BLACK),
sprite_sheet.get_image(2, 4, 64, 64, 1, BLACK),
sprite_sheet.get_image(3, 4, 64, 64, 1, BLACK),
sprite_sheet.get_image(4, 4, 64, 64, 1, BLACK),
]

run = True
while run:
    #update background
    screen.fill(BG)

    #show frame image
    x = 0
    y = 0
    frame_idx = 0

    for frame in frames:
        while y < 5:
            while x < 5:
                screen.blit(frames[frame_idx], (x * 64, y * 64))
                frame_idx += 1
                x = x+1
            y += 1
            x = 0
    

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update()

pygame.quit()