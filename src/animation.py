import pygame
import random
from enums import ObjectStates, Instruments

move_animation_rects = {
    ObjectStates.IDLE : [[pygame.Rect(34*i, 0, 35, 35) for i in range(3)],8],
    ObjectStates.RUNNING : [[pygame.Rect(34*i, 35, 35, 35) for i in range(6)], 8 ],
    ObjectStates.IDLE_BLINK : [[pygame.Rect(34*3, 0, 35, 35)], 8],
    ObjectStates.FALLING : [[pygame.Rect(34*5, 0, 35, 35)], 8],
    ObjectStates.JUMPING : [[pygame.Rect(34*4, 0, 35, 35)], 8],
    ObjectStates.CROUCH_IDLE : [[pygame.Rect(0, 4*35, 35, 35)], 8],
    ObjectStates.CROUCH_WALK : [[pygame.Rect(34*i, 4*35, 35, 35) for i in range(1,6)], 8],
    ObjectStates.DASHING : [[pygame.Rect(34*6, 1*35, 35, 35)], 8]
    # ObjectStates.ATTACKING_WALK : [pygame.Rect(34*i, 2*35, 35, 35) for i in range(7)],
    # ObjectStates.ATTACKING : [pygame.Rect(34*i, 3*35, 35, 35) for i in range(7)]
}

attack_animation_rects = {}

row = 0
for instrument in Instruments:
    attack_animation_rects[instrument] = [[pygame.Rect(34*i, row*35, 35, 35) for i in range(6)], 8]
    row += 1


class Animation():
    def __init__(self, array_of_frames, frame_speed, name = "", rev_loop = False, extra_anim = None, anims_needed = [], instruments = [], assets = None):
        self.array_of_frames = array_of_frames
        self.rev_loop = rev_loop
        if self.rev_loop:
            self.full_animation = self.array_of_frames + self.array_of_frames[-1::-1]
        else:
            self.full_animation = self.array_of_frames
        
        #animation rate variables
        self.extra_anim = extra_anim
        self.frame_speed = frame_speed
        self.frame_counter = 0

        #current frame
        self.animation_frames = {}

        # How long to Blink
        self.blink_timer = 0

        #animation loading
        self.name = name
        self.anims_needed = anims_needed
        self.instruments = instruments
        self.owned_anims = {}
        self.assets = assets

        self.load_frames(anims_needed, instruments)

        

    def load_subsurf(self, list_of_rects, name, subname=""):
        key = name + subname
        subsurfs = []
        for rect in list_of_rects:
            if key in self.assets.sprite_sheets:
                sprite_sheet = self.assets.sprite_sheets[key]
                subsurfs.append(sprite_sheet.subsurface(rect))
            else:
                print(f"{key} not in sprite_sheets")
            
        return subsurfs
    
    def load_frames(self, anims_needed, instruments = []):
        subname = ""
        for anim in anims_needed:
            if anim in move_animation_rects:
                print(f"Adding {anim} to Animations")

                rects = move_animation_rects[anim][0]
                print(rects)
                
                self.owned_anims[anim] = [self.load_subsurf(rects, self.name, subname=subname), move_animation_rects[anim][1]]
            else:
                print(f'Anim name: {anim} not in Keys')
        for instrument in instruments:
            if instrument in attack_animation_rects:
                rects = attack_animation_rects[instrument][0]
                print(f'Instrument name: {instrument} added to Animations')
                self.owned_anims[str(instrument)] = [self.load_subsurf(rects, self.name, subname="_attack"), attack_animation_rects[instrument][1]]
                self.owned_anims[str(instrument) + " walk"] = [self.load_subsurf(rects, self.name, subname="_attack_walk"), attack_animation_rects[instrument][1]]
            else:
                print(f'Instrument name: {instrument} not in Keys')
            

            

    def newAnimate(self, dt, state, instrument = None, reset = False):
        
        if state == ObjectStates.ATTACKING:
            state = str(instrument)
        elif state == ObjectStates.ATTACKING_WALK:
            state = str(instrument) + " walk"
        if state in self.owned_anims:

            current_frames = self.owned_anims[state]

            if reset:
                self.animation_frame = 0
                self.frame_counter = 0
            
            if random.random() < 0.1 and self.extra_anim:
                self.blink_timer = .15
                return self.extra_anim[0]
            
            if self.blink_timer > 0 and self.extra_anim:
                self.blink_timer -= dt
                return self.extra_anim[0]
            index = 0
            try:
                index = self.grab_index(dt, state, current_frames)
                return current_frames[0][index]
            except(IndexError):
                print(f"Erroring on {state} with index: {index}")
                return pygame.Surface((35,35))
        else:
            print(f"{state} not a animation applied to DynamicObject")
            return pygame.Surface((35,35))
    
    def grab_index(self, dt, state_or_instrument, current_frames):

        frames = current_frames[0]
        frame_speed = current_frames[1]

        if state_or_instrument not in self.animation_frames:
            self.animation_frames[state_or_instrument] = 0
        self.frame_counter += dt
        if self.frame_counter >= frame_speed / 60:
            self.extra_anim_placeholder = None
            # self.animation_frame = (self.animation_frame + 1) % len(self.full_animation)
            self.animation_frames[state_or_instrument] = (self.animation_frames[state_or_instrument] + 1) % len(frames)
            self.frame_counter -= frame_speed / 60  
        return self.animation_frames[state_or_instrument]

    def animate(self, dt): 

        if self.blink_timer > 0 and self.extra_anim:
            self.blink_timer -= dt
            return self.extra_anim[0]

        self.frame_counter += dt
        if self.frame_counter >= self.frame_speed / 60:
            self.extra_anim_placeholder = None
            self.animation_frame = (self.animation_frame + 1) % len(self.full_animation)
            self.frame_counter -= self.frame_speed / 60

            
            if random.random() < 0.1 and self.extra_anim:
                self.blink_timer = .15
                return self.extra_anim[0]
        
        return self.full_animation[self.animation_frame]
