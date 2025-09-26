#simple animation class to hold state/title, frames list, frame speed and current index of the animation
class Animation():
    def __init__(self, state, frames, frame_speed, current_index = 0):
        self.state = state
        self.frames = frames
        self.frame_speed = frame_speed
        self.current_index = current_index