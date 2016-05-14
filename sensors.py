

class Sensor:
    def __init__(self, sim, org, outgoing_connections=[]):
        from sim import Simulation
        from organism import Organism
        assert isinstance(sim, Simulation)
        assert isinstance(org, Organism)
        self.sim = sim
        self.org = org
        self.outgoing_connections = outgoing_connections

    def add_connection(self, neuron):
        from brain import Neuron
        assert isinstance(neuron, Neuron)
        self.outgoing_connections.append(neuron)

    def should_activate(self) -> bool:
        return False

    def activate(self, target=None):
        for conn in self.outgoing_connections:
            conn.activate()


class ProximitySensor(Sensor):
    def should_activate(self) -> bool:
        from organism import Organism
        for obj in self.sim.get_objs_at_pos(self.org.x, self.org.y, 1,0):
            if isinstance(obj, Organism):
                return True
        for obj in self.sim.get_objs_at_pos(self.org.x, self.org.y, 1,1):
            if isinstance(obj, Organism):
                return True
        for obj in self.sim.get_objs_at_pos(self.org.x, self.org.y, 0,1):
            if isinstance(obj, Organism):
                return True
        for obj in self.sim.get_objs_at_pos(self.org.x, self.org.y, -1,0):
            if isinstance(obj, Organism):
                return True
        for obj in self.sim.get_objs_at_pos(self.org.x, self.org.y, 1,-1):
            if isinstance(obj, Organism):
                return True
        for obj in self.sim.get_objs_at_pos(self.org.x, self.org.y, -1,1):
            if isinstance(obj, Organism):
                return True
        for obj in self.sim.get_objs_at_pos(self.org.x, self.org.y, 0,-1):
            if isinstance(obj, Organism):
                return True
        for obj in self.sim.get_objs_at_pos(self.org.x, self.org.y, -1,-1):
            if isinstance(obj, Organism):
                return True
        return False

