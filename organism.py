import sys
import uuid
import brain
import random
import string

from sim_tools import bernoulli, clip, binomial


class Organism:
    """
    Has a list of attributes. up speed, down speed, right speed, up speed, diagonal speeds, can move diagonally, etc.
    Should be able to see other organisms and make decisions based on that.
    """
    hash = str(uuid.uuid4())

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
        self.hunger = 0

        if power:
            self.power = power
        else:
            self.power = max(0, random.normalvariate(mu=5, sigma=2.5))
        self.dead = False
        self.actuators = brain.Actuators(sim, self).list
        #self.sensors = brain.Sensors(sim, self).list
        from actuators import AttackActuator
        from sensors import ProximitySensor
        attack_actuator = AttackActuator(sim, self)
        self.sensors = [ProximitySensor(sim, self, [attack_actuator])]
        self.genome = binomial(n=len(self.sensors), p=0.7)

        if representing_char:
            assert len(representing_char) == 1
            assert isinstance(representing_char, str)
            self.representing_char = representing_char
        else:
            self.representing_char = random.choice(string.ascii_letters)

    def update(self):
        """
        Updates the status of the organism within its simulation.
        Fires off all the sensors, which in turn will (or may) fire the actuators.
        """
        self.hunger += 1
        for sensor in self.sensors:
            should_activate = sensor.should_activate()
            if should_activate:
                if isinstance(should_activate, bool):
                    sensor.activate()
                else:
                    target = should_activate
                    sensor.activate(target)
        #self.check_status()

    def check_status(self):
        died_of_hunger = bernoulli(self.hunger / 5000)
        if died_of_hunger:
            self.sim.remove(self)

    def kill(self):
        self.dead = True

    def __str__(self):
        return self.representing_char

    def __hash__(self):
        return hash(self.hash)

    def __eq__(self, other):
        return hash(self) == hash(other)
