import sim_tools
import random

class Actuator:
    """ Only actuates on all organisms. "targets" can be False.
    """
    def __init__(self, sim, org):
        from sim import Simulation
        from organism import Organism
        assert isinstance(sim, Simulation)
        assert isinstance(org, Organism)
        self.sim = sim
        self.organism = org

    def actuate(self, target):
        """
        Actuates on an organism. Perhaps eventually an erroneous assumption,
        but works for now (there is nothing other than organisms)
        """
        assert False  # this must be overwritten by the actuator

    def activate(self, target=None, signal=None, parent=None):
        assert signal is not None
        if signal == False:
            return
        self.actuate(target)


class MoveActuator(Actuator):
    """
    Performs an action when it recieves a signal.
    """
    def __init__(self, sim, organism, delta_x=0, delta_y=0):
        super().__init__(sim, organism)
        self.delta_x = delta_x
        self.delta_y = delta_y

    def actuate(self, target) -> None:
        # TODO: turn this intervace into a TowardsActuator and an AwayActuator that
        #       takes in an argument (target is a list now!!!) and goes
        #       towards/away from something, using THESE moveactuators
        self.sim[self.organism.x][self.organism.y].remove(self.organism)
        self.organism.x += self.delta_x
        self.organism.y += self.delta_y
        self.organism.x = self.organism.x % self.sim.width
        self.organism.y = self.organism.y % self.sim.height
        self.sim[self.organism.x][self.organism.y].add(self.organism)


class AttackActuator(Actuator):
    """
    Can battle another organism if they're one unit away from you
    """
    def actuate(self, target):
        """
        Only attack if Check if the target(s) is(are) 1 unit away
        """
        if False:  # if they try to attack something that's more than one unit away
            return
        prob_victory = self.organism.power / (self.organism.power + target.power)
        won_battle = sim_tools.bernoulli(prob_victory)
        if won_battle:
            winner = self.organism
            loser = target
        else:
            winner = target
            loser = self.organism
        self.sim.remove(loser)
        winner.kills += 1
        winner.hunger = 0
        winner.power += 1


class MateActuator(Actuator):
    """
    Can mate with another organism if they're one unit away from you
    """
    def actuate(self, target):
        """ Returns the baby of self.organism and target, to-be-placed where they are """
        if False:  # if they try to mate with something that's more than 1 unit away
            return
        power_avg = (target.power + self.organism.power) / 2
        parent_coords = (self.organism.x, self.organism.y)
        #  TODO: combine the sensors of this organism and the target
        my_char = sim_tools.bernoulli(0.5)
        if my_char:
            char = self.organism.representing_char
        else:
            char = target.representing_char
        baby = self.sim.spawn_new_life(coords=parent_coords, representing_char=char, power=power_avg)
        return baby
