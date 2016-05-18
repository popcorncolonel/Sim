import random

class Neuron:
    def __init__(self, sim, org, outgoing_connections=None, parents=None):
        if parents is None:
            parents = []
        if outgoing_connections is None:
            outgoing_connections = set()
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

