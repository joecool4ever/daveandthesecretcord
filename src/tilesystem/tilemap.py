import pygame
from .tile import Tile

PHYSIC_TYPES = {'grass', 'stone'}

class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []
        self.grid_width = 30
        self.grid_height = 16

        for i in range(-self.grid_width * 2, self.grid_width * 2):
            tile = Tile(self.game, "grass", 0, (i, self.grid_height))
            self.tilemap[str(i) + ";" + str(self.grid_height)] = tile
            self.game.all_sprites.add(tile)
            self.game.tiles.add(tile)

            tile2 = Tile(self.game, "grass", 1, (5 + i, self.grid_height - 2), special="True")
            self.tilemap[str(5 + i) + ";" + str(self.grid_height - 2)] = tile2
            self.game.all_sprites.add(tile2)
            self.game.tiles.add(tile2)

    def tiles_around(self, rect):
        tiles = []

        left = int(rect.left // self.tile_size)
        right = int((rect.right - 1) // self.tile_size)
        top = int(rect.top // self.tile_size)
        bottom = int((rect.bottom - 1) // self.tile_size)

        for x in range(left, right + 1):
            for y in range(top, bottom + 1):
                check_loc = f"{x};{y}"
                if check_loc in self.tilemap:
                    tiles.append(self.tilemap[check_loc])

        return tiles
        
    def physics_tiles(self, rect):
        tiles = []
        for tile in self.tiles_around(rect):
            if tile.type in PHYSIC_TYPES:
                tiles.append(tile)
        return tiles
