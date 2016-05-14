import sim_tools

class Neuron:
    """
    Could be a Sensor, Actuator, or just an intermediary Neuron
    """
    def __init__(self, outgoing_connections=None):
        if outgoing_connections is None:
            outgoing_connections = set()
        self.outgoing_connections = outgoing_connections

    def add_connection(self, connection: NeuronConnection):
        assert isinstance(connection, NeuronConnection)
        self.outgoing_connections.add(connection)

    def activate(self, *args):
        pass


class Actuator(Neuron):
    """
    Performs an action when it recieves a signal.
    """
    def __init__(self, sim, organism, delta_x=0, delta_y=0):
        super().__init__()
        self.sim = sim
        self.organism = organism
        self.delta_x = delta_x
        self.delta_y = delta_y

    def activate(self) -> None:
        self.sim[self.organism.x][self.organism.y].remove(self.organism)
        self.organism.x += self.delta_x
        self.organism.y += self.delta_y
        self.organism.x = self.organism.x % self.sim.width
        self.organism.y = self.organism.y % self.sim.height
        self.sim[self.organism.x][self.organism.y].add(self.organism)


class AttackActuator(Neuron):
    """
    Can battle another organism if they're one unit away from you
    """
    def __init__(self, sim, organism):
        """

        :type sim: Simulation
        :type organism: Organism
        """
        super().__init__()
        self.sim = sim
        self.organism = organism

    def activate(self, target):
        """
        Check if theyre 1 unit away

        :type target: Organism
        """
        if False:  # if they try to attack something that's more than one unit away
            return
        prob_victory = self.organism.power / (self.organism.power + target.power)
        won_battle = sim_tools.bernoulli(prob_victory)
        if won_battle:
            self.sim.remove(target)
            self.organism.kills += 1
        else:
            self.sim.remove(self.organism)
            target.kills += 1


class MateActuator(Neuron):
    """
    Can mate with another organism if they're one unit away from you
    """
    def __init__(self, sim, organism):
        super().__init__()
        self.sim = sim
        self.organism = organism

    def activate(self, target):
        """ Returns the baby of self.organism and target, to-be-placed where they are """
        if False:  # if they try to mate with something that's more than 1 unit away
            return
        power_avg = (target.power + self.organism.power) / 2
        parent_coords = (self.organism.x, self.organism.y)
        #  TODO: combine the sensors of this organism and the target
        my_char = sim_tools.bernoulli(0.5)
        if my_char:
            char = self.organism.representing_char
        else:
            char = target.representing_char
        baby = self.sim.spawn_new_life(coords=parent_coords, representing_char=char, power=power_avg)
        return baby
    pass


class Sensors(Neuron):
    """
    Can sense whether there is an organism immediately surrounding you,
    can compare the power of organisms,
    can look left,right,up,upright,downleft,...,
    can see how many organisms are at a location
    can see if you are the same representative character of any of these,
    TODO: add more sensors
    """
    def __init__(self, sim, org):
        super().__init__()
        self.sim = sim
        self.org = org

    def activate(self):
        for conn in self.outgoing_connections:
            conn.activate()


class NeuronConnection:
    """Connects Neurons to Neurons and transmits a signal when it receives a signal """
    def __init__(self, start: Neuron, end: Neuron):
        self.start = start
        self.end = end

    def activate(self):
        self.end.activate()


class Actuators:
    def __init__(self, sim, org):
        self.up = Actuator(sim, org, delta_x=0, delta_y=-1)
        self.down = Actuator(sim, org, delta_x=0, delta_y=1)
        self.right = Actuator(sim, org, delta_x=1, delta_y=0)
        self.left = Actuator(sim, org, delta_x=-1, delta_y=0)
        self.upright = Actuator(sim, org, delta_x=1, delta_y=-1)
        self.upleft = Actuator(sim, org, delta_x=-1, delta_y=-1)
        self.downright = Actuator(sim, org, delta_x=1, delta_y=1)
        self.downleft = Actuator(sim, org, delta_x=-1, delta_y=1)
        self.attacker = AttackActuator(sim, org)
        self.mater = MateActuator(sim, org)
        self.list = [
             self.up,
             self.down,
             self.right,
             self.left,
             self.upright,
             self.upleft,
             self.downright,
             self.downleft,
             self.attacker,
             self.mater,
                     ]
