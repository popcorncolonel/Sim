"""
can see how many organisms are at a location
can see if you are the same representative character of any of these,
TODO: add more sensors
"""
import itertools

class Sensor:
    def __init__(self, sim, org, outgoing_connections=None):
        if outgoing_connections is None:
            outgoing_connections = set()
        from sim import Simulation
        from organism import Organism
        assert isinstance(sim, Simulation)
        assert isinstance(org, Organism)
        self.sim = sim
        self.org = org
        self.outgoing_connections = outgoing_connections

    def add_connection(self, neuron):
        self.outgoing_connections.add(neuron)

    def get_target(self) -> object:
        return None  # Can be None or an Organism (for now)

    def activate(self, target, signal) -> None:
        """
        :param target: Organism or None
        :param signal: bool - whether or not we detected something
        """
        # Activates with False if it shouldn't activate. Otherwise, "target" is an Organism. (for now)
        for conn in self.outgoing_connections:
            conn.activate(target, signal, parent=self)


class ProximitySensor(Sensor):
    """
    Activates when the organism is right next to another organism
    """
    def get_target(self) -> object:
        from organism import Organism
        targets = []
        for dx, dy in itertools.product([-1,0,1], repeat=2):
            for obj in self.sim.get_objs_at_pos(self.org.x, self.org.y, dx, dy):
                if isinstance(obj, Organism) and obj != self.org:
                    targets.append(obj)
        if targets == []:
            return None
        else:
            #  TODO: should we eventually return a list of organisms next to me?
            import random
            target = random.choice(targets)
            return target


class RightSensor(Sensor):
    def get_target(self):
        targets = []
        from organism import Organism
        for i in range(1, 15):
            for obj in self.sim.get_objs_at_pos(self.org.x, self.org.y, i, 0):
                if isinstance(obj, Organism):
                    targets.append(obj)
        import random
        if targets == []:
            return None
        else:
            return random.choice(targets)


class LeftSensor(Sensor):
    def get_target(self):
        targets = []
        from organism import Organism
        for i in range(1, 15):
            for obj in self.sim.get_objs_at_pos(self.org.x, self.org.y, -i, 0):
                if isinstance(obj, Organism):
                    targets.append(obj)
        import random
        if targets == []:
            return None
        else:
            return random.choice(targets)


class UpSensor(Sensor):
    def get_target(self):
        targets = []
        from organism import Organism
        for i in range(1, 15):
            for obj in self.sim.get_objs_at_pos(self.org.x, self.org.y, 0, i):
                if isinstance(obj, Organism):
                    targets.append(obj)
        import random
        if targets == []:
            return None
        else:
            return random.choice(targets)


class DownSensor(Sensor):
    def get_target(self):
        targets = []
        from organism import Organism
        for i in range(1, 15):
            for obj in self.sim.get_objs_at_pos(self.org.x, self.org.y, 0, -i):
                if isinstance(obj, Organism):
                    targets.append(obj)
        import random
        if targets == []:
            return None
        else:
            return random.choice(targets)

class UpRightSensor(Sensor):
    def get_target(self):
        targets = []
        from organism import Organism
        for i, j in [(i,j) for i in range(1, 15) for j in range(1, 15)]:
            for obj in self.sim.get_objs_at_pos(self.org.x, self.org.y, i, j):
                if isinstance(obj, Organism):
                    targets.append(obj)
        import random
        if targets == []:
            return None
        else:
            return random.choice(targets)


class DownRightSensor(Sensor):
    def get_target(self):
        targets = []
        from organism import Organism
        for i, j in [(i,j) for i in range(1, 15) for j in range(1, 15)]:
            for obj in self.sim.get_objs_at_pos(self.org.x, self.org.y, i, -j):
                if isinstance(obj, Organism):
                    targets.append(obj)
        import random
        if targets == []:
            return None
        else:
            return random.choice(targets)


class DownLeftSensor(Sensor):
    def get_target(self):
        targets = []
        from organism import Organism
        for i, j in [(i,j) for i in range(1, 15) for j in range(1, 15)]:
            for obj in self.sim.get_objs_at_pos(self.org.x, self.org.y, -i, -j):
                if isinstance(obj, Organism):
                    targets.append(obj)
        import random
        if targets == []:
            return None
        else:
            return random.choice(targets)


class UpLeftSensor(Sensor):
    def get_target(self):
        targets = []
        from organism import Organism
        for i, j in [(i,j) for i in range(1, 15) for j in range(1, 15)]:
            for obj in self.sim.get_objs_at_pos(self.org.x, self.org.y, -i, j):
                if isinstance(obj, Organism):
                    targets.append(obj)
        import random
        if targets == []:
            return None
        else:
            return random.choice(targets)

