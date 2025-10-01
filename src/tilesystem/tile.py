import pygame

newTiles = {
    "left_top_corner" : [pygame.Rect(0, 0, 16, 16)],
    "middle_top" : [pygame.Rect(16, 0, 16, 16), pygame.Rect(16, 0, 16, 16)],
    "right_top_corner": [pygame.Rect(48, 0, 16, 16)],
    "left_middle" : [pygame.Rect(0, 16, 16, 16)]
}

platformTiles = {
    "left" : [pygame.Rect(64, 0, 16, 16)],
    "middle" : [pygame.Rect(80, 0, 16, 16), pygame.Rect(96, 0, 16, 16)],
    "right" : [pygame.Rect(112, 0, 16, 16)]
}



class Tile(pygame.sprite.Sprite):
    
    def __init__(self, game, tile_type, variant, grid_pos, *groups, tile_size=16, passable = False, special = False):
        super().__init__(*groups)

        self.game = game
        self.type = tile_type
        self.variant = variant
        self.grid_x, self.grid_y = grid_pos
        self.tile_size = tile_size
        self.passable = passable

        # tile_images = game.assets.load_images(self.type, folder=f"tiles\\{self.type}\\")
        # self.image = tile_images[self.variant]
        
        # gsame.assets.delete_iccfile("assets\\tiles\\Forest_Tileset.png")
        tile_images = game.assets.load_image("tiles\\Forest_Tileset.png")
        self.image = tile_images.subsurface(platformTiles[tile_type][variant])

        self.type = "grass"

        # if special:
        #     self.image = self.image.subsurface(pygame.Rect(0,0,16,8))

        self.rect = self.image.get_rect(
            topleft =(self.grid_x * self.tile_size,
                      self.grid_y * self.tile_size)
        )

        self.mask = pygame.mask.from_surface(self.image)

