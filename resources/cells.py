from resources.settings import abc, enum, random, pygame
from resources.settings import PALETTE
from resources.settings import toss


class Solid(enum.Enum):
    sand = "SAND"
    dirt = "DIRT"


class Liquid(enum.Enum):
    water = "WATER"


class CellType(enum.Enum):
    solid = Solid
    liquid = Liquid
    empty = "EMPTY"


class Cell(abc.ABC):
    color = None
    pos = x, y = None, None
    type = None
    viscosity = 1
    is_moving = True
    momento = 1.0
    inertia = random.randrange(-1, 1, 2)
    reflect_matrix = [[3, 2, 3],
                      [1, 2, 1],
                      [0, 1, 0]]  # 1 - random reflection, 2 - consistent reflection, 3 - random if cell goes down

    @abc.abstractmethod
    def __init__(self):
        pass

    def reflect(self, pax):
        for row in range(len(self.reflect_matrix)):
            for col in range(len(self.reflect_matrix[row])):
                if (self.reflect_matrix[row][col] == 1 and toss(self.momento)) or self.reflect_matrix[row][col] == 2:
                    pax.moving_cells.add(pax.at((self.x + col - 1, self.y + row - 1)))
                    pax.at((self.x + col - 1, self.y + row - 1)).inertia = self.inertia
                if self.reflect_matrix[row][col] == 3 and toss(self.momento):
                    pax.at((self.x + col - 1, self.y + row - 1)).inertia = self.inertia
                    pax.moving_cells.add(pax.at((self.x + col - 1, self.y + row - 1)))

    def move(self, direction, pax):
        # Update inertia
        if direction[0] != 0:
            self.inertia = direction[0]

        if direction[1] == 0:  # this is made for equal falling speed for all objects
            for _ in range(self.viscosity):
                if self.try_move(direction[0], direction[1], pax):
                    if not pax.in_bounds(self.x + direction[0], self.y + direction[1]):
                        pax.remove(self)
                        return
                    else:
                        self.reflect(pax)
                        pax.swap(self.pos, (self.x + direction[0], self.y + direction[1]))
                else:
                    return
        else:
            if not pax.in_bounds(self.x + direction[0], self.y + direction[1]):
                pax.remove(self)
                return

            self.reflect(pax)
            pax.swap(self.pos, (self.x + direction[0], self.y + direction[1]))

    def update_pos(self, new_pos):
        self.pos = self.x, self.y = new_pos[0], new_pos[1]

    def try_move(self, x, y, pax):
        if pax.in_bounds(self.x + x, self.y + y):
            if any(self.type == solid_type for solid_type in CellType.solid.value):
                if all(pax.at((self.x + x, self.y + y)).type != solid_type for solid_type in CellType.solid.value):
                    return True
            elif any(self.type == liquid_type for liquid_type in CellType.liquid.value):
                if pax.at((self.x + x, self.y + y)).type == CellType.empty:
                    return True
            return False
        # Check to move out of horizontal bounds
        elif pax.in_bounds(self.x, self.y + y):
            return True

    def behave(self, pax):
        # We have two types of cells - solid and liquid
        # All solids behave the same, as well as liquids
        # All cells try to go down, if not - go down-left/down-right
        # That logic describes solid cells' behavior, liquid behavior = solid behavior + try to go left/right
        # Let's start:
        # If cell is empty - do nothing
        if self.type == CellType.empty:
            return

        # Try to move down
        # x  ->   ø
        # ø  ->   x
        if self.try_move(0, 1, pax):
            self.move((0, 1), pax)
        else:
            # Then if cell can move to down-left and down-right, chooses its inertia direction to fall
            if self.try_move(1, 1, pax) and self.try_move(-1, 1, pax):
                self.move((self.inertia, 1), pax)
            else:
                # Try to move right
                #  x  ->    ø
                # ∆∆ø  ->  ∆∆x
                if self.try_move(1, 1, pax):
                    self.move((1, 1), pax)
                # Try to move left
                #  x  ->    ø
                # ø∆∆  ->  x∆∆
                elif self.try_move(-1, 1, pax):
                    self.move((-1, 1), pax)
                    # Now solid behavior is over, continue with liquid
                elif any(self.type == liquid_type for liquid_type in CellType.liquid.value):
                    # That means liquid should go horizontal
                    # Then if liquid can move to left and right, chooses its inertia direction to fall
                    if self.try_move(-1, 0, pax) and self.try_move(1, 0, pax):
                        self.move((self.inertia, 0), pax)
                    else:
                        # Try to move left
                        #  øx  ->   xø
                        if self.try_move(1, 0, pax):
                            self.move((1, 0), pax)
                        # Try to move right
                        #  xø  ->   øx
                        elif self.try_move(-1, 0, pax):
                            self.move((-1, 0), pax)


class EmptyCell(Cell):
    def __init__(self, p):
        super().__init__()
        self.color = PALETTE.get_color("EMPTY_COLOR")
        self.type = CellType.empty
        self.pos = self.x, self.y = p


class SandCell(Cell):
    def __init__(self, p):
        super().__init__()
        self.color = PALETTE.get_color("SAND_COLOR")
        self.type = CellType.solid.value.sand
        self.pos = self.x, self.y = p
        self.moved = False
        self.viscosity = 1
        self.momento = 0.8
        self.inertia = random.randrange(-1, 1, 2)


class WaterCell(Cell):
    def __init__(self, p):
        super().__init__()
        self.color = PALETTE.get_color("WATER_COLOR")
        self.type = CellType.liquid.value.water
        self.pos = self.x, self.y = p
        self.viscosity = 4
        self.inertia = 1  # random.randrange(-1, 1, 2)
        self.momento = 1.0


class DirtCell(Cell):
    def __init__(self, p):
        super(DirtCell, self).__init__()
        self.color = PALETTE.get_color("DIRT_COLOR")
        self.type = CellType.solid.value.dirt
        self.pos = self.x, self.y = p
        self.viscosity = 1
        self.momento = 0.1
        self.inertia = random.randrange(-1, 1, 2)
