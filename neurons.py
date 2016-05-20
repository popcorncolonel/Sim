import uuid
import random
import sim_tools


class Neuron:
    __id__ = "BaseNeuron"
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
        self.guid = str(uuid.uuid4())  # Each neuron has a unique guid associated with it to uniquely identify what it is.

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
        assert False

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

    def to_dict(self, sensor_list, actuator_list):
        from sensors import Sensor
        from actuators import Actuator
        d = dict()
        d['type'] = self.__id__
        d['guid'] = self.guid
        parent_list = list()
        for parent in self.parents:
            if isinstance(parent, Sensor):
                parent_list.append({"sensor": sensor_list.index(parent)})
            else:  # Then it's a Neuron
                assert isinstance(parent, Neuron)
                parent_list.append({"neuron": parent.guid})
        d['parents'] = parent_list
        conn_list = list()
        for conn in self.outgoing_connections:
            if isinstance(conn, Actuator):
                conn_list.append({"actuator": actuator_list.index(conn)})
            else:  # Then it's a Neuron
                assert isinstance(conn, Neuron)
                conn_list.append({"neuron": conn.guid})
        d['connections'] = conn_list
        return d


class Direct(Neuron):
    __id__ = "Direct"
    def should_broadcast(self) -> bool:
        return all(self.parent_signals)


class XOR(Neuron):
    __id__ = "XOR"
    def should_broadcast(self) -> bool:
        result = False
        for signal in self.parent_signals:
            assert signal is not None
            assert type(signal) == bool
            result ^= signal
        return result


class AND(Neuron):
    __id__ = "AND"
    def should_broadcast(self) -> bool:
        for signal in self.parent_signals:
            if not signal:
                return False
        return True


class OR(Neuron):
    __id__ = "OR"
    def should_broadcast(self) -> bool:
        for signal in self.parent_signals:
            if signal:
                return True
        return False


class NOR(Neuron):
    __id__ = "NOR"
    def should_broadcast(self) -> bool:
        for signal in self.parent_signals:
            if signal:
                return False
        return True


class NAND(Neuron):
    __id__ = "NAND"
    def should_broadcast(self) -> bool:
        for signal in self.parent_signals:
            if not signal:
                return False
        return True


class SameSpecies(Neuron):
    __id__ = "SameSpecies"
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
    __id__ = "GreaterPower"
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
    __id__ = "LessPower"
    def should_broadcast(self):
        for target in self.parent_targets:
            if target is None:
                continue
            if target.power < self.org.power:
                return True
        return False


class MoreKills(Neuron):
    """ Gets activated if ONE OF its targets has more kills than the organism
    """
    __id__ = "MoreKills"
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
    __id__ = "FewerKills"
    def should_broadcast(self):
        for target in self.parent_targets:
            if target is None:
                continue
            if target.kills < self.org.kills:
                return True
        return False


def GreaterPowerByN(n):
    class C(Neuron):
        __id__ = "GreaterPowerBy" + str(n)
        def should_broadcast(self):
            for target in self.parent_targets:
                if target is None:
                    continue
                if target.power > self.org.power and target.power >= self.org.power + n:
                    return True
            return False
    return C


def LessPowerByN(n):
    class C(Neuron):
        __id__ = "LessPowerBy" + str(n)
        def should_broadcast(self):
            for target in self.parent_targets:
                if target is None:
                    continue
                if target.power < self.org.power and target.power <= self.org.power + n:
                    return True
            return False
    return C


def WithinNUnits(n):
    """ Gets activated if ONE OF its targets is within n units of the organism
        (for example, for n=2, things that are 2 units away return True, but 3 return False)
        Does not work around corners or borders of the map.
    """
    class C(Neuron):
        __id__ = "Within" + str(n) + "Units"
        def should_broadcast(self):
            for target in self.parent_targets:
                if target is None:
                    continue
                if sim_tools.is_n_units_away((self.org.x, self.org.y), (target.x, target.y), n):
                    return True
            return False
    return C




