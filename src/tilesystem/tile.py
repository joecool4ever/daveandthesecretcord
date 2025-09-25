import pygame

class Tile(pygame.sprite.Sprite):
    
    def __init__(self, game, tile_type, variant, grid_pos, tile_size=16, passable = False, special = False):
        super().__init__()

        self.game = game
        self.type = tile_type
        self.variant = variant
        self.grid_x, self.grid_y = grid_pos
        self.tile_size = tile_size
        self.passable = passable

        tile_images = game.assets.load_images(self.type, folder=f"tiles\\{self.type}\\")
        self.image = tile_images[self.variant]
        if special:
            self.image = self.image.subsurface(pygame.Rect(0,0,16,8))

        self.rect = self.image.get_rect(
            topleft =(self.grid_x * self.tile_size,
                      self.grid_y * self.tile_size)
        )

        self.mask = pygame.mask.from_surface(self.image)

