from resources.settings import pygame, math
from resources.cells import EmptyCell, Cell, CellType
from resources.interface import Interface
from resources.settings import CELL_SIZE, PALETTE, FONT, WORLD_HEIGHT, WORLD_WIDTH
from resources.settings import set_fps, rect_convert
from resources.settings import idle_theme


class World:
    def __init__(self, inter):
        self.width, self.height = WORLD_WIDTH, WORLD_HEIGHT
        self.space = inter.screen
        self.celling = [[Cell] * self.height for _ in range(self.width)]
        self.moving_cells = set()
        self.updates = set()
        self.base_color = EmptyCell((0, 0)).color
        self.start()

    def start(self):
        self.space.fill(self.base_color)
        for i in range(self.width):
            for j in range(self.height):
                self.celling[i][j] = EmptyCell((i, j))

    def update(self):
        copy = self.moving_cells.copy()
        self.moving_cells = set()
        for cell in copy:
            cell.behave(self)
        self.moving_cells = set(sorted(self.moving_cells, reverse=True, key=lambda comp_cell: comp_cell.pos))

    def draw(self):
        for cell in self.updates:
            if CELL_SIZE == 1:
                self.space.set_at(cell.pos, cell.color)
            else:
                pygame.draw.rect(self.space, cell.color, rect_convert(cell.pos))
        self.updates = set()

    def in_bounds(self, x, y):
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return False
        return True

    def swap(self, pos_1, pos_2):
        self.celling[pos_1[0]][pos_1[1]], self.celling[pos_2[0]][pos_2[1]] = self.celling[pos_2[0]][pos_2[1]], \
                                                                             self.celling[pos_1[0]][pos_1[1]]
        self.at(pos_1).update_pos(pos_1)
        self.at(pos_2).update_pos(pos_2)
        self.updates.add(self.at(pos_1))
        self.updates.add(self.at(pos_2))

    def append(self, new_cell):
        if self.in_bounds(new_cell.x, new_cell.y) and self.at(new_cell.pos).type == CellType.empty:
            self.celling[new_cell.x][new_cell.y] = new_cell
            self.moving_cells.add(self.celling[new_cell.x][new_cell.y])
            self.updates.add(new_cell)
            self.at(new_cell.pos).reflect(self)

    def remove(self, cell):
        if self.in_bounds(cell.x, cell.y):
            self.celling[cell.x][cell.y] = EmptyCell(cell.pos)
            self.updates.add(self.at(cell.pos))

    def at(self, position):
        if self.in_bounds(position[0], position[1]):
            return self.celling[position[0]][position[1]]
        return EmptyCell((0, 0))

    def iterate(self):
        self.update()
        self.draw()


interface = Interface()
menu_running = True
running = True
pygame.mixer.Sound.play(idle_theme)
volume = 0

while menu_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menu_running = False
            running = False
    if pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()
        if PALETTE.set_palette(pos):
            menu_running = False
    text = FONT.render("CHOOSE PALETTE", True, PALETTE.get_color("FONT_COLOR"))
    PALETTE.draw_palettes(interface.screen)
    interface.screen.blit(text, (PALETTE.pos[0], PALETTE.size[1] // 2))
    pygame.display.flip()
    if volume != 100:
        idle_theme.set_volume(math.sin(math.radians(volume ** 2)))
        volume += .0015

world = World(interface)

while running:
    world.iterate()
    running = interface.iterate(running, world)
    if interface.clear_button.is_clicked():
        world = World(interface)
    set_fps()
    pygame.display.flip()
    if volume != 100:
        idle_theme.set_volume(math.sin(math.radians(volume ** 2)))
        volume += .0015
