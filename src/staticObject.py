import pygame
from objectTypes import GameObjectTypes

class StaticObject():
    staticObjectsInScene = {}

    def __init__(self, x, y, name, width, height, velx = 0, vely = 0, sprite = None, type = None):
        self.x = x
        self.y = y
        self.name = name
        self.width = width
        self.height = height
        self.velx = velx # incase its a running platform
        self.vely = vely
        self.sprite = sprite
        self.type = type
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.surface = pygame.Surface((self.width, self.height))

        StaticObject.staticObjectsInScene[self.name] = self