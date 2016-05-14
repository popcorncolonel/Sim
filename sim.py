import random
import time

from organism import Organism
from sim_tools import bernoulli, Reprinter


class Simulation:
    def __init__(self, height=14, width=30):
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
        self.collisions = []  # Reset each timestep. Dealt with after the orgs are done updating.

    def collide(self, org1: Organism, resulting_coord: tuple):
        for org in [obj for obj in self[resulting_coord[0]][resulting_coord[1]]
                    if isinstance(obj, Organism)]:
            self.collisions.append((org1, org, resulting_coord))

    def battle(self, org1: Organism, org2: Organism) -> Organism:
        """ Returns the victor of the battle. Removes the loser from the grid. """
        pass  # TODO: make this more complex. only battle if the orgs want to battle.

    def handle_collisions(self):
        """ Handles the collision of two organisms. """
        for (org1, org2, resulting_coord) in self.collisions:
            if org1.representing_char == org2.representing_char:
                baby = self.mate(org1, org2)
                self[resulting_coord[0]][resulting_coord[1]].append(baby)
        self.collisions = []

    def add(self, organism: Organism):
        self.organisms.add(organism)

    def remove(self, organism: Organism):
        if organism in self.organisms:
            self.organisms.remove(organism)
            organism.kill()
            self[organism.x][organism.y].remove(organism)

    def timestep(self):
        for organism in self.organisms:
            organism.update()
        self.handle_collisions()
        if bernoulli(0.1):
            self.spawn_new_life()

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


def main():
    sim = Simulation()

    for c in 'ABCDE':
        sim.spawn_new_life(representing_char=c)

    sim.run()


if __name__ == '__main__':
    main()
