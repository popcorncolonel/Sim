

class Neuron:
    """ Could be a Sensor, Actuator, or just an intermediary Neuron
    """
    def __init__(self, outgoing_connections=None):
        if outgoing_connections is None:
            outgoing_connections = set()
        self.outgoing_connections = outgoing_connections

    def add_connection(self, connection: NeuronConnection):
        assert isinstance(connection, NeuronConnection)
        self.outgoing_connections.add(connection)

    def activate(self):
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


class MateActuator(Neuron):
    """
    Can mate with another organism if they're one unit away from you
    """

class Sensors(Neuron):
    """
    Can sense whether there is an organism immediately surrounding you,
    can compare the power of organisms,
    can look left,right,up,upright,downleft,...,
    can see if you are the same representative character
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
        self.list = [self.up,
                     self.down,
                     self.right,
                     self.left,
                     self.upright,
                     self.upleft,
                     self.downright,
                     self.downleft]
