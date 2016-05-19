import sys
import uuid
import time
import brain
import random
import string

from sim_tools import bernoulli, clip


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
        self.start_time = time.time()
        self.mate_timeout = self.start_time + 30
        self.assign_genome()

    def assign_genome(self):
        self.sensors = brain.Sensors(self.sim, self).list
        self.neuron_classes = brain.Neurons(self.sim, self).list
        self.actuators = brain.Actuators(self.sim, self).list

        self.possible_parents = list(self.sensors)
        self.possible_connections = list(self.actuators)

        self.neurons = []  # actual live instances of the neurons
        self.genome = []  # This should be dicts representing to what depth we connect stuff.
                                # i.e. [ { "type": MoreKills,
        #                                  "parents": ["sensor": 0, "neuron": 2], # can be sensors or neurons, but NOT actuators
        #                                  "connections": ["actuator": 1, "neuron": 3"] } # can be actuators or neurons, but NOT sensors ]
        """ Neuron numbers are indices into the genome list. """
        self.assign_neurons()

    def assign_neurons(self):
        num_neurons = random.randint(1, 7)
        num_parents = random.randint(1, 3)
        num_conns = random.randint(1, 4)

        def assign_parents(neuron):
            for _ in range(num_parents):
                parent = random.choice(self.possible_parents)
                neuron.add_parent(parent)
                parent.add_connection(neuron)

        def assign_conns(neuron):
            for _ in range(num_conns):
                conn = random.choice(self.possible_connections)
                neuron.add_connection(conn)
                conn.add_parent(neuron)

        for _ in range(num_neurons):
            neuron_class = random.choice(self.neuron_classes)
            neuron = neuron_class(self.sim, self)
            assign_parents(neuron)
            assign_conns(neuron)
            self.genome.append(neuron.to_dict(self.sensors, self.actuators))
            self.neurons.append(neuron)
            self.possible_parents.append(neuron)
            self.possible_connections.insert(0, neuron)

    def get_age(self):
        return int(time.time() - self.start_time)

    def able_to_mate(self) -> bool:
        return time.time() > self.mate_timeout

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
        for neuron in self.neurons:
            neuron.reset()
        self.check_status()

    def check_status(self):
        age_in_seconds = self.get_age()
        if age_in_seconds < 1200:
            return
        died_of_old_age = bernoulli(age_in_seconds / 500000)
        if died_of_old_age:
            self.sim.remove(self)

    def __str__(self):
        return self.representing_char

    def __hash__(self):
        return hash(self.hash)

    def __eq__(self, other):
        return hash(self) == hash(other)
