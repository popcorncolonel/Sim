import sim_tools


class Actuator:
    def __init__(self, sim, org):
        from sim import Simulation
        from organism import Organism
        assert isinstance(sim, Simulation)
        assert isinstance(org, Organism)
        self.sim = sim
        self.organism = org

    def activate(self, *args):
        pass


class MoveActuator(Actuator):
    """
    Performs an action when it recieves a signal.
    """
    def __init__(self, sim, organism, delta_x=0, delta_y=0):
        super().__init__(sim, organism)
        self.delta_x = delta_x
        self.delta_y = delta_y

    def activate(self, target=None, parent=None) -> None:
        # TODO: turn this intervace into a TowardsActuator and an AwayActuator that
        #       takes in an argument (target is a list now!!!) and goes
        #       towards/away from something, using THESE moveactuators
        if target == False:
            return
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
    def activate(self, target, parent=None):
        """
        Check if theyre 1 unit away

        :type target: Organism
        """
        if False:  # if they try to attack something that's more than one unit away
            return
        if not target:
            return
        # TODO: TARGET IS A LIST OF ORGANISMS NOW. What do i do about it??? random.choice from the list of organisms? attack all?
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
    def activate(self, target, parent=None):
        """ Returns the baby of self.organism and target, to-be-placed where they are """
        if False:  # if they try to mate with something that's more than 1 unit away
            return
        if not target:
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
    pass