import pygame

pygame.init()

screen = pygame.display.set_mode((640, 480))


class Circle(pygame.sprite.Sprite):
    def __init__(self, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 255, 255))
        pygame.draw.circle(self.image, (color), (25, 25), 25)
        self.rect = self.image.get_rect()
        self.rect.center = (0, 0)
        self.dx = 5
        self.dy = 5

    def update(self):
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
        if self.rect.right > screen.get_width():
            self.rect.left = 0
        if self.rect.top > screen.get_height():
            self.rect.bottom = 0


def main():
    pygame.display.set_caption("Diagonal Circle")

    background = pygame.Surface(screen.get_size())
    background.fill((255, 255, 255))
    screen.blit(background, (0, 0))

    circle1 = Circle(pygame.color.Color("yellow"))

    allSprites = pygame.sprite.Group(circle1)

    clock = pygame.time.Clock()
    keepGoing = True
    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False

        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()

pygame.quit()