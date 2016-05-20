import sim_tools
import random
import time

class Actuator:
    """ Only actuates on all organisms. "targets" can be False.
    """
    def __init__(self, sim, org):
        from sim import Simulation
        from organism import Organism
        assert isinstance(sim, Simulation)
        assert isinstance(org, Organism)
        self.sim = sim
        self.org = org
        self.parents = set()

    def add_parent(self, parent):
        self.parents.add(parent)

    def actuate(self, target):
        """
        Actuates on an organism. Perhaps eventually an erroneous assumption,
        but works for now (there is nothing other than organisms)
        """
        assert False  # this must be overwritten by the actuator

    def default(self):
        """
        What gets called if target == None
        """
        return

    def activate(self, target, signal, parent=None):
        if signal == False:
            return
        if target is not None:
            self.actuate(target)
        else:
            self.default()


class MoveActuator(Actuator):
    """
    Performs an action when it recieves a signal.
    """
    def __init__(self, sim, org, delta_x=0, delta_y=0):
        super().__init__(sim, org)
        self.delta_x = delta_x
        self.delta_y = delta_y

    def actuate(self, target) -> None:
        self.sim[self.org.x][self.org.y].remove(self.org)
        self.org.x += self.delta_x
        self.org.y += self.delta_y
        self.org.x = self.org.x % self.sim.width
        self.org.y = self.org.y % self.sim.height
        self.sim[self.org.x][self.org.y].append(self.org)


class TowardsActuator(MoveActuator):
    def default(self):
        # If target is None, move in a random direction
        self.delta_x = random.choice([-1, 0, 1])
        self.delta_y = random.choice([-1, 0, 1])
        super().actuate(None)

    def actuate(self, target):
        assert target is not None
        import math
        if target.x == self.org.x:
            self.delta_x = 0
        else:
            self.delta_x = math.copysign(1, target.x - self.org.x)  # if i am at (5,0) and target is at (7,0), we want to return 1.
        if target.y == self.org.y:
            self.delta_y = 0
        else:
            self.delta_y = math.copysign(1, target.y - self.org.y)  # if i am at (0,8) and target is at (0,10), we want to return 1.
        self.delta_x = int(self.delta_x)
        self.delta_y = int(self.delta_y)
        super().actuate(target)

class AwayActuator(MoveActuator):
    def default(self):
        # If target is None, move in a random direction
        self.delta_x = random.choice([-1, 0, 1])
        self.delta_y = random.choice([-1, 0, 1])
        super().actuate(None)

    def actuate(self, target):
        assert target is not None
        import math
        if target.x == self.org.x:
            self.delta_x = random.choice([-1, 1])
        else:
            self.delta_x = math.copysign(1, -(target.x - self.org.x))  # if i am at (5,0) and target is at (7,0), we want to return -1.
        if target.y == self.org.y:
            self.delta_y = random.choice([-1, 1])
        else:
            self.delta_y = math.copysign(1, -(target.y - self.org.y))  # if i am at (0,8) and target is at (0,10), we want to return -1.
        self.delta_x = int(self.delta_x)
        self.delta_y = int(self.delta_y)
        super().actuate(target)


class AttackActuator(Actuator):
    """
    Can battle another organism if they're one unit away from you
    """
    def actuate(self, target):
        """
        Only attack if Check if the target(s) is(are) 1 unit away
        """
        if not sim_tools.is_n_units_away((self.org.x, self.org.y), (target.x, target.y), 1):
            return  # if they try to attack something that's more than one unit away
        self.org.power += 1  # reward for being aggressive
        prob_victory = self.org.power / (self.org.power + target.power)
        won_battle = sim_tools.bernoulli(prob_victory)
        if won_battle:
            winner = self.org
            loser = target
        else:
            winner = target
            loser = self.org
        self.sim.remove(loser)
        winner.kills += 1
        winner.hunger = 0
        winner.power += 1  # reward for winning


class MateActuator(Actuator):
    """
    Can mate with another organism if they're one unit away from you
    """
    def actuate(self, target):
        """ Returns the baby of self.organism and target, to-be-placed where they are """
        if not sim_tools.is_n_units_away((self.org.x, self.org.y), (target.x, target.y), 1):
            return  # if they try to mate with something that's more than 1 unit away
        if self.org.representing_char != target.representing_char:
            #  TODO: maybe allow orgs of different species to mate? just with unfavorable outcomes
            #        (i.e. choose the min of the powers, not the avg)
            return
        if not self.org.able_to_mate() or not target.able_to_mate():
            return
        power_avg = (target.power + self.org.power) / 2
        parent_coords = (self.org.x, self.org.y)
        my_char = sim_tools.bernoulli(0.5)
        if my_char:
            char = self.org.representing_char
        else:
            char = target.representing_char
        baby = self.sim.spawn_new_life(coords=parent_coords, representing_char=char,
                                       power=power_avg, parents=(self.org, target))
        self.org.mate_timeout = target.mate_timeout = time.time() + 30
        return baby

