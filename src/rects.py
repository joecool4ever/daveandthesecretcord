import pygame

from enums import ObjectStates, Instruments

move_animation_rects = {
    ObjectStates.IDLE : [[pygame.Rect(34*i, 0, 35, 35) for i in range(3)], 13],
    ObjectStates.RUNNING : [[pygame.Rect(34*i, 35, 35, 35) for i in range(6)], 7],
    ObjectStates.IDLE_BLINK : [[pygame.Rect(34*3, 0, 35, 35)], 1],
    ObjectStates.FALLING : [[pygame.Rect(34*5, 0, 35, 35)], 1],
    ObjectStates.JUMPING : [[pygame.Rect(34*4, 0, 35, 35)], 1],
    ObjectStates.CROUCH_IDLE : [[pygame.Rect(0, 4*35, 35, 35)], 8],
    ObjectStates.CROUCH_WALK : [[pygame.Rect(34*i, 4*35, 35, 35) for i in range(1,6)], 8],
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

item_rects = {
    "health" : [[pygame.Rect(10 + (i * 50), 0, 50, 60) for i in range(4)], 8],
    "coin" : [[pygame.Rect(1 + (i * 29), 494, 27, 27) for i in range(6)], 8]
}

scales = {
    "note" : 1,
    "dave" : 1,
    "coin" : 1
}



notes_rects = {}
j = 0

note_colors = ["red", "orange", "yellow", "green", "lightblue", "blue", "clear"]

for color in note_colors:
    notes_rects[color] = [pygame.Rect(1 + (29 * j), 88 + (i * 29), 27, 27) for i in range(12)]
    j += 1



instrument_rects = {
    Instruments.LYRE : pygame.Rect(550, 0, 50, 60),
    Instruments.MIC : pygame.Rect(500, 12, 25, 45),
    Instruments.DRUMS : pygame.Rect(500, 70, 50, 45),
    Instruments.BASS : pygame.Rect(500, 230, 50, 100)
}