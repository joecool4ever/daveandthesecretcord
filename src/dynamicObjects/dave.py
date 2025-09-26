import pygame
from dynamicObject import DynamicObject
from objectTypes import GameObjectTypes
from enums import Instruments, ObjectStates
from animationsystem import AnimationController, Animation



class Dave(DynamicObject):
    global assets
    def __init__(self, game, health = 100, current_instrument = None, unlocked_instruments = []):
        x, y = game.screen.virtual_width//2, game.screen.virtual_height//2
        self.name = "dave"
        self.type = GameObjectTypes.DAVE
        self.current_instrument = current_instrument
        self.image = pygame.image.load("assets/sprites/dave/DAVE_SPRITE.png")
        self.image = self.image.subsurface(pygame.Rect(34, 0, 35, 35))
        super().__init__(x, y, name = self.name, type = type, width = 35, height = 35, game= game, cor = False, image = self.image)


        # self.dash_animation = Animation(self.assets.load_images(self.name, state = ObjectStates.DASHING, type = "object"), 8)
        


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


    # def changeState(self, movement):
    #     state = super().changeState(movement)

    #     if self.dashing:
    #         state = ObjectStates.DASHING
    #         self.animation_stall = 20

    #     if self.attacking:

    #         if self.grounded_timer > 0:
    #             if abs(movement[0]) > 0.1:
    #                 state = ObjectStates.ATTACKING_WALK
    #             else:
    #                 state = ObjectStates.ATTACKING

    #         else:
    #             if self.vel[1] < 0:
    #                 state = ObjectStates.ATTACKING_JUMP
    #             else:
    #                 state = ObjectStates.ATTACKING_FALL
        
    #         print(state)
    #     return state
    
    def update(self, game, tilemap, dt, movement=(0,0)):
        super().update(game, tilemap, dt, movement)

        if self.dashing:
            self.dash_timer -= dt
            if self.dash_timer <= 0:
                self.dashing = False
                self.vel[0] = 0
