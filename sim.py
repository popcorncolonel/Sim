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
                row.append(' ')
        self.organisms = set()  # Maps coords to organisms.
        self.collisions = []  # Reset each timestep. Dealt with after the orgs are done updating.

    def collide(self, org1: Organism, org2: Organism, resulting_coord: tuple):
        self.collisions.append((org1, org2, resulting_coord))

    def handle_collisions(self):
        for (org1, org2, resulting_coord) in self.collisions:
            """ Handles the collision of two organisms"""
            total_power = org1.power + org2.power
            org1_victory = bernoulli(org1.power / total_power)
            if org1_victory:
                self[resulting_coord[0]][resulting_coord[1]] = org1
                self.remove_from_sim(org2)
                org1.kills += 1
            else:
                self[resulting_coord[0]][resulting_coord[1]] = org2
                self.remove_from_sim(org1)
                org2.kills += 1
        self.collisions = []

    def add_to_sim(self, organism):
        self.organisms.add(organism)

    def remove_from_sim(self, organism):
        self.organisms.remove(organism)
        self[organism.x][organism.y] = ' '

    def timestep(self):
        for organism in self.organisms:
            organism.update()
        self.handle_collisions()

    def run(self):
        """ Infinitely loops. """
        while True:
            self.timestep()
            self.print_to_screen()
            time.sleep(0.5)

    def randomize(self):
        """ For testing. """
        for row in self._grid:
            for j in range(self.height):
                row[j] = random.choice(['0', '1', '2'])

    def print_to_screen(self):
        self.reprinter.reprint(str(self))

    def __str__(self) -> str:
        rows = []
        for row in self._grid:
            rows.append(''.join([str(x) for x in row]))
        this_str = '\n'.join(rows)
        return '\n' + this_str

    # sim[5]
    def __getitem__(self, key: int) -> list:
        return self._grid[key]


def main():
    sim = Simulation()

    org1 = Organism(sim, 2, 3, 5, 'A')
    org2 = Organism(sim, 3, 10, 4, 'B')
    org3 = Organism(sim, 6, 13, 3, 'C')
    org4 = Organism(sim, 0, 0, 2, 'D')
    org5 = Organism(sim, 9, 1, 1, 'E')
    sim.add_to_sim(org1)
    sim.add_to_sim(org2)
    sim.add_to_sim(org3)
    sim.add_to_sim(org4)
    sim.add_to_sim(org5)

    sim.run()


if __name__ == '__main__':
    main()
