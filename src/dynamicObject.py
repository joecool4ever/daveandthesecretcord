import pygame
from objectTypes import GameObjectTypes
from animationsystem import AnimationController
from enums import ObjectStates, Instruments
from animationsystem import StateMachine

class DynamicObject(pygame.sprite.Sprite):
    G = 400

    def __init__(self, x, y, name, type, width, height, game, image, *groups, health = 100, cor = False, ):
        super().__init__(*groups)

        self.image = image
        self.rect = self.image.get_rect(topleft=(x,y))
        self.mask = pygame.mask.from_surface(self.image)

        self.instrument_iter = iter(Instruments)
        self.current_instrument = next(self.instrument_iter)

        #body hitboxes
        self.mask_rect = self.mask.get_bounding_rects()[0]

        #states
        self.attacking = False
        self.dashing = False
        self.crouching = False

        self.can_jump = True
        self.can_dash = True

        # position, physics
        self.vel = pygame.Vector2(0,0)
        self.speed = 50
        self.width = width
        self.height = height
        self.dx = 0
        self.dy = 0

        #tracking things
        self.grounded_timer = .1
        self.center = pygame.math.Vector2(self.rect.center)
        self.radius = self.height//2


        # game variables
        self.name = name
        self.health = health
        self.type = type
        self.game = game
        self.assets = game.assets
        self.state = ObjectStates.IDLE
        
        if name is None:
            self.name = pygame.Surface((50,50))
            self.name.fill((255,0,0))
        else:
            self.name = name

        #animation variables
        self.draw_timer = 0
        self.backwards = False
        self.image_array = None
        self.animation_stall = 0
        self.objectState = ObjectStates.IDLE
        self.cor = cor
        self.image_index = 0

        anims_needed = [state for state in ObjectStates]
        instruments = [instrument for instrument in Instruments]

        self.animationController = AnimationController(type= "object", rev_loop = True, anims_needed=anims_needed, instruments = instruments, assets = self.game.assets, name =self.name)

        self.collisions = []


        self.colliding_text = ''

    def rects_update(self):
        self.mask_rect = self.mask.get_bounding_rects()[0]
        self.mask_rect = self.mask_rect.move(self.rect.topleft)
    
    
    def update(self, game, tilemap, dt, movement=(0,0)):
        self.colliding_text = " "
        
        self.col = {'up': False, 'down': False, 'left': False, 'right': False,} 
        
        self.dx = 0
        
        self.dx = (movement[0] * self.speed + self.vel[0]) * dt

        local_mask_rect = self.mask.get_bounding_rects()[0]  

        mask_rect_x = local_mask_rect.move(self.rect.topleft)
        mask_rect_x.x += self.dx
        
        for collide_tile in tilemap.physics_tiles(mask_rect_x):
            if mask_rect_x.colliderect(collide_tile.rect):
                self.colliding_text = "Collided!"
                if self.dx > 0:
                    mask_rect_x.right = collide_tile.rect.left
                    self.col['right'] = True
                elif self.dx < 0:
                    mask_rect_x.left = collide_tile.rect.right
                    self.col['left'] = True

        self.rect.x = mask_rect_x.x - local_mask_rect.x

        self.vel[1] = min(self.vel[1] + DynamicObject.G * dt, 200)
        self.dy = (self.vel[1] + movement[1] * self.speed) * dt

        mask_rect_y = local_mask_rect.move(self.rect.topleft)
        mask_rect_y.y += self.dy
        
        for collide_tile in tilemap.physics_tiles(mask_rect_y):
            if mask_rect_y.colliderect(collide_tile.rect):
                if self.dy < 0:
                    self.vel[1] = 0
                    self.col['up'] = True
                    mask_rect_y.top = collide_tile.rect.bottom
                if self.dy > 0:
                    mask_rect_y.bottom = collide_tile.rect.top
                    self.vel[1] = 0
                    self.col['down'] = True
                
        
        self.rect.y = mask_rect_y.y - local_mask_rect.y
        
        self.mask_rect = self.mask.get_bounding_rects()[0].move(self.rect.topleft)

        # self.vel[0] *= .85
        # self.vel[0] = 0 if abs(self.vel[0]) > .1 else self.vel[0]
                

        if self.dx < 0:
            self.backwards = True
        elif self.dx > 0:
            self.backwards = False

        
        if self.col['down']:
            self.grounded_timer = .1
        else:
            self.grounded_timer = max(0, self.grounded_timer - dt)

        self.draw_timer += 1
        
    def post_update(self, dt):
        prev_state = self.state
        
        self.state = StateMachine.stateChange(self, self.state, (self.dx,self.dy))

        reset = prev_state is not self.state
        self.image = self.animationController.animate(dt, self.state, self.current_instrument, reset)
        
        if self.backwards:
            self.image = pygame.transform.flip(self.image, True, False)

        self.mask = pygame.mask.from_surface(self.image)
        
        


            
