import re
import sys
import time
import random

from organism import Organism


def bernoulli(p) -> bool:
    """
    :param p: Probability of returning True
    """
    x = random.random()
    return x < p


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
        self.organisms = set()

    def collide(self, org1: Organism, org2: Organism, resulting_coord: tuple):
        """ Handles the collision of two organisms"""
        total_power = org1.power + org2.power

    def update(self):
        for organism in self.organisms:
            organism.update()

    def run(self):
        """ Infinitely loops. """
        while True:
            self.randomize()
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



class Reprinter:
    def __init__(self):
        self.text = ''

    def moveup(self, lines):
        for _ in range(lines):
            sys.stdout.write("\x1b[A")

    def reprint(self, text):
        # Clear previous text by overwriting non-spaces with spaces
        self.moveup(self.text.count("\n"))
        sys.stdout.write(re.sub(r"[^\s]", " ", self.text))

        # Print new text
        lines = min(self.text.count("\n"), text.count("\n"))
        self.moveup(lines)
        sys.stdout.write(text)
        self.text = text


def main():
    sim = Simulation()
    sim.run()


if __name__ == '__main__':
    main()
