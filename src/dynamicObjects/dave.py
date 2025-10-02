import pygame
from dynamicObject import DynamicObject
from objectTypes import GameObjectTypes
from enums import Instruments, ObjectStates
from animationsystem import AnimationController, Animation
from utils import note_colors



class Dave(DynamicObject):
    global assets
    def __init__(self, game, *groups, health = 100, current_instrument = None, unlocked_instruments = []):
        x, y = game.screen.virtual_width//2, game.screen.virtual_height//2
        self.name = "dave"
        self.type = GameObjectTypes.DAVE
        self.current_instrument = current_instrument
        self.image = pygame.Surface((35,35))
        self.mask = pygame.mask.from_surface(self.image)
        # self.image = self.image.subsurface(pygame.Rect(34, 0, 35, 35))
        super().__init__(x, y, self.name, type, 35, 35, game, self.image, cor = False, *groups)

        self.monies = 0
        self.notes_collected = {color : False for color in note_colors}

    def collect_item(self, name):
        if "note" in name:
            self.notes_collected[name[:-4:]] = True
        elif "coin" in name:
            self.monies += 1
        print("Collected", name)


    def attack(self, attacking, dt):
        self.attacking = attacking
        self.state = ObjectStates.ATTACKING

            

    def dash(self):
        if not self.dashing and self.can_dash:
            self.dashing = True
            self.dash_timer = .4
            self.vel[0] = - 200 if self.backwards else 200
            self.state = ObjectStates.DASHING
    
    def jump(self):
        if self.can_jump:
            self.grounded_timer = 0
            self.vel[1] = - 200

    def crouch(self, crouching):
        self.crouching = crouching
        self.state = ObjectStates.CROUCH_IDLE
    
    def update(self, game, tilemap, dt, movement=(0,0)):
        super().update(game, tilemap, dt, movement)

        if self.dashing:
            self.dash_timer -= dt
            if self.dash_timer <= 0:
                self.dashing = False
                self.vel[0] = 0
