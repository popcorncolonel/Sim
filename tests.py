import unittest

import neurons
import organism
import sensors
import actuators
import brain
import sim

def fail_case(target):
    if target:
        raise Exception

class Tests(unittest.TestCase):
    sim = sim.Simulation()
    org = organism.Organism(sim, 0, 0, power=10, representing_char='r')

    def test_neurons(self):
        sensor = sensors.Sensor(self.sim, self.org)
        sensor2 = sensors.Sensor(self.sim, self.org)
        actuator = actuators.Actuator(self.sim, self.org)
        actuator.actuate = fail_case  # make sure it doesnt happen

        middle_xor = neurons.XOR(self.sim, self.org, outgoing_connections=[actuator], parents=[sensor, sensor2])
        sensor.activate(self.org)
        sensor2.activate(self.org)
        sensor.outgoing_connections = []
        sensor2.outgoing_connections = []

        middle_and = neurons.AND(self.sim, self.org, outgoing_connections=[actuator], parents=[sensor, sensor2])
        sensor.activate(self.org)
        sensor2.activate(False)
        sensor.outgoing_connections = []
        sensor2.outgoing_connections = []

        middle_or = neurons.OR(self.sim, self.org, outgoing_connections=[actuator], parents=[sensor, sensor2])
        sensor.activate(False)
        sensor2.activate(False)
        sensor.outgoing_connections = []
        sensor2.outgoing_connections = []

        middle_nor = neurons.NOR(self.sim, self.org, outgoing_connections=[actuator], parents=[sensor, sensor2])
        sensor.activate(self.org)
        # we should just have another function in Sensor that is like activate(False) but also passes the target.
        sensor2.activate(False)
        sensor.outgoing_connections = []
        sensor2.outgoing_connections = []

