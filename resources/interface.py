from resources.settings import pygame, abc
from resources.settings import plus_button, minus_button, sand_button, water_button, clear_button, dirt_button
from resources.settings import grid_convert, size_attr_pos
from resources.settings import WINDOW_WIDTH, WINDOW_HEIGHT, MAX_INS_SIZE, PALETTE, FONT
from resources.cells import SandCell, WaterCell, DirtCell


class Button:
    icon = pygame.Surface
    pos = ()
    size = ()

    def __init__(self):
        pass

    def in_bounds(self, x, y):
        if self.pos[0] <= x < self.pos[0] + self.size[0]:
            if self.pos[1] <= y < self.pos[1] + self.size[1]:
                return True
        return False

    def is_clicked(self):
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] == 1 and self.in_bounds(mouse_pos_x, mouse_pos_y):
            return True
        return False

    def draw(self, screen):
        pygame.draw.rect(screen, PALETTE.get_color("EMPTY_COLOR"), (self.pos, self.size))
        screen.blit(self.icon, self.pos)


class PlusButton(Button):

    def __init__(self):
        super().__init__()
        self.icon = plus_button["icon"]
        self.pos = plus_button["pos"]
        self.size = plus_button["size"]

    @staticmethod
    def action(size):
        if size + 1 <= MAX_INS_SIZE:
            return size + 1
        return size


class MinusButton(Button):
    def __init__(self):
        super().__init__()
        self.icon = minus_button["icon"]
        self.pos = minus_button["pos"]
        self.size = minus_button["size"]

    @staticmethod
    def action(size):
        if size - 1 > 0:
            return size - 1
        return size


class SandButton(Button):
    def __init__(self):
        super().__init__()
        self.icon = sand_button["icon"]
        self.pos = sand_button["pos"]
        self.size = sand_button["size"]


class WaterButton(Button):
    def __init__(self):
        super().__init__()
        self.icon = water_button["icon"]
        self.pos = water_button["pos"]
        self.size = water_button["size"]


class DirtButton(Button):
    def __init__(self):
        super(DirtButton, self).__init__()
        self.icon = dirt_button["icon"]
        self.pos = dirt_button["pos"]
        self.size = dirt_button["size"]


class ClearButton(Button):
    def __init__(self):
        super().__init__()
        self.icon = clear_button["icon"]
        self.pos = clear_button["pos"]
        self.size = clear_button["size"]


class Instrument(abc.ABC):
    button = Button
    size = 1
    type = None
    image = None

    @abc.abstractmethod
    def __init__(self):
        pass

    def update_size(self, new_size):
        self.size = new_size

    @abc.abstractmethod
    def get_cell(self, cell_pos):
        pass

    def draw(self, screen, render_text=False):
        self.button.draw(screen)
        text = FONT.render(str(self.type), True, PALETTE.get_color("FONT_COLOR"))
        pygame.draw.rect(screen, PALETTE.get_color("EMPTY_COLOR"),
                         ((self.button.pos[0], self.button.pos[1] + self.button.size[1]), text.get_size()))
        if render_text:
            screen.blit(text, (self.button.pos[0], self.button.pos[1] + self.button.size[1]))

    def is_chosen(self):
        return self.button.is_clicked()

    def action(self, world):
        if pygame.mouse.get_pressed()[0] == 1:
            mouse_pos = pygame.mouse.get_pos()
            for i in range(self.size):
                for j in range(self.size):
                    world.append(self.get_cell((grid_convert(mouse_pos)[0] + i, grid_convert(mouse_pos)[1] + j)))


class SandInstrument(Instrument):
    def __init__(self):
        super(SandInstrument, self).__init__()
        self.type = "Sand"
        self.size = 1
        self.button = SandButton()

    def get_cell(self, cell_pos):
        return SandCell(cell_pos)


class WaterInstrument(Instrument):
    def __init__(self):
        super(WaterInstrument, self).__init__()
        self.type = "Water"
        self.size = 1
        self.button = WaterButton()

    def get_cell(self, cell_pos):
        return WaterCell(cell_pos)


class DirtInstrument(Instrument):
    def __init__(self):
        super(DirtInstrument, self).__init__()
        self.type = "Dirt"
        self.size = 1
        self.button = DirtButton()

    def get_cell(self, cell_pos):
        return DirtCell(cell_pos)


class SizeInstrument:
    def __init__(self):
        self.plus_button = PlusButton()
        self.minus_button = MinusButton()
        self.size = 1

    def draw(self, screen):
        text = FONT.render(str(self.size), True, PALETTE.get_color("FONT_COLOR"))
        max_text = FONT.render(str(MAX_INS_SIZE), True, PALETTE.get_color("FONT_COLOR"))
        text_attribute = FONT.render("SIZE", True, PALETTE.get_color("FONT_COLOR"))
        text_width = max_text.get_width()
        text_pos_x = (plus_button["pos"][0] + plus_button["size"][0] + minus_button["pos"][0] - text_width) // 2
        text_pos_y = plus_button["pos"][1]
        self.plus_button.draw(screen)
        self.minus_button.draw(screen)
        pygame.draw.rect(screen, PALETTE.get_color("EMPTY_COLOR"), (size_attr_pos, text_attribute.get_size()))
        pygame.draw.rect(screen, PALETTE.get_color("EMPTY_COLOR"), ((text_pos_x, text_pos_y), max_text.get_size()))
        screen.blit(text_attribute, size_attr_pos)
        screen.blit(text, (text_pos_x, text_pos_y))

    def action(self):
        if self.plus_button.is_clicked():
            self.size = self.plus_button.action(self.size)
            return True
        if self.minus_button.is_clicked():
            self.size = self.minus_button.action(self.size)
            return True
        return False


class Interface:

    def __init__(self):
        self.size = WINDOW_WIDTH, WINDOW_HEIGHT
        self.screen = pygame.display.set_mode(self.size, pygame.SCALED)
        self.instruments = [SandInstrument(), WaterInstrument(), DirtInstrument()]
        self.instrument_in_use = self.instruments[0]
        self.ins_size = SizeInstrument()
        self.clear_button = ClearButton()
        self.set_clicked = False

    def iterate(self, running, world):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        for ins in self.instruments:
            if ins.is_chosen():
                self.instrument_in_use = ins
                self.set_clicked = True
            else:
                ins.draw(self.screen)
        self.instrument_in_use.draw(self.screen, True)
        self.ins_size.draw(self.screen)
        self.clear_button.draw(self.screen)

        if self.ins_size.action():
            self.set_clicked = True
            pygame.time.wait(100)
        if self.clear_button.is_clicked():
            self.set_clicked = True
        if not self.set_clicked:
            self.instrument_in_use.action(world)
        self.instrument_in_use.update_size(self.ins_size.size)

        self.set_clicked = False
        return running
