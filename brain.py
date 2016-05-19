import sensors
from actuators import MoveActuator, AttackActuator, MateActuator
from neurons import Neuron


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


class MiddleNeurons:
    def __init__(self, sim, org):
        self.direct = Neuron(sim, org)
        self.list = [
            self.direct
        ]


