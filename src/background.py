import pygame


class Background():
    def __init__(self, assets):
        
        self.pictures = assets.load_images("background", folder = f"background\\")

        # self.rect = pygame.Rect(0, -300, 806, 682)
        self.rect = pygame.Rect(0, 0, 806, 682)
        self.pos = pygame.Vector2(0,0)

        self.pos = {}
        for pic in self.pictures:
            self.pos[pic] = pygame.Vector2(0,0)

        self.offsets = [.025, .1, .1025, .9, .4, .5, .9]



    def updateBackgrounds(self):
        pass

    def backRender(self, surface):
        index = 0
        for pic in self.pos:
            surface.blit(pic, self.pos[pic], self.offsets[index])
            index += 1

    def frontRender(self,surface):
        pass
