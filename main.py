import pygame


if __name__ == '__main__':
    running = True
    pygame.init()
    pygame.display.set_caption('City Builder')
    size = width, height = 600, 500
    screen = pygame.display.set_mode(size)
    pygame.display.flip()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()