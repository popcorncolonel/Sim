import random

class Organism:
    #  Has a list of attributes. up speed, down speed, right speed, up speed, diagonal speeds, can move diagonally, etc.
    #  Should be able to see other organisms.
    def __init__(self, sim, x, y, strength=None):
        self.sim = sim
        self.x = x
        self.y = y
        if strength:
            self.power = strength
        else:
            self.power = random.normalvariate(mu=5, sigma=2.5)
        self.x_vel = 0
        self.y_vel = 0



    def update(self):
        """ Updates the status of the organism within its simulation.
            Also updates the simulation grid.
        """
        old_x = self.x
        old_y = self.y

        self.x += self.x_vel
        self.y += self.y_vel

        self.sim[old_x][old_y] = ' '
        if isinstance(self.sim[self.x][self.y], Organism):
            self.sim.collide(self, self.sim[self.x][self.y])
            return

