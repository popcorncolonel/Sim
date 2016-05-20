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

    def __init__(self, sim, x, y, power=None, representing_char=None, parent1=None, parent2=None):
        """
        :representing_char: What's going to display on the board. Has to be one char.
        """
        self.sim = sim
        self.x = x
        self.y = y
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
        if not parent1 and not parent2:
            self.assign_genome()
        else:
            assert parent1 and parent2
            self.combine_genomes(parent1, parent2)

    def assign_genome(self):
        self.sensors = brain.Sensors(self.sim, self).list
        self.neuron_classes = brain.Neurons(self.sim, self).list
        self.actuators = brain.Actuators(self.sim, self).list

        self.possible_parents = list(self.sensors)
        self.possible_connections = list(self.actuators)

        self.neurons = []  # actual live instances of the neurons
        self.genome = []  # This should be dicts representing to what depth we connect stuff.
        # i.e. [ { "type": MoreKills,
        #          "guid": <guid>,
        #          "parents": ["sensor": 0, "neuron": <guid>], # can be sensors or neurons, but NOT actuators
        #          "connections": ["actuator": 1, "neuron": <guid>"] } # can be actuators or neurons, but NOT sensors ]
        """ Neuron numbers are indices into the genome list. """
        self.assign_neurons()

    def create_random_neuron(self):
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

        neuron_class = random.choice(self.neuron_classes)
        neuron = neuron_class(self.sim, self)
        assign_parents(neuron)
        assign_conns(neuron)
        return neuron

    def assign_neurons(self):
        num_neurons = random.randint(1, 7)
        for _ in range(num_neurons):
            neuron = self.create_random_neuron()
            self.add_neuron_to_genome(neuron)

    def add_neuron_to_genome(self, neuron):
        """ Appends the neuron in dict form to the genome, adds it to its relevant lists """
        self.genome.append(neuron.to_dict(self.sensors, self.actuators))
        self.neurons.append(neuron)
        self.possible_parents.append(neuron)
        self.possible_connections.insert(0, neuron)

    def combine_genomes(self, parent1, parent2):
        """ Mixes the genomes of parent1 and parent2 (exactly how is TBD) """
        self.sensors = brain.Sensors(self.sim, self).list
        self.neuron_classes = brain.Neurons(self.sim, self).list
        self.actuators = brain.Actuators(self.sim, self).list

        longest_genome = max(parent1.genome, parent2.genome, key=lambda x: len(x))
        self.copy_genome(longest_genome)
        # TODO: add randomness (randomly sometimes add neurons, or mess up existing ones)
        # TODO: combine both genomes!
        # TODO: detect duplicate connections (like we don't want a sensor hooked up to an actuator twice)

    def duplicate_all_neurons(self, genome):
        """
        Creates neurons and copies their guids from the genomes, but does not add any connections
        """
        for neuron_dict in genome:
            neuron_classes = [C for C in self.neuron_classes if C.__id__ == neuron_dict['type']]
            assert len(neuron_classes) == 1
            neuron = neuron_classes[0](self.sim, self)
            neuron.guid = neuron_dict['guid']
            self.neurons.append(neuron)

    def add_connections_to_neurons(self, genome):
        """
        Connects all the neurons' parents and connections
        """
        for neuron_dict in genome:
            neuron = [n for n in self.neurons if n.guid == neuron_dict['guid']][0]
            self.add_parent_connections(neuron, neuron_dict)
            self.add_outgoing_connections(neuron, neuron_dict)

    def add_outgoing_connections(self, neuron, neuron_dict):
        """
        Connects a neuron to its outgoing connections
        """
        for conn_dict in neuron_dict['connections']:
            for conn_type, index in conn_dict.items():
                if conn_type == 'actuator':
                    neuron.add_parent(self.actuators[index])  # Assumption: actuators are all at the same indices in all organisms
                else:
                    assert conn_type == 'neuron'
                    guid = index
                    assert type(guid) == str
                    parent_neurons = [n for n in self.neurons if n.guid == guid]
                    assert len(parent_neurons) == 1
                    parent_neuron = parent_neurons[0]
                    neuron.add_parent(parent_neuron)

    def add_parent_connections(self, neuron, neuron_dict):
        """
        Connects a neuron to its parents
        """
        for parent_dict in neuron_dict['parents']:
            for parent_type, index in parent_dict.items():
                if parent_type == 'sensor':
                    neuron.add_parent(self.sensors[index])  # Assumption: sensors are all at the same indices in all organisms
                else:
                    assert parent_type == 'neuron'
                    guid = index
                    assert type(guid) == str
                    parent_neurons = [n for n in self.neurons if n.guid == guid]
                    assert len(parent_neurons) == 1
                    parent_neuron = parent_neurons[0]
                    neuron.add_parent(parent_neuron)

    def copy_neuron(self, neuron_dict, prev_genome):
        """
        Takes a neuron dict from a different genome
        """

    def copy_genome(self, genome):
        self.genome = genome
        self.neurons = []
        self.duplicate_all_neurons(genome)
        self.add_connections_to_neurons(genome)

    def mutate(self):
        # add a random neuron to the genome, or don't
        if bernoulli(0.3):
            neuron = self.create_random_neuron()
            self.add_neuron_to_genome(neuron)

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
