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

        middle_xor = neurons.XOR(self.sim, self.org, outgoing_connections={actuator}, parents=[sensor, sensor2])
        sensor.activate(self.org, True)
        sensor2.activate(self.org, True)
        sensor.outgoing_connections = set()
        sensor2.outgoing_connections = set()

        middle_and = neurons.AND(self.sim, self.org, outgoing_connections={actuator}, parents=[sensor, sensor2])
        sensor.activate(self.org, True)
        sensor2.activate(self.org, False)
        sensor.outgoing_connections = set()
        sensor2.outgoing_connections = set()

        middle_or = neurons.OR(self.sim, self.org, outgoing_connections={actuator}, parents=[sensor, sensor2])
        sensor.activate(self.org, False)
        sensor2.activate(self.org, False)
        sensor.outgoing_connections = set()
        sensor2.outgoing_connections = set()

        middle_nor = neurons.NOR(self.sim, self.org, outgoing_connections={actuator}, parents=[sensor, sensor2])
        sensor.activate(self.org, True)
        # we should just have another function in Sensor that is like activate(False) but also passes the target.
        sensor2.activate(self.org, False)
        sensor.outgoing_connections = set()
        sensor2.outgoing_connections = set()

    def test_neuron_chain(self):
        sensor = sensors.Sensor(self.sim, self.org)
        sensor2 = sensors.Sensor(self.sim, self.org)
        actuator = actuators.Actuator(self.sim, self.org)
        actuator.actuate = fail_case  # make sure it doesnt happen

        middle_xor = neurons.XOR(self.sim, self.org, parents=[sensor, sensor2])
        middle_xor2 = neurons.XOR(self.sim, self.org, parents=[middle_xor, middle_xor, middle_xor])
        middle_xor2.add_connection(actuator)

        sensor.activate(self.org, False)
        sensor2.activate(self.org, True)
        sensor.outgoing_connections = set()
        sensor2.outgoing_connections = set()

