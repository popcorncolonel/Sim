import sys
import uuid
import brain
import random
import string

import neurons
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
        if representing_char:
            assert len(representing_char) == 1
            assert isinstance(representing_char, str)
            self.representing_char = representing_char
        else:
            self.representing_char = random.choice("abcde")

        if power:
            self.power = power
        else:
            self.power = max(0, random.normalvariate(mu=5, sigma=2.5))
        self.power = int(self.power)
        self.sensors = brain.Sensors(sim, self).list
        self.actuators = brain.Actuators(sim, self).list

        self.genome = []  # This should be dicts representing to what depth we connect stuff.
                                # i.e. [ { "type": MoreKills,
        #                                  "parents": ["sensor": 0, "neuron": 2], # can be sensors or neurons, but NOT actuators
        #                                  "connections": ["actuator": 1, "neuron": 3"] } # can be actuators or neurons, but NOT sensors ]
        """ Neuron numbers are indices into the genome list. """


    def update(self):
        """
        Updates the status of the organism within its simulation.
        Fires off all the sensors, which in turn will (or may) fire the actuators.
        """
        for sensor in self.sensors:
            target = sensor.get_target()
            if target is not None:
                sensor.activate(target, signal=True)
            else:
                sensor.activate(None, signal=False)
        for gate in self.genome:
            gate.reset()
        #self.check_status()

    def check_status(self):
        died_of_hunger = bernoulli(self.hunger / 5000)
        if died_of_hunger:
            self.sim.remove(self)

    def __str__(self):
        return self.representing_char

    def __hash__(self):
        return hash(self.hash)

    def __eq__(self, other):
        return hash(self) == hash(other)
