import random
import string
import sys
import uuid

from sim_tools import bernoulli, clip


class Organism:
    """
    Has a list of attributes. up speed, down speed, right speed, up speed, diagonal speeds, can move diagonally, etc.
    Should be able to see other organisms and make decisions based on that.
    """
    def __init__(self, sim, x, y, power=None, representing_char=None):
        """
        :representing_char: What's going to display on the board. Has to be one char.
        """
        self.sim = sim
        self.x = x
        self.y = y
        self.sim[x][y].append(self)
        self.hash = str(uuid.uuid4())
        self.kills = 0

        if power:
            self.power = power
        else:
            self.power = random.normalvariate(mu=5, sigma=2.5)
        self.x_vel = 0
        self.y_vel = 0
        self.x_accel = 0
        self.y_accel = 0
        self.dead = False

        if representing_char:
            assert len(representing_char) == 1
            assert isinstance(representing_char, str)
            self.representing_char = representing_char
        else:
            self.representing_char = random.choice(string.ascii_letters)

    def update(self):
        """ Updates the status of the organism within its simulation.
            Also updates the simulation grid.
        """
        (old_x, old_y) = self.update_positioning()

        try:
            self.sim[old_x][old_y].remove(self)
        except:
            print(self.sim[old_x][old_y])
            sys.exit()
        if isinstance(self.sim[self.x][self.y], Organism):
            self.sim.collide(self, (self.x, self.y))
            return
        else:
            self.sim[self.x][self.y].append(self)

    def set_accel(self):
        #  Set x and y acceleration
        #  TODO: set based on proximity to other items in the grid and their relative power.
        #  TODO: learn these based on the parameters to the organism!! Have these pref's change randomly!
        if bernoulli(0.5):
            self.x_accel += 1
        else:
            self.x_accel -= 1
        if bernoulli(0.5):
            self.y_accel += 1
        else:
            self.y_accel -= 1
        self.x_accel = clip(-1, self.x_accel, 1)
        self.y_accel = clip(-1, self.y_accel, 1)

    def update_positioning(self) -> tuple:
        old_x = self.x
        old_y = self.y

        self.x += self.x_vel
        self.x = self.x % self.sim.width
        self.y += self.y_vel
        self.y = self.y % self.sim.height

        self.set_accel()

        # set x_vel and y_vel based on my acceleration
        self.x_vel += self.x_accel
        self.y_vel += self.y_accel
        self.x_vel = clip(-1, self.x_vel, 1)
        self.y_vel = clip(-1, self.y_vel, 1)

        return old_x, old_y

    def kill(self):
        self.dead = True

    def __str__(self):
        return self.representing_char

    def __hash__(self):
        return hash(self.hash)

    def __eq__(self, other):
        return hash(self) == hash(other)


