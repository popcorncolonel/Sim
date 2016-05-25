import neurons
import sensors
import actuators


class Sensors:
    def __init__(self, sim, org):
        super().__init__()
        from sim import Simulation
        from organism import Organism
        assert isinstance(sim, Simulation)
        assert isinstance(org, Organism)
        self.list = [
            sensors.ProximitySensor(sim, org),
            sensors.LeftSensor(sim, org),
            sensors.RightSensor(sim, org),
            sensors.UpSensor(sim, org),
            sensors.DownSensor(sim, org),
            sensors.DownLeftSensor(sim, org),
            sensors.DownRightSensor(sim, org),
            sensors.UpLeftSensor(sim, org),
            sensors.UpRightSensor(sim, org),
        ]


class Actuators:
    """ TODO: make it so organisms can only use one MoveActuator at a time? (or none)
    """
    def __init__(self, sim, org):
        from sim import Simulation
        from organism import Organism
        assert isinstance(sim, Simulation)
        assert isinstance(org, Organism)

        self.list = [
            actuators.AttackActuator(sim, org),
            actuators.MateActuator(sim, org),
            actuators.TowardsActuator(sim, org),
            actuators.AwayActuator(sim, org),
        ]


class Neurons:
    def __init__(self, sim, org):
        from sim import Simulation
        from organism import Organism
        assert isinstance(sim, Simulation)
        assert isinstance(org, Organism)

        self.list = [
            neurons.Direct,
            neurons.AND,
            neurons.NAND,
            neurons.NOR,
            neurons.OR,
            neurons.XOR,
            neurons.SameSpecies,
            neurons.GreaterPower,
            neurons.LessPower,

            neurons.GreaterPowerByN(3),
            neurons.LessPowerByN(3),
            neurons.WithinNUnits(2),
            neurons.WithinNUnits(3),
            neurons.WithinNUnits(5),
        ]


