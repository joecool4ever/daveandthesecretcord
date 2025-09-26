import pygame,os
from enums import ObjectStates, Instruments


class AssetLoad():
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    ASSET_DIR = os.path.join(PROJECT_ROOT, "assets")

    def __init__(self):
        self.sprite_sheets = {
            "dave": pygame.image.load(os.path.join(AssetLoad.ASSET_DIR, "sprites\\dave\\DAVE_SPRITE.png")).convert_alpha(),
            "dave_attack": pygame.image.load(os.path.join(AssetLoad.ASSET_DIR, "sprites\\dave\\DAVE_MUSIC.png")).convert_alpha(),
            "dave_attack_walk" : pygame.image.load(os.path.join(AssetLoad.ASSET_DIR, "sprites\\dave\\DAVE_MUSIC_WALK.png")).convert_alpha(),
            "dave_attack_jump" : pygame.image.load(os.path.join(AssetLoad.ASSET_DIR, "sprites\\dave\\DAVE_MUSIC_JUMP.png")).convert_alpha(),
            "benson": pygame.image.load(os.path.join(AssetLoad.ASSET_DIR, "sprites\\benson\\BENSON_GOOD.png")).convert_alpha(),
            "benson_cor": pygame.image.load(os.path.join(AssetLoad.ASSET_DIR, "sprites\\benson\\BENSON_BAD.png")).convert_alpha(),
            "bree": pygame.image.load(os.path.join(AssetLoad.ASSET_DIR, "sprites\\bree\\BREE_GOOD.png")).convert_alpha(),
            "bree_cor": pygame.image.load(os.path.join(AssetLoad.ASSET_DIR, "sprites\\bree\\BREE_BAD.png")).convert_alpha(),
            "roxxy": pygame.image.load(os.path.join(AssetLoad.ASSET_DIR, "sprites\\roxxy\\ROXXY_GOOD.png")).convert_alpha(),
            "roxxy_cor": pygame.image.load(os.path.join(AssetLoad.ASSET_DIR, "sprites\\roxxy\\ROXXY_BAD.png")).convert_alpha(),
            "items" : pygame.image.load(os.path.join(AssetLoad.ASSET_DIR, "sprites\\ITEMS.png")).convert_alpha()
        }
        self.tilemaps = {
            "grass": pygame.image.load(os.path.join(AssetLoad.ASSET_DIR, "grassTiles.png")).convert_alpha()
        }
        self.dave_sprite_sections = []


    def bree_flight(self, name):
        return [
            self.sprite_sheets[name].subsurface(pygame.Rect(0, 70, 35, 35)),
            self.sprite_sheets[name].subsurface(pygame.Rect(34*1 + 2, 70, 35, 35)),
            self.sprite_sheets[name].subsurface(pygame.Rect(34*2, 70, 35, 35)),
            self.sprite_sheets[name].subsurface(pygame.Rect(34*3 + 1, 70, 35, 35)),
            self.sprite_sheets[name].subsurface(pygame.Rect(34*4 , 70, 35, 35)),
            self.sprite_sheets[name].subsurface(pygame.Rect(34*5 -1, 70, 35, 35)),
            self.sprite_sheets[name].subsurface(pygame.Rect(34*6, 70, 35, 35)),
        ]


    def tile_cutter(self, sheet):
        tile_array = []
        for i in range(0,640,32):
            for j in range(0,640,32):
                tile_array.append(sheet.subsurface(pygame.Rect(i,j,32,32)))

        return tile_array
    
    def frame_cutter(self, name, state, instrument = None, isWalking = False):
        match(state):
            case ObjectStates.IDLE:
                return [self.sprite_sheets[name].subsurface(pygame.Rect(34*i, 0, 35, 35)) for i in range(3)]
            case ObjectStates.IDLE_BLINK:
                return [self.sprite_sheets[name].subsurface(pygame.Rect(34*3, 0, 35, 35))]
            case ObjectStates.RUNNING:
                if name == "bree_cor":
                    return [self.sprite_sheets[name].subsurface(pygame.Rect(34*i, 70, 35, 35)) for i in range(7)]
                return [self.sprite_sheets[name].subsurface(pygame.Rect(34*i, 35, 35, 35)) for i in range(6)]
            case ObjectStates.FALLING:
                if "bree" in name:
                    return self.bree_flight(name)
                return [self.sprite_sheets[name].subsurface(pygame.Rect(34*5, 0, 35, 35))]
            case ObjectStates.JUMPING:
                if "bree" in name:
                    return self.bree_flight(name)
                return [self.sprite_sheets[name].subsurface(pygame.Rect(34*4, 0, 35, 35))]
            case ObjectStates.CROUCH_IDLE:
                return [self.sprite_sheets[name].subsurface(pygame.Rect(0, 4*35, 35, 35))]
            case ObjectStates.CROUCH_WALK:
                return [self.sprite_sheets[name].subsurface(pygame.Rect(34*i, 4*35, 35, 35)) for i in range(1,6)]
            case ObjectStates.DASHING:
                return [self.sprite_sheets[name].subsurface(pygame.Rect(34*6, 1*35, 35, 35))]
            

            case ObjectStates.ATTACKING:
                key = name + "_attack"
                if isWalking:
                    key = key + "_walk"
                match(instrument):
                    case Instruments.MIC:
                        return [self.sprite_sheets[key].subsurface(pygame.Rect(34*i, 1*35, 35, 35)) for i in range(7)]
                    case Instruments.LYRE:
                        return [self.sprite_sheets[key].subsurface(pygame.Rect(34*i, 0*35, 35, 35)) for i in range(7)]
                    case Instruments.BASS:
                        return [self.sprite_sheets[key].subsurface(pygame.Rect(34*i, 3*35, 35, 35)) for i in range(7)]
                    case Instruments.DRUMS:
                        return [self.sprite_sheets[key].subsurface(pygame.Rect(34*i, 2*35, 35, 35)) for i in range(7)]
    
    def load_image(self, path):
        img = pygame.image.load(os.path.join(AssetLoad.ASSET_DIR, path)).convert_alpha()
        return img

    def load_images(self, name, folder = None, type = None, state = None, instrument = None, isWalking = False):
        if type == "object":
            return self.frame_cutter(name, state, instrument, isWalking)
        else:
            folder_path = os.path.join(AssetLoad.ASSET_DIR,folder)
            images = []
            for img_name in sorted(os.listdir(folder_path)):
                images.append(self.load_image(os.path.join(folder, img_name)))
            return images
    
    

