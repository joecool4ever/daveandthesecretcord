import pygame

from rects import note_colors, notes_rects, item_rects, instrument_rects
from enums import Instruments

class Hud():
    def __init__(self, player, screen, assets, font):

        self.player = player
        self.game_surface = screen.game_surface
        self.font = font
        self.screen_width, self.screen_height = self.game_surface.get_size()
        self.items_rect = pygame.Rect(0,0, self.screen_width, self.screen_height *.15)

        self.items_rect.bottom = self.screen_height

        self.surface = pygame.Surface((self.screen_width, self.screen_height * .15), pygame.SRCALPHA)
        

        self.coin_sprite = assets.sprite_sheets['items_test'].subsurface(item_rects['coin'][0][0])
        self.note_sprites = {color : assets.sprite_sheets['items_test'].subsurface(notes_rects[color][0]) for color in note_colors}

        self.instrument_sprites = {}
        
        for key in instrument_rects:
            self.instrument_sprites[key] = assets.sprite_sheets['items_test'].subsurface(instrument_rects[key])

        


    def display(self):
        self.surface.fill((0,0,0,0))
        self.surface.blit(self.coin_sprite, (0,0))
        dave_monies = self.font.render(f'{self.player.monies}', True, (0,0,0))
        self.surface.blit(dave_monies, (10, 0))

        i = 0
        for color in note_colors[:-1]:
            i += 1
            if self.player.notes_collected[color]:
                self.surface.blit(self.note_sprites[color], (i * 29, 0))
            else:
                self.surface.blit(self.note_sprites["clear"], (i * 29, 0))

        self.game_surface.blit(self.surface, self.items_rect)
        if self.player.current_instrument in self.instrument_sprites:
            self.game_surface.blit(self.instrument_sprites[self.player.current_instrument], (0, 0))