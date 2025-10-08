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

        mask_rect = self.mask.get_bounding_rects()[0]  # relative to mask
        # distance from left edge of rect to leftmost opaque pixel
        self.mask_offset_left = mask_rect.left
        # distance from right edge of rect to rightmost opaque pixel
        self.mask_offset_right = self.rect.width - mask_rect.right
        # distance from top of rect to top opaque pixel
        self.mask_offset_top = mask_rect.top
        # distance from bottom of rect to bottom opaque pixel
        self.mask_offset_bottom = self.rect.height - mask_rect.bottom




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
        
        

        # local_mask_rect = self.mask.get_bounding_rects()[0]

        # mask_rect_x = local_mask_rect.move(self.rect.topleft)

        # mask_rect_x.x += self.dx
        
        
        # for collide_tile in self.game.tiles.sprites():
        #     left_object_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width * .1, self.rect.height * .5)
        #     right_object_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width * .1, self.rect.height * .5)
        #     right_object_rect.right = self.rect.right
        #     left_tile_rect = pygame.Rect(collide_tile.rect.x, collide_tile.rect.y, collide_tile.rect.width * .1, collide_tile.rect.height)
        #     right_tile_rect = pygame.Rect(collide_tile.rect.x, collide_tile.rect.y, collide_tile.rect.width * .1, collide_tile.rect.height)
        #     right_tile_rect.right = collide_tile.rect.right

        #     if pygame.Rect.colliderect(left_object_rect, right_tile_rect):
        #         print("Hitting on the left")
        #     if pygame.Rect.colliderect(right_object_rect, left_tile_rect):
        #         print("Hitting on the right")

        #     if pygame.sprite.collide_rect(self, collide_tile):
        #         hit = pygame.sprite.collide_mask(self, collide_tile)
        #         if (hit):
        #             if self.vel[0] > 0:
        #                 self.col['right'] = True
        #                 mask_rect_x.right = collide_tile.rect.left + 1
        #             if self.vel[0] < 0:
        #                 self.col['left'] = True
        #                 mask_rect_x.left = collide_tile.rect.right + 1
        #             self.vel[0] = 0

        # self.rect.x = mask_rect_x.x - local_mask_rect.x
        
        
        # mask_rect_y = local_mask_rect.move(self.rect.topleft)
        # mask_rect_y.y += self.dy

        # for collide_tile in self.game.tiles.sprites():
        #     top_object_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height * .1)
        #     bottom_object_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height * .1)
        #     bottom_object_rect.bottom = self.rect.bottom
        #     top_tile_rect = pygame.Rect(collide_tile.rect.x, collide_tile.rect.y, collide_tile.rect.width, collide_tile.rect.height * .1)
        #     bottom_tile_rect = pygame.Rect(collide_tile.rect.x, collide_tile.rect.y, collide_tile.rect.width, collide_tile.rect.height * .1)
        #     bottom_tile_rect.bottom = collide_tile.rect.bottom

        #     if pygame.Rect.colliderect(bottom_object_rect, top_tile_rect):
        #         hit = pygame.sprite.collide_mask(self, collide_tile)
        #         if (hit):
        #             if self.vel[1] > 0 and not self.col['down']:
        #                 self.col['down'] = True
        #                 mask_rect_y.bottom = collide_tile.rect.top + 1
        #                 self.vel[1] = 0
        #         # print("Hitting on the bottom")
        #     if pygame.Rect.colliderect(top_object_rect, bottom_tile_rect):
        #         hit = pygame.sprite.collide_mask(self, collide_tile)
        #         if (hit):
        #             self.col['up'] = True
        #             mask_rect_y.top = collide_tile.rect.bottom + 1
        #             self.vel[1] = 0

        #         print("Hitting on the top")

        
            # if pygame.sprite.collide_rect(self, collide_tile):
            #     hit = pygame.sprite.collide_mask(self, collide_tile)
            #     if (hit):
            #         if self.vel[1] > 0 and not self.col['down']:
            #             self.col['down'] = True
            #             mask_rect_y.bottom = collide_tile.rect.top + 1
            #         if self.vel[1] < 0 and not self.col['up']:
            #             self.col['up'] = True
            #             mask_rect_y.top = collide_tile.rect.bottom + 1
            #         self.vel[1] = 0

                
        # mask_rect_y.y = int(mask_rect_y.y)

        self.dx = 0
        
        self.dx = (movement[0] * self.speed + self.vel[0]) * dt
        self.rect.x += self.dx

        for collide_tile in self.game.tiles.sprites():
            hit = pygame.sprite.collide_mask(self, collide_tile)
            if hit:
                print("colliding left/right")
                if self.dx < 0:
                    if self.rect.bottom > collide_tile.rect.top and self.rect.top < collide_tile.rect.bottom:
                        if self.rect.left >= collide_tile.rect.centerx:
                            self.rect.left = collide_tile.rect.right - 7
                            self.col['left'] = True
                            self.dx = 0
                elif self.dx > 0:
                    if self.rect.bottom > collide_tile.rect.top and self.rect.top < collide_tile.rect.bottom:
                        if self.rect.right <= collide_tile.rect.centerx:
                            print("Right")
                            self.rect.right = collide_tile.rect.left + 7
                            self.col['right'] = True
                            self.dx = 0

        self.vel[1] = min(self.vel[1] + DynamicObject.G * dt, 200)
        self.dy = (self.vel[1] + movement[1] * self.speed) * dt

        
        self.rect.y += self.dy

        for collide_tile in self.game.tiles.sprites():
            hit = pygame.sprite.collide_mask(self, collide_tile)
            if hit:
                if self.dy < 0:
                    if self.rect.right > collide_tile.rect.left and self.rect.left < collide_tile.rect.right:
                        if self.rect.bottom >= collide_tile.rect.centery:
                            print("top")
                            self.rect.top = collide_tile.rect.bottom - self.mask_offset_top
                            self.col['up'] = True
                            self.vel[1] = 0
                            self.dy = 0
                elif self.dy > 0:
                    if self.rect.right > collide_tile.rect.left and self.rect.left < collide_tile.rect.right:
                        if self.rect.bottom <= collide_tile.rect.centery:
                            self.rect.bottom = collide_tile.rect.top + self.mask_offset_bottom
                            self.col['down'] = True
                            self.vel[1] = 0
                            self.dy = 0
        
                



        # if hit[0] > 18:
        #                 self.rect.x += 35 - hit[0]
        #             else:
        #                 self.rect.x -= hit[0]
                    # if self.dy < 0:
                    #     self.vel[1] = 0
                    #     self.col['up'] = True
                    #     # self.rect.top = collide_tile.rect.bottom
                    # if self.dy > 0:
                    #     # self.rect.bottom = collide_tile.rect.top
                    #     self.vel[1] = 0
                    #     self.col['down'] = True
        
        local_mask_rect = self.mask.get_bounding_rects()[0]
        
        # self.rect.y = mask_rect_y.y - local_mask_rect.y
        
        self.mask_rect = self.mask.get_bounding_rects()[0].move(self.rect.topleft)

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

        mask_rect = self.mask.get_bounding_rects()[0]  # relative to mask
        # distance from left edge of rect to leftmost opaque pixel
        self.mask_offset_left = mask_rect.left
        # distance from right edge of rect to rightmost opaque pixel
        self.mask_offset_right = self.rect.width - mask_rect.right
        # distance from top of rect to top opaque pixel
        self.mask_offset_top = mask_rect.top
        # distance from bottom of rect to bottom opaque pixel
        self.mask_offset_bottom = self.rect.height - mask_rect.bottom


        
        


            
