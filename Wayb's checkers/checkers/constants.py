import pygame

width, height = 700,700
rows,cols = 8,8
square_size = width // cols

# colors
red = (255,0,0)
white = (255,255,255)
black = (0,0,0)
grey = (128,128,128)
light_blue = (173, 216, 230)
dark_green = (0, 100, 0)
dark_blue = (0, 0, 139)
dark_purple = (72, 61, 139)
shiny_dark_red = (139, 0, 0)
crown = pygame.transform.scale(pygame.image.load("assets/crown1.png"),(45,30))