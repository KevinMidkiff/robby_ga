from .environment import Environment


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

        # dictionary representing each move
        self.movement_map = [
            'move_north',
            'move_northwest',
            'move_west',
            'move_southwest',
            'move_south',
            'move_southeast',
            'move_east',
            'move_northeast',
            'pick_up',
            'stay'
        ]

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

        for i in range(0, num_iter):
            cur_fitness = 0
            env = Environment(
                self.sim_params.env_x, self.sim_params.env_y,
                self.sim_params.can_density, self.sim_params.point_system)

            for j in range(0, steps):
                movement = self.movement_map[int(self.strategy[j])]
                move_func = getattr(env, movement)
                cur_fitness += move_func()

            if self.fitness is not None:
                if cur_fitness > best_fitness:
                    best_fitness = cur_fitness
            else:
                best_fitness = cur_fitness

        self.fitness = best_fitness

    def __repr__(self):
        return str(self.fitness)

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
