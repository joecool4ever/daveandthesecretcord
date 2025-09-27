import os, warnings

# Hide pygame startup messages
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
os.environ["PYGAME_SDL_NO_LOGGING"] = "1"

# Ignore Python warnings from certain modules
warnings.filterwarnings("ignore", category=UserWarning, module="pkg_resources")
warnings.filterwarnings("ignore", category=UserWarning)

import pygame

from utils import lerp
from dynamicObject import DynamicObject, ObjectStates
from dynamicObjects.dave import Instruments
from dynamicObjects import Boss, Dave
from objectTypes import GameObjectTypes
from screen import Screen
from assetload import AssetLoad
from tilesystem import Tilemap
from spriteGroup import SpriteGroup
from animationsystem import AnimationController
from background import Background

assets = None

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()

        # self.trumpet = pygame.mixer.Sound('assets\\sounds\\trumpet.wav')
        # self.trumpet = self.trumpet.play(loops=-1)
        
        # self.trumpet.pause()
        self.font = pygame.font.SysFont('Arial', 30)
        
        
        self.screen = Screen()

        self.assets = AssetLoad()
        self.background = Background(self.assets)

        #sprites
        self.dave = Dave(self, current_instrument=Instruments.MIC)

        #spriteGroups
        self.all_sprites = SpriteGroup()
        self.camera_group = SpriteGroup()
        self.tiles = SpriteGroup()
        self.character_sprites = SpriteGroup()

        self.all_sprites.add(self.dave)
        self.character_sprites.add(self.dave)
        
        #focus on Dave
        self.screen.camera.x = self.dave.rect.centerx - self.screen.virtual_width // 2
        self.screen.camera.y = self.dave.rect.centery - self.screen.virtual_height // 2
        
        # self.bree = Boss((100, 20), "bree", GameObjectTypes.ENEMY, 35, 35, self)
        self.movement = [False, False]
        self.crouch_pressed = False

        self.clock = pygame.time.Clock()

        self.running = True

        self.tilemap = Tilemap(self)

        self.frames = 0

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            if dt > 0.5:
                dt = 0
    
            self.handle_input(dt)
            self.applyPhysics(dt)
            self.renderScene(dt)
            
            pygame.display.flip()

            
    def handle_input(self,dt):
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.attack_button_pressed = True
                    self.dave.attack(self.attack_button_pressed, dt)
                    # if self.dave.current_instrument == Instruments.TRUMPET:
                    #     self.trumpet.unpause()
                if event.button == 3:
                    try:
                        self.dave.current_instrument = next(self.dave.instrument_iter)
                    except(StopIteration):
                        self.dave.instrument_iter = iter(Instruments)
                        self.dave.current_instrument = next(self.dave.instrument_iter)
                    # if not self.dave.current_instrument == Instruments.TRUMPET:
                    #     self.trumpet.pause()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.attack_button_pressed = False
                    self.dave.attack(self.attack_button_pressed, dt)
                    # if self.dave.current_instrument == Instruments.TRUMPET:
                    #     self.trumpet.pause()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_s:
                    self.crouch_pressed = True
                    self.dave.crouch(self.crouch_pressed)
                if event.key == pygame.K_a:
                    self.movement[0] = True
                if event.key == pygame.K_d:
                    self.movement[1] = True
                if event.key == pygame.K_SPACE:
                    self.dave.jump() 
                if event.key == pygame.K_LSHIFT:
                    self.dave.dash()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.movement[0] = False
                if event.key == pygame.K_d:
                    self.movement[1] = False
                if event.key == pygame.K_s:
                    self.crouch_pressed = False
                    self.dave.crouch(self.crouch_pressed)
                    
    def applyPhysics(self,dt):
        
        self.character_sprites.update(self,self.tilemap, dt, (self.movement[1] - self.movement[0], self.crouch_pressed))
        self.character_sprites.post_update(dt)
        

        # Moving the camera to player
        alpha = 1 - pow(0.9, dt * 60) 
        target = pygame.math.Vector2((self.dave.rect.x,self.dave.rect.y)) - pygame.math.Vector2(self.screen.virtual_width // 2, self.screen.virtual_height // 2)

        self.screen.camera.x = lerp(self.screen.camera.x, target.x, alpha)
        self.screen.camera.y = lerp(self.screen.camera.y, target.y, alpha)
        # self.screen.camera += (target - self.screen.camera) * alpha
        self.screen.camera.x = max(self.screen.camera.x, 0)

        self.background.updateBackgrounds()

    
    def renderScene(self, dt):
        self.screen.game_surface.fill((226, 255, 252)) 
        self.background.backRender(self.screen)
        for sprite in self.tiles.sprites():
            self.screen.blit(sprite.image, sprite.rect.topleft)
        self.screen.blit(self.dave.image, self.dave.rect)
        
        # debug text
        dave_pos_text = self.font.render(f'{self.dave.rect.x}, {self.dave.rect.y}', True, (0,0,0))
        dave_vel_text = self.font.render(f'{self.dave.vel[0]}, {self.dave.vel[1]}', True, (0,0,0))
        dave_grounded_text = self.font.render(f'{self.dave.grounded_timer}', True, (0,0,0))
        dave_grounded_bool_text = self.font.render(f'{self.dave.col['down']}', True, (0,0,0))
        dave_crouching_text = self.font.render(f'{self.dave.crouching}', True, (0,0,0))

        self.screen.set_to_screen()
        self.screen.display.blit(dave_pos_text, (100,100))
        self.screen.display.blit(dave_vel_text, (100,50))
        self.screen.display.blit(dave_grounded_text, (100,150))
        self.screen.display.blit(dave_grounded_bool_text, (100,200))
        self.screen.display.blit(dave_crouching_text, (100,250))


        

        

Game().run()
pygame.quit()