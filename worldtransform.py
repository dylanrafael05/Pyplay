import pygame

SCREEN_DIMS = pygame.Vector2(1000, 666)

def WorldToScreen(pos: pygame.Vector2) -> pygame.Vector2:
    return (SCREEN_DIMS / 2 + pygame.Vector2(pos.x, -pos.y) * (SCREEN_DIMS.x / 480))

def ScreenToWorld(pos: pygame.Vector2) -> pygame.Vector2:
    pos -= SCREEN_DIMS / 2
    return pygame.Vector2(pos.x, -pos.y) * (480 / SCREEN_DIMS.x)

def WorldToScreenFactor(pos): return pygame.Vector2(pos.x, -pos.y) * (SCREEN_DIMS.x / 480)
def ScreenToWorldFactor(pos): return pygame.Vector2(pos.x, -pos.y) / (SCREEN_DIMS.x / 480)

def WorldToScreenFactorX(x): return +x * (SCREEN_DIMS.x / 480)
def ScreenToWorldFactorX(x): return +x / (SCREEN_DIMS.x / 480)
def WorldToScreenFactorY(y): return -y * (SCREEN_DIMS.x / 480)
def ScreenToWorldFactorY(y): return -y / (SCREEN_DIMS.x / 480)

def WorldToScreenX(x): return WorldToScreen(pygame.Vector2(x, 0)).x
def WorldToScreenY(y): return WorldToScreen(pygame.Vector2(0, y)).y
def ScreenToWorldX(x): return ScreenToWorld(pygame.Vector2(x, 0)).x
def ScreenToWorldY(y): return ScreenToWorld(pygame.Vector2(0, y)).y