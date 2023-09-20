# game settings

# imports
import pygame
import math
import abc
import enum
import random

# Game Settings
WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 720
CLOCK = pygame.time.Clock()
CELL_SIZE = 3
WORLD_SIZE = WORLD_WIDTH, WORLD_HEIGHT = WINDOW_WIDTH // CELL_SIZE, WINDOW_HEIGHT // CELL_SIZE
FPS = 120
MAX_INS_SIZE = 10
pygame.init()
pygame.mixer.init()
idle_theme = pygame.mixer.Sound('resources/Elevator_Music.mp3')

# UI settings
FONT = pygame.font.SysFont('pixel', 20)
FONT_COLOR = pygame.Color((255, 255, 255))
UI_COL_SIZE = (WINDOW_WIDTH * .05)
UI_BORDERLINE = (WINDOW_WIDTH * .01)

# sand button
sand_icon_ref = pygame.image.load("resources/sand_icon.png")
sand_icon_ref.set_colorkey('black')
sand_icon_ref_width, sand_icon_ref_height = sand_icon_ref.get_size()
sand_icon_scale = (UI_COL_SIZE - UI_BORDERLINE) / sand_icon_ref_width
sand_icon_width, sand_icon_height = int(sand_icon_ref_width * sand_icon_scale), \
                                    int(sand_icon_ref_height * sand_icon_scale)
sand_button = {
    "icon": pygame.transform.scale(sand_icon_ref,
                                   (sand_icon_width, sand_icon_height)),
    "pos": (int(WINDOW_WIDTH - UI_COL_SIZE), int(WINDOW_HEIGHT * .2)),

    "size": (sand_icon_width, sand_icon_height)
}

# water icon
water_icon_ref = pygame.image.load("resources/water_icon.png")
water_icon_ref_width, water_icon_ref_height = water_icon_ref.get_size()
water_icon_scale = (UI_COL_SIZE - UI_BORDERLINE) / water_icon_ref_width
water_icon_size = water_icon_width, water_icon_height = int(water_icon_ref_width * water_icon_scale), \
                                                        int(water_icon_ref_height * water_icon_scale)

water_button = {
    "icon": pygame.transform.scale(water_icon_ref, water_icon_size),
    "pos": (int(WINDOW_WIDTH - UI_COL_SIZE),
            int(WINDOW_HEIGHT * .01 + sand_button["pos"][1] + sand_icon_height + FONT.size("Sand")[1])),
    "size": water_icon_size
}

# plus button
plus_icon_ref = pygame.image.load("resources/plus_icon.png")
plus_icon_width, plus_icon_height = plus_icon_ref.get_size()
plus_icon_scale = (UI_COL_SIZE / 3) / plus_icon_width
plus_icon_width, plus_icon_height = int(plus_icon_width * plus_icon_scale), int(plus_icon_height * plus_icon_scale)

plus_button = {
    "icon": pygame.transform.scale(plus_icon_ref,
                                   (plus_icon_width, plus_icon_height)),

    "pos": (WINDOW_WIDTH - 3 / 2 * UI_COL_SIZE - UI_BORDERLINE, int(WINDOW_HEIGHT * .1)),
    "size": (plus_icon_width, plus_icon_height)
}

# minus button
minus_icon_ref = pygame.image.load("resources/minus_icon.png")
minus_icon_ref_width, minus_icon_ref_height = minus_icon_ref.get_size()
minus_icon_scale = (UI_COL_SIZE / 3) / minus_icon_ref_width
minus_icon_width, minus_icon_height = int(minus_icon_ref_width * minus_icon_scale), \
                                      int(minus_icon_ref_height * minus_icon_scale)

minus_button = {
    "icon": pygame.transform.scale(minus_icon_ref,
                                   (minus_icon_width, minus_icon_height)),

    "pos": (WINDOW_WIDTH - int(minus_icon_width) - UI_BORDERLINE, int(WINDOW_HEIGHT * .1)),
    "size": (int(minus_icon_ref_width * minus_icon_scale), int(minus_icon_ref_height * minus_icon_scale))
}
# dirt button
dirt_icon_ref = pygame.image.load("resources/dirt_icon.png")
dirt_icon_ref_width, dirt_icon_ref_height = dirt_icon_ref.get_size()
dirt_icon_scale = (UI_COL_SIZE - UI_BORDERLINE) / dirt_icon_ref_width
dirt_icon_width, dirt_icon_height = int(dirt_icon_ref_width * dirt_icon_scale), \
                                    int(dirt_icon_ref_height * dirt_icon_scale)

dirt_button = {
    "icon": pygame.transform.scale(dirt_icon_ref,
                                   (dirt_icon_width, dirt_icon_height)),

    "pos": (WINDOW_WIDTH - int(dirt_icon_width) - UI_BORDERLINE,
            water_button["pos"][1] + water_button["size"][1] + FONT.size("Water")[1]),
    "size": (int(dirt_icon_ref_width * dirt_icon_scale), int(dirt_icon_ref_height * dirt_icon_scale))
}

# clear button
clear_icon_ref = pygame.image.load("resources/reset_icon.png")
clear_icon_ref_width, clear_icon_ref_height = clear_icon_ref.get_size()
clear_icon_scale = (2 * UI_COL_SIZE - UI_BORDERLINE) / clear_icon_ref_width
clear_icon_width, clear_icon_height = int(clear_icon_ref_width * clear_icon_scale), \
                                      int(clear_icon_ref_height * clear_icon_scale)
clear_button = {
    "icon": pygame.transform.scale(clear_icon_ref,
                                   (clear_icon_width, clear_icon_height)),

    "pos": (WINDOW_WIDTH - 2 * UI_COL_SIZE - UI_BORDERLINE, 0),
    "size": (clear_icon_width, clear_icon_height)
}

# Size Text
size_attr_pos = (plus_button["pos"][0] + minus_button["pos"][0]) // 2, int(plus_button["pos"][1] + plus_icon_height)


# colors
class Palette:
    def __init__(self):
        self.background_color = pygame.Color((41, 41, 42))
        self.chosen_palette = 2
        self.palettes = [
            {
                "EMPTY_COLOR": pygame.Color((23, 41, 59)),
                "SAND_COLOR": pygame.Color((205, 182, 125)),
                "FONT_COLOR": pygame.Color((255, 255, 255)),
                "WATER_COLOR": pygame.Color((108, 167, 201)),
                "DIRT_COLOR": pygame.Color((107, 64, 74))
            }, {
                "EMPTY_COLOR": pygame.Color((66, 71, 80)),
                "SAND_COLOR": pygame.Color((238, 198, 72)),
                "FONT_COLOR": pygame.Color((255, 255, 255)),
                "WATER_COLOR": pygame.Color((108, 167, 201)),
                "DIRT_COLOR": pygame.Color((107, 64, 74))
            }, {
                "EMPTY_COLOR": pygame.Color((226, 226, 226)),
                "SAND_COLOR": pygame.Color((220, 158, 52)),
                "FONT_COLOR": pygame.Color((6, 9, 4)),
                "WATER_COLOR": pygame.Color((115, 110, 174)),
                "DIRT_COLOR": pygame.Color((24, 3, 15))
            }, {
                "EMPTY_COLOR": pygame.Color((222, 192, 224)),
                "SAND_COLOR": pygame.Color((251, 194, 129)),
                "FONT_COLOR": pygame.Color((12, 14, 55)),
                "WATER_COLOR": pygame.Color((161, 184, 209)),
                "DIRT_COLOR": pygame.Color((88, 82, 71))
            }
        ]
        self.size = WINDOW_WIDTH // 3 // len(self.palettes[0]), WINDOW_HEIGHT // (2 * len(self.palettes) + 1)
        self.pos = WINDOW_WIDTH // 3, WINDOW_HEIGHT // (2 * len(self.palettes) + 1)

    # Draw palette prerender
    def draw_palettes(self, surface):
        surface.fill(self.background_color)
        palette_count = 0
        for palette in self.palettes:
            color_count = 0
            for color in palette.keys():
                pygame.draw.rect(surface, palette[color],
                                 ((self.pos[0] + color_count * self.size[0],
                                   self.pos[1] + palette_count * self.size[1]),
                                  self.size))
                color_count += 1
            palette_count += 2

    # set palette
    def set_palette(self, pos):
        if self.pos[0] <= pos[0] < self.pos[0] + len(self.palettes[0]) * self.size[0]:
            if pos[1] // self.size[1] % 2 == 1:
                self.chosen_palette = pos[1] // self.size[1] // 2
                return True
        return False

    # get color
    def get_color(self, color):
        return self.palettes[self.chosen_palette][color]


PALETTE = Palette()


# game functions
def grid_convert(pos):
    return pos[0] // CELL_SIZE, pos[1] // CELL_SIZE


def surf_convert(pos):
    return pos[0] * CELL_SIZE, pos[1] * CELL_SIZE


def rect_convert(pos):
    return (pos[0] * CELL_SIZE, pos[1] * CELL_SIZE), (CELL_SIZE, CELL_SIZE)


# Show FPS
def set_fps():
    CLOCK.tick(120)
    pygame.display.set_caption(f'FPS: {CLOCK.get_fps()}')


# random chance
def toss(chance):
    return random.randint(0, 100) <= chance * 100
