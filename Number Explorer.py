import pygame
import sys

pygame.init()
pygame.display.set_caption('Number Explorer')
screen = pygame.display.set_mode((500, 500),0,32)

#font
font = pygame.font.SysFont("arialblack", 20)

#font color
TEXT_COL = (255,255,255)
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#Buttons

start_img = pygame.image.load

#for game loop

run = True
while run:

    text = font.render('quit', True, (255, 255, 255))

    screen.fill((255, 221, 174))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    pygame.display.update()

pygame.quit()
