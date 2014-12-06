import datetime
from .environment import Environment
from .movement_maps import COMPLEX, SIMPLE


class RobbyTheRobot(object):
    """
    Class representation of Robby the Robot
    """
    def __init__(self, simulation_params, strategy):
        """
        RobbyTheRobot constructor

        Arguments:
            <ADD DOCUMENTATION>
        """
        self.strategy = strategy
        self.fitness = None
        self.sim_params = simulation_params
        self.run_time = None

        # dictionary representing each move
        if self.sim_params.complex:
            self.movement_map = COMPLEX
        else:
            self.movement_map = SIMPLE

        # self.movement_map = [
            # 'move_north',
            # 'move_northwest',
            # 'move_west',
            # 'move_southwest',
            # 'move_south',
            # 'move_southeast',
            # 'move_east',
            # 'move_northeast',
            # 'pick_up',
            # 'stay'
        # ]

    def run(self):
        """
        Runs the instance of Robby the Robot for in randomly generated
        environments based on the given simulation parameters.

        Arguments:
            iterations - Number of environment to run robby in
        """
        best_fitness = None
        num_iter = self.sim_params.iterations
        steps = self.sim_params.steps_per_iteration
        start_timestamp = datetime.datetime.now()

        for i in range(0, num_iter):
            cur_fitness = 0
            env = Environment(
                self.sim_params.env_x, self.sim_params.env_y,
                self.sim_params.can_density, self.sim_params.point_system,
                self.sim_params.complex)

            for j in range(0, steps):
                move_idx = int(self.strategy[j])
                movement = self.movement_map[move_idx]
                move_func = getattr(env, movement)
                cur_fitness += move_func()

            if self.fitness is not None:
                if cur_fitness > best_fitness:
                    best_fitness = cur_fitness
            else:
                best_fitness = cur_fitness

        self.fitness = best_fitness
        td = datetime.datetime.now() - start_timestamp
        self.run_time = '{0}.{1}'.format(str(td.seconds),
                                         str(td.microseconds).rjust(6, '0'))

    def __gt__(self, other):
        """
        Overridden greater than function for comparing Robbys to each other
        """
        return self.fitness > other.fitness

    def __ge__(self, other):
        """
        Overridden greater than or equal function for comparing Robbys to
        each other
        """
        return self.fitness >= other.fitness

    def __lt__(self, other):
        """
        Overridden less than function for comparing Robbys to
        each other
        """
        return self.fitness < other.fitness

    def __le__(self, other):
        """
        Overridden less than or equal function for comparing Robbys to
        each other
        """
        return self.fitness <= other.fitness

    def __getstate__(self):
        """
        Used for serializing the class
        """
        return self.__dict__.copy()

    def __setstate__(self, state):
        """
        Used for restoring after serialization
        """
        self.__dict__.update(state)
