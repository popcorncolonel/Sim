import unittest
import organism
import sensors
import actuators
import brain
import sim

def fail_case(target, parent):
    if target:
        raise Exception

class Tests(unittest.TestCase):
    sim = sim.Simulation()
    org = organism.Organism(sim, 0, 0, power=10, representing_char='r')

    def test_neurons(self):
        sensor = sensors.Sensor(self.sim, self.org)
        sensor2 = sensors.Sensor(self.sim, self.org)
        actuator = actuators.Actuator(self.sim, self.org)
        actuator.activate = fail_case  # make sure it doesnt happen
        middle_xor = brain.XOR(self.sim, self.org, outgoing_connections=[actuator], parents=[sensor, sensor2])
        sensor.outgoing_connections = [middle_xor]
        sensor2.outgoing_connections = [middle_xor]
        sensor.activate(self.org)
        sensor2.activate(False)
