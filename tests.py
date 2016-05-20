import unittest

import neurons
import organism
import sensors
import actuators
import sim

def fail_case(target):
    if target:
        raise Exception

class Tests(unittest.TestCase):
    sim = sim.Simulation(30, 30)
    org = organism.Organism(sim, 0, 0, power=10, representing_char='r')
    org2 = organism.Organism(sim, 3, 3, power=3, representing_char='b')

    def reset(self):
        self.sim = sim.Simulation(30, 30)
        self.org = organism.Organism(self.sim, 0, 0, power=10, representing_char='r')
        self.org2 = organism.Organism(self.sim, 3, 3, power=3, representing_char='b')

    def test_neurons(self):
        sensor = sensors.Sensor(self.sim, self.org)
        sensor2 = sensors.Sensor(self.sim, self.org)
        actuator = actuators.Actuator(self.sim, self.org)
        actuator.actuate = fail_case  # make sure it doesnt happen

        middle_xor = neurons.XOR(self.sim, self.org, outgoing_connections={actuator}, parents=[sensor, sensor2])
        sensor.activate(self.org2, True)
        sensor2.activate(self.org2, True)
        sensor.outgoing_connections = set()
        sensor2.outgoing_connections = set()

        middle_and = neurons.AND(self.sim, self.org, outgoing_connections={actuator}, parents=[sensor, sensor2])
        sensor.activate(self.org2, True)
        sensor2.activate(self.org2, False)
        sensor.outgoing_connections = set()
        sensor2.outgoing_connections = set()

        middle_or = neurons.OR(self.sim, self.org, outgoing_connections={actuator}, parents=[sensor, sensor2])
        sensor.activate(self.org2, False)
        sensor2.activate(self.org2, False)
        sensor.outgoing_connections = set()
        sensor2.outgoing_connections = set()

        middle_nor = neurons.NOR(self.sim, self.org, outgoing_connections={actuator}, parents=[sensor, sensor2])
        sensor.activate(self.org2, True)
        # we should just have another function in Sensor that is like activate(False) but also passes the target.
        sensor2.activate(self.org2, False)
        sensor.outgoing_connections = set()
        sensor2.outgoing_connections = set()

    def test_neuron_chain(self):
        sensor = sensors.Sensor(self.sim, self.org)
        sensor2 = sensors.Sensor(self.sim, self.org)
        actuator = actuators.Actuator(self.sim, self.org)
        actuator.actuate = fail_case  # make sure it doesnt happen

        middle_xor = neurons.XOR(self.sim, self.org, parents=[sensor, sensor2])
        middle_xor2 = neurons.XOR(self.sim, self.org, parents=[middle_xor, middle_xor, middle_xor, middle_xor])
        middle_xor2.add_connection(actuator)

        sensor.activate(self.org2, False)
        sensor2.activate(self.org2, True)
        sensor.outgoing_connections = set()
        sensor2.outgoing_connections = set()

    def test_towards_xy(self):
        self.reset()
        sensor = sensors.Sensor(self.sim, self.org)
        dumbass = organism.Organism(self.sim, 8, 8, power=10, representing_char='d')
        neuron = neurons.Direct(self.sim, self.org, parents=[sensor])
        actuator = actuators.TowardsActuator(self.sim, self.org)
        neuron.add_connection(actuator)

        sensor.activate(dumbass, True)
        self.assertEqual(self.org.x, 1)
        self.assertEqual(self.org.y, 1)

    def test_away_xy(self):
        self.reset()
        sensor = sensors.Sensor(self.sim, self.org)
        dumbass = organism.Organism(self.sim, 8, 1, power=10, representing_char='d')
        neuron = neurons.Direct(self.sim, self.org, parents=[sensor])
        actuator = actuators.AwayActuator(self.sim, self.org)
        neuron.add_connection(actuator)

        sensor.activate(dumbass, True)
        self.assertEqual(self.org.x, self.sim.width-1)
        self.assertEqual(self.org.y, self.sim.height-1)

        dumbass = organism.Organism(self.sim, 8, 8, power=10, representing_char='d')

    def test_same_species(self):
        self.reset()
        dumbass = organism.Organism(self.sim, 0, 0, power=8, representing_char='h')
        sensor = sensors.Sensor(self.sim, self.org)
        actuator = actuators.Actuator(self.sim, self.org)
        actuator.actuate = fail_case  # make sure it doesnt happen
        middle = neurons.SameSpecies(self.sim, self.org, outgoing_connections={actuator}, parents=[sensor])
        sensor.activate(dumbass, True)

    def test_mating(self):
        dumbass = organism.Organism(self.sim, 1, 1, parent1=self.org, parent2=self.org)
        print(dumbass.genome)
