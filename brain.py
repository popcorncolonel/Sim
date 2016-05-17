import sensors
from actuators import MoveActuator, AttackActuator, MateActuator


class Neuron:
    """
    Could be a Sensor, Actuator, or just an intermediary Neuron
    Sensors connect to intermediary Neurons, intermediary neurons connect to other intermediary neurons or actuators,
    and actuators receive signals from intermediary neurons
    """
    def __init__(self, outgoing_connections=None):
        if outgoing_connections is None:
            outgoing_connections = list()
        self.outgoing_connections = outgoing_connections

    def add_connection(self, connection):
        assert isinstance(connection, Neuron)
        self.outgoing_connections.add(connection)

    def activate(self, *args):
        pass


class Sensors:
    def __init__(self, sim, org):
        super().__init__()
        from sim import Simulation
        from organism import Organism
        assert isinstance(sim, Simulation)
        assert isinstance(org, Organism)
        self.sim = sim
        self.org = org
        self.list = [
            sensors.ProximitySensor(sim, org, [])
        ]


class Actuators:
    """ TODO: make it so organisms can only use one MoveActuator at a time? (or none)
    """
    def __init__(self, sim, org):
        self.up = MoveActuator(sim, org, delta_x=0, delta_y=-1)
        self.down = MoveActuator(sim, org, delta_x=0, delta_y=1)
        self.right = MoveActuator(sim, org, delta_x=1, delta_y=0)
        self.left = MoveActuator(sim, org, delta_x=-1, delta_y=0)
        self.upright = MoveActuator(sim, org, delta_x=1, delta_y=-1)
        self.upleft = MoveActuator(sim, org, delta_x=-1, delta_y=-1)
        self.downright = MoveActuator(sim, org, delta_x=1, delta_y=1)
        self.downleft = MoveActuator(sim, org, delta_x=-1, delta_y=1)
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


class IntermediaryNeuron(Neuron):
    def __init__(self, sim, org, outgoing_connections=[], parents=[]):
        super().__init__(outgoing_connections)
        self.sim = sim
        self.org = org
        self.parents = parents
        self.parent_signals = [None for _ in parents]

    def reset(self):
        for i in range(len(self.parent_signals)):
            self.parent_signals[i] = None

    def add_parent(self, parent):
        self.parents.append(parent)
        self.parent_signals.append(None)

    def broadcast(self, target):
        for conn in self.outgoing_connections:
            conn.activate(target, self)

    def all_signals_received(self):
        parents_all_received = list(filter(lambda x: x==None, self.parent_signals)) == []
        return parents_all_received

    def should_broadcast(self) -> bool:
        """
        Invariant: there are no items in self.parent_signals that are None
        """
        return all(self.parent_signals)

    def activate(self, target=None, parent=None):
        """
        Set parent signals of the proper index to false
        """
        assert parent
        parent_index = self.parents.index(parent)
        self.parent_signals[parent_index] = target  # TODO: make target a list? What happens if 2 proximity sensors are hooked up to an AND gate and both detect different objects?
        if not self.all_signals_received():  # wait for a response from all parents before saying something
            return
        else:
            assert list(filter(lambda x:x==None, self.parent_signals)) == []
            if self.should_broadcast():
                #  TODO: broadcast only the things that evaluate to truthy?
                self.broadcast(self.parent_signals)
            else:
                self.broadcast(False)


class XOR(IntermediaryNeuron):
    def should_broadcast(self) -> bool:
        result = False
        for i in self.parent_signals:
            assert i != None
            result ^= bool(i)
        return result


class AND(IntermediaryNeuron):
    def should_broadcast(self) -> bool:
        for i in self.parent_signals:
            if not i:
                return False
        return True


class OR(IntermediaryNeuron):
    def should_broadcast(self) -> bool:
        for i in self.parent_signals:
            if i:
                return True
        return False


class MiddleNeurons:
    def __init__(self, sim, org):
        self.direct = IntermediaryNeuron(sim, org)
        self.list = [
            self.direct
        ]