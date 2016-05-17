import random
import time
from copy import deepcopy

from organism import Organism
from sim_tools import bernoulli, Reprinter


class Simulation:
    def __init__(self, height=35, width=109):
        self.reprinter = Reprinter()
        self.width = height  # Internally not the same but who cares. just think about it as if x += 1 means "go right"
        self.height = width
        self._grid = []
        for i in range(height):
            self._grid.append([])
        for row in self._grid:
            for j in range(width):
                row.append([' '])
        self.organisms = set()  # Maps coords to organisms.
        self.kill_list = []

    def get_objs_at_pos(self, x, y, dx, dy) -> list:
        """

        :param x,y: location of the thing
        :param dx,dy: the dx,dy such that we are looking for (x + dx, y + dy) mod (width, height)
        :return: list of objects at that location
        """
        resulting_x = (x + dx) % self.width
        resulting_y = (y + dy) % self.height
        return self[resulting_x][resulting_y]

    def battle(self, org1: Organism, org2: Organism) -> Organism:
        """ Returns the victor of the battle. Removes the loser from the grid. """
        pass  # TODO: make this more complex. only battle if the orgs want to battle.

    def add(self, organism: Organism):
        self.organisms.add(organism)

    def clean_kill_list(self):
        for organism in self.kill_list:
            if organism in self.organisms:
                self.organisms.remove(organism)
                organism.kill()
                # self[organism.x][organism.y][self[organism.x][organism.y].index(organism)] = 'X'
                self[organism.x][organism.y].remove(organism)
        self.kill_list = []

    def remove(self, organism: Organism):
        self.kill_list.append(organism)

    def timestep(self):
        for organism in self.organisms:
            organism.update()
        self.clean_kill_list()
        if bernoulli(0.1):
            self.spawn_new_life()

    def is_one_unit_away(self, pos1: tuple, pos2: tuple) -> bool:
        """
         Doesn't handle edge cases (pos1 = on left border, pos2 = on right border)
        """
        return abs(pos1[0] - pos2[0]) <= 1 and abs(pos1[0] - pos2[0]) <= 1

    def run(self):
        """ Infinitely loops. Could return a thread at some point but I don't see the need now. """
        while True:
            self.timestep()
            self.print_to_screen()
            time.sleep(0.15)

    def spawn_new_life(self, coords=None, representing_char=None, power=None):
        """ Creates a new organism and adds it to the simulation. """
        if not coords:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            while isinstance(self[x][y], Organism):
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
        else:
            assert len(coords) == 2
            x, y = coords

        org = Organism(self, x, y, representing_char=representing_char, power=power)
        self.add(org)
        return org

    def print_to_screen(self):
        self.reprinter.reprint(str(self))

    def __str__(self) -> str:
        rows = [' ' + '_' * self.height]
        for row in self._grid:
            rowstr = '|'
            rowstr += ''.join([str(x[-1]) for x in row])
            rowstr += '|'
            rows.append(rowstr)
        this_str = '\n'.join(rows)
        return '\n' + this_str + '\n ' + '_' * self.height

    # sim[5]
    def __getitem__(self, key: int) -> list:
        return self._grid[key]
