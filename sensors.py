"""
Can sense whether there is an organism immediately surrounding you,
can compare the power of organisms,
can look left,right,up,upright,downleft,...,
can see how many organisms are at a location
can see if you are the same representative character of any of these,
TODO: add more sensors
"""

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
        self.outgoing_connections.append(neuron)

    def should_activate(self) -> bool:
        return False

    def activate(self, target=None, parent=None):
        for conn in self.outgoing_connections:
            conn.activate(target, self)

class ProximitySensor(Sensor):
    """
    Activates when the organism is right next to another organism
    """
    def should_activate(self) -> object:
        """
        :return: False or a target
        """
        from organism import Organism
        for obj in self.sim.get_objs_at_pos(self.org.x, self.org.y, 1,0):
            if isinstance(obj, Organism):
                return obj
        for obj in self.sim.get_objs_at_pos(self.org.x, self.org.y, 1,1):
            if isinstance(obj, Organism):
                return obj
        for obj in self.sim.get_objs_at_pos(self.org.x, self.org.y, 0,1):
            if isinstance(obj, Organism):
                return obj
        for obj in self.sim.get_objs_at_pos(self.org.x, self.org.y, -1,0):
            if isinstance(obj, Organism):
                return obj
        for obj in self.sim.get_objs_at_pos(self.org.x, self.org.y, 1,-1):
            if isinstance(obj, Organism):
                return obj
        for obj in self.sim.get_objs_at_pos(self.org.x, self.org.y, -1,1):
            if isinstance(obj, Organism):
                return obj
        for obj in self.sim.get_objs_at_pos(self.org.x, self.org.y, 0,-1):
            if isinstance(obj, Organism):
                return obj
        for obj in self.sim.get_objs_at_pos(self.org.x, self.org.y, -1,-1):
            if isinstance(obj, Organism):
                return obj
        for obj in self.sim.get_objs_at_pos(self.org.x, self.org.y, 0,0):  #  Check if anything is in the current position
            if isinstance(obj, Organism) and obj != self.org:
                return obj
        return False

