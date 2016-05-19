import random
import time

from organism import Organism
from sim_tools import bernoulli, Reprinter


class Simulation:
    def __init__(self, height, width):
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
        self.baby_list = []

    def get_objs_at_pos(self, x, y, dx, dy) -> list:
        """
        :param x,y: location of the thing
        :param dx,dy: the dx,dy such that we are looking for (x + dx, y + dy) mod (width, height)
        :return: list of objects at that location
        """
        resulting_x = (x + dx) % self.width
        resulting_y = (y + dy) % self.height
        return self[resulting_x][resulting_y]

    def add(self, organism: Organism):
        self.organisms.add(organism)

    def clean_kill_list(self):
        for organism in self.kill_list:
            if organism in self.organisms:
                self.organisms.remove(organism)
                # self[organism.x][organism.y][self[organism.x][organism.y].index(organism)] = 'X'
                self[organism.x][organism.y].remove(organism)
        self.kill_list = []

    def clean_baby_list(self):
        for organism in self.baby_list:
            if organism not in self.organisms:
                self.organisms.add(organism)
                self[organism.x][organism.y].append(organism)
        self.baby_list = []

    def remove(self, organism: Organism):
        self.kill_list.append(organism)

    def timestep(self):
        self.clean_kill_list()
        self.clean_baby_list()
        for organism in self.organisms:
            organism.update()
        if len(self.organisms) < (self.width + self.height) / 5 and bernoulli(0.1):
            self.spawn_new_life()

    def run(self):
        """ Infinitely loops. Could return a thread at some point but I don't see the need now. """
        while True:
            self.timestep()
            self.print_to_screen()
            time.sleep(0.10)

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

        if power is not None:
            power = random.normalvariate(power, 1.0)
            power = int(power)
        org = Organism(self, x, y, representing_char=representing_char, power=power)
        #self.add(org)
        self.baby_list.append(org)
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
        this_str += '\n ' + '_' * self.height
        this_str += '\n' + "Organisms: " + str(len(self.organisms))
        this_str += "  |  "
        this_str += "Max power: " + str(max(self.organisms, key=lambda x: x.power).power)
        this_str += '\n'
        return '\n' + this_str

    # sim[5]
    def __getitem__(self, key: int) -> list:
        return self._grid[key]
