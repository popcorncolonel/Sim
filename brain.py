

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
        self.sim[self.organism.x][self.organism.y].add(self.organism)


class Sensors(Neuron):
    def __init__(self):
        super().__init__()

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

