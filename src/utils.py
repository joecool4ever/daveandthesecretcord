import pygame

def circle_rect_collide(circle_center, circle_radius, rect):
    closest_x = max(rect.left, min(circle_center[0], rect.right))
    closest_y = max(rect.top, min(circle_center[1], rect.bottom))

    dx = circle_center[0] - closest_x
    dy = circle_center[1] - closest_y

    return (dx*dx + dy*dy) < (circle_radius * circle_radius)


def mask_to_surface(mask, color=(255, 0, 0)):
    """Convert a pygame.Mask into a Surface for debugging."""
    surf = pygame.Surface(mask.get_size(), pygame.SRCALPHA)
    for x in range(mask.get_size()[0]):
        for y in range(mask.get_size()[1]):
            if mask.get_at((x, y)):  # solid pixel
                surf.set_at((x, y), color + (120,))  # semi-transparent
    return surf
