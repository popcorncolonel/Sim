import random
import sim_tools


class Neuron:
    def __init__(self, sim, org, outgoing_connections=None, parents=None):
        if parents is None:
            parents = []
        if outgoing_connections is None:
            outgoing_connections = set()
        from sim import Simulation
        from organism import Organism
        assert isinstance(sim, Simulation)
        assert isinstance(org, Organism)
        self.outgoing_connections = outgoing_connections
        self.sim = sim
        self.org = org
        self.parents = parents
        for parent in parents:
            parent.outgoing_connections.add(self)
        self.parent_signals = [None for _ in parents]
        self.parent_targets = [None for _ in parents]

    def add_connection(self, connection):
        self.outgoing_connections.add(connection)

    def reset(self):
        for i in range(len(self.parent_signals)):
            self.parent_signals[i] = None

    def add_parent(self, parent):
        self.parents.append(parent)
        self.parent_signals.append(None)
        self.parent_targets.append(None)

    def broadcast(self, target, signal):
        for conn in self.outgoing_connections:
            conn.activate(target, signal, self)

    def all_signals_received(self):
        parents_all_received = list(filter(lambda x: x==None, self.parent_signals)) == []
        return parents_all_received

    def should_broadcast(self) -> bool:
        """
        Invariant: there are no items in self.parent_signals that are None
        """
        return all(self.parent_signals)

    def broadcast_if_ready(self):
        if not self.all_signals_received():  # wait for a response from all parents before saying something
            return
        else:
            assert list(filter(lambda x: x is None, self.parent_signals)) == []
            """ TODO: figure out what to do about this.
            if self.should_broadcast():
                self.broadcast(self.parent_targets, True)
            else:
                self.broadcast(self.parent_targets, False)
            """
            org_list = [target for target in self.parent_targets if target is not None]
            if org_list == []:
                random_target = None
            else:
                random_target = random.choice(org_list)  # TODO: random target is probably not a good idea
            if self.should_broadcast():
                self.broadcast(random_target, True)
            else:
                self.broadcast(random_target, False)

    def activate(self, target, signal, parent):
        assert parent
        assert signal is not None
        for parent_index, other_parent in enumerate(self.parents):
            if parent == other_parent:
                assert target is not self.org
                self.parent_signals[parent_index] = signal  # Assign target and signal
                self.parent_targets[parent_index] = target  # target can be None - for example, if ProximityActuator doesn't see anyone around.
                self.broadcast_if_ready()


class XOR(Neuron):
    def should_broadcast(self) -> bool:
        result = False
        for signal in self.parent_signals:
            assert signal is not None
            assert type(signal) == bool
            result ^= signal
        return result


class AND(Neuron):
    def should_broadcast(self) -> bool:
        for signal in self.parent_signals:
            if not signal:
                return False
        return True


class OR(Neuron):
    def should_broadcast(self) -> bool:
        for signal in self.parent_signals:
            if signal:
                return True
        return False


class NOR(Neuron):
    def should_broadcast(self) -> bool:
        for signal in self.parent_signals:
            if signal:
                return False
        return True


class NAND(Neuron):
    def should_broadcast(self) -> bool:
        for signal in self.parent_signals:
            if not signal:
                return False
        return True


class SameSpecies(Neuron):
    def should_broadcast(self):
        for target in self.parent_targets:
            if target is None:
                return False
            if target.representing_char != self.org.representing_char:
                return False
        return True


class GreaterPower(Neuron):
    """ Gets activated if ONE OF its targets have a greater power than the organism
    """
    def should_broadcast(self):
        for target in self.parent_targets:
            if target is None:
                continue
            if target.power > self.org.power:
                return True
        return False


class LessPower(Neuron):
    """ Gets activated if ONE OF its targets have a less power than the organism
    """
    def should_broadcast(self):
        for target in self.parent_targets:
            if target is None:
                continue
            if target.power < self.org.power:
                return True
        return False


class GreaterPowerByN(Neuron):
    def __init__(self, sim, org, n, outgoing_connections=None, parents=None):
        self.n = n
        if outgoing_connections is None:
            outgoing_connections = set()
        if parents is None:
            parents = []
        super().__init__(sim, org, outgoing_connections, parents)

    def should_broadcast(self):
        for target in self.parent_targets:
            if target is None:
                continue
            if target.power > self.org.power and target.power >= self.org.power + self.n:
                return True
        return False


class LessPowerByN(Neuron):
    def __init__(self, sim, org, n, outgoing_connections=None, parents=None):
        self.n = n
        if outgoing_connections is None:
            outgoing_connections = set()
        if parents is None:
            parents = []
        super().__init__(sim, org, outgoing_connections, parents)

    def should_broadcast(self):
        for target in self.parent_targets:
            if target is None:
                continue
            if target.power < self.org.power and target.power <= self.org.power + self.n:
                return True
        return False


class MoreKills(Neuron):
    """ Gets activated if ONE OF its targets has more kills than the organism
    """
    def should_broadcast(self):
        for target in self.parent_targets:
            if target is None:
                continue
            if target.kills > self.org.kills:
                return True
        return False


class FewerKills(Neuron):
    """ Gets activated if ONE OF its targets has fewer kills than the organism
    """
    def should_broadcast(self):
        for target in self.parent_targets:
            if target is None:
                continue
            if target.kills < self.org.kills:
                return True
        return False


class WithinNUnits(Neuron):
    """ Gets activated if ONE OF its targets is within n units of the organism
        (for example, for n=2, things that are 2 units away return True, but 3 return False)
        Does not work around corners or borders of the map.
    """
    def __init__(self, sim, org, n, outgoing_connections=None, parents=None):
        self.n = n
        if outgoing_connections is None:
            outgoing_connections = set()
        if parents is None:
            parents = []
        super().__init__(sim, org, outgoing_connections, parents)

    def should_broadcast(self):
        for target in self.parent_targets:
            if target is None:
                continue
            if sim_tools.is_n_units_away((self.org.x, self.org.y), (target.x, target.y), self.n):
                return True
        return False




