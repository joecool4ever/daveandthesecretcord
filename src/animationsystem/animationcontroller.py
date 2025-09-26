import pygame
import random
from enums import ObjectStates, Instruments
from .animation import Animation

move_animation_rects = {
    ObjectStates.IDLE : [[pygame.Rect(34*i, 0, 35, 35) for i in range(3)], 13],
    ObjectStates.RUNNING : [[pygame.Rect(34*i, 35, 35, 35) for i in range(6)], 7],
    ObjectStates.IDLE_BLINK : [[pygame.Rect(34*3, 0, 35, 35)], 1],
    ObjectStates.FALLING : [[pygame.Rect(34*5, 0, 35, 35)], 1],
    ObjectStates.JUMPING : [[pygame.Rect(34*4, 0, 35, 35)], 1],
    ObjectStates.CROUCH_IDLE : [[pygame.Rect(0, 4*35, 35, 35)], 8],
    ObjectStates.CROUCH_WALK : [[pygame.Rect(34*i, 4*35, 35, 35) for i in range(5)], 8],
    ObjectStates.DASHING : [[pygame.Rect(34*6, 1*35, 35, 35)], 1]
    # ObjectStates.ATTACKING_WALK : [pygame.Rect(34*i, 2*35, 35, 35) for i in range(7)],
    # ObjectStates.ATTACKING : [pygame.Rect(34*i, 3*35, 35, 35) for i in range(7)]
}

attack_animation_rects = {}

row = 0
for instrument in Instruments:
    attack_animation_rects[instrument] = [[pygame.Rect(34*i, row*35, 35, 35) for i in range(6)], 7]
    row += 1

attack_animation_rects[Instruments.BASS][1] = 9

attack_jump_animation_rects = {
    Instruments.MIC : [[pygame.Rect(34*i, 35*2, 35, 35) for i in range(7)], 7],
    Instruments.LYRE : [[pygame.Rect(34*i, 35*0, 35, 35) for i in range(7)], 7],
    Instruments.DRUMS : [[pygame.Rect(34*i, 35*4, 35, 35) for i in range(7)], 7],
}

attack_fall_animation_rects = {
    Instruments.MIC : [[pygame.Rect(34*i, 35*3, 35, 35) for i in range(7)], 7],
    Instruments.LYRE : [[pygame.Rect(34*i, 35*1, 35, 35) for i in range(7)], 7],
    Instruments.DRUMS : [[pygame.Rect(34*i, 35*5, 35, 35) for i in range(7)], 7],
}


class AnimationController():
    def __init__(self, type, name = "", rev_loop = False, extra_anim = None, anims_needed = [], instruments = [], assets = None):
        
        #animation rate variables
        self.extra_anim = extra_anim
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
        self.new_owned_anims = {}
        self.assets = assets

        self.current_anim = None

        self.load_frames(anims_needed, instruments)
        self.newAnimations = []

        for key,anim in self.owned_anims.items():
            self.newAnimations.append(Animation(key, anim[0], anim[1]))


        

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
                
                self.owned_anims[anim] = [self.load_subsurf(rects, self.name, subname=subname), move_animation_rects[anim][1]]
                self.new_owned_anims[anim] = Animation(anim, self.load_subsurf(rects, self.name, subname=subname), move_animation_rects[anim][1])
            else:
                print(f'Anim name: {anim} not in Keys')
        for instrument in instruments:
            if instrument in attack_animation_rects:
                rects = attack_animation_rects[instrument][0]
                print(f'Instrument name: {instrument} added to Animations')
                self.owned_anims[str(instrument)] = [self.load_subsurf(rects, self.name, subname="_attack"), attack_animation_rects[instrument][1]]
                self.new_owned_anims[str(instrument)] = Animation(instrument, self.load_subsurf(rects, self.name, subname="_attack"), attack_animation_rects[instrument][1])

                self.owned_anims[str(instrument) + " walk"] = [self.load_subsurf(rects, self.name, subname="_attack_walk"), attack_animation_rects[instrument][1]]
                self.new_owned_anims[str(instrument) + " walk"] = Animation(instrument, self.load_subsurf(rects, self.name, subname="_attack_walk"), attack_animation_rects[instrument][1])

                
                if instrument in attack_jump_animation_rects:
                    rects = attack_jump_animation_rects[instrument][0]
                    self.owned_anims[str(instrument) + " jump"] = [self.load_subsurf(rects, self.name, subname="_attack_jump"), attack_jump_animation_rects[instrument][1]]
                    self.new_owned_anims[str(instrument) + " jump"] = Animation(instrument, self.load_subsurf(rects, self.name, subname="_attack_jump"), attack_jump_animation_rects[instrument][1])
                if instrument in attack_fall_animation_rects:
                    rects = attack_fall_animation_rects[instrument][0]
                    self.owned_anims[str(instrument) + " fall"] = [self.load_subsurf(rects, self.name, subname="_attack_jump"), attack_fall_animation_rects[instrument][1]]
                    self.new_owned_anims[str(instrument) + " fall"] = Animation(instrument, self.load_subsurf(rects, self.name, subname="_attack_jump"), attack_fall_animation_rects[instrument][1])
            else:
                print(f'Instrument name: {instrument} not in Keys')
            

            

    def newAnimate(self, dt, state, instrument = None, reset = False):
        
        if state == ObjectStates.ATTACKING:
            state = str(instrument)
        elif state == ObjectStates.ATTACKING_WALK:
            state = str(instrument) + " walk"
        elif state == ObjectStates.ATTACKING_JUMP:
            state = str(instrument) + " jump"
        elif state == ObjectStates.ATTACKING_FALL:
            state = str(instrument) + " fall"

        
        if state in self.owned_anims:
            self.current_anim = state
            current_frames = self.new_owned_anims[state]

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
                return current_frames.frames[index]
            except(IndexError):
                print(f"Erroring on {state} with index: {index}")
                return pygame.Surface((35,35))
        else:
            print(f"{state} not a animation applied to DynamicObject")
            return pygame.Surface((35,35))
    
    def grab_index(self, dt, state_or_instrument, current_frames):

        frames = current_frames.frames
        frame_speed = current_frames.frame_speed

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
    
    def update_frame_rate(self, adjust):
        self.owned_anims[self.current_anim][1] += adjust
        print(f'{self.current_anim} set to {self.owned_anims[self.current_anim][1]}')
