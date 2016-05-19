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


class MiddleNeurons:
    def __init__(self, sim, org):
        from sim import Simulation
        from organism import Organism
        assert isinstance(sim, Simulation)
        assert isinstance(org, Organism)

        self.list = [
            neurons.Direct(sim, org),
            neurons.AND(sim, org),
            neurons.NAND(sim, org),
            neurons.NOR(sim, org),
            neurons.OR(sim, org),
            neurons.XOR(sim, org),
            neurons.SameSpecies(sim, org),
            neurons.GreaterPower(sim, org),
            neurons.LessPower(sim, org),
            neurons.MoreKills(sim, org),
            neurons.FewerKills(sim, org),

            neurons.GreaterPowerByN(sim, org, 2),
            neurons.LessPowerByN(sim, org, 2),
            neurons.WithinNUnits(sim, org, 2),
            neurons.GreaterPowerByN(sim, org, 3),
            neurons.LessPowerByN(sim, org, 3),
            neurons.WithinNUnits(sim, org, 3),
            neurons.GreaterPowerByN(sim, org, 4),
            neurons.LessPowerByN(sim, org, 4),
            neurons.WithinNUnits(sim, org, 4),
            neurons.GreaterPowerByN(sim, org, 5),
            neurons.LessPowerByN(sim, org, 5),
            neurons.WithinNUnits(sim, org, 5),
        ]


