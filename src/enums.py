from enum import Enum

class ObjectStates(Enum):
    IDLE = "Idle"
    RUNNING = "Running"
    JUMPING = "Jumping"
    FALLING = "Falling"
    IDLE_BLINK = "Idle Blink"
    CROUCH_IDLE = "Crouch Idle"
    CROUCH_WALK = "Crouch Walk"
    DASHING = "Dashing"
    ATTACKING = "Attacking"
    ATTACKING_WALK = "Attacking Walk"

class Instruments(Enum):
    LYRE = "Lyre"
    MIC = "Mic"
    BASS = "Bass"
    DRUMS = "Drums"
    VIOLIN = "Violin"
    TRUMPET = "Trumpet"