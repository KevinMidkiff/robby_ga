from .point_system import PointSystem


class SimulationParams(object):
    """
    Class representation of the simulation parameters
    """
    def __init__(self, can_reward, pickup_penalty, wall_penalty, stay_put,
                 iterations, steps_per_iter, can_density, env_x, env_y,
                 population_size, num_generations, crossover_prob,
                 mutation_rate, tournament_size, repititions,
                 experiment_name, complex):
        """
        SimulationParams constructor

        Arguments:
            can_reward      - Number of points to reward for picking up a can
            pickup_penalty  - Number of points to deduct for trying to pick up
                              a can in an empty square
            wall_penalty    - Number of points to deduct for running into the
                              wall
            stay_put        - Number of points to deduct for staying put
            iterations      - Number of iterations to run each Robby
            steps_per_iter  - Number of steps to run each Robby in the current
                              environment
            can_density     - Density of cans in the environment
            env_x           - X dimension of the environment grid
            env_y           - Y dimension of the environment grid
            population_size - Number of Robby’s in each generation
            num_generations -   Number of generations to run the simulation
            crossover_prob  - Probability of two strategies to be crossed over
            mutation_rate   - The probability of each action in a strategy to
                              be mutated
            tournament_size - Size of the tournament to select parents from
            repititions     - Number of repetitions to run each simulation
            experiment_name - Name of the simulation
            complex         - Boolean value for which movement map to use

        """
        self.point_system = PointSystem(can_reward, pickup_penalty,
                                        wall_penalty, stay_put)
        self.iterations = iterations
        self.steps_per_iteration = steps_per_iter
        self.can_density = can_density
        self.env_x = env_x
        self.env_y = env_y
        self.population_size = population_size
        self.num_generations = num_generations
        self.crossover_prob = crossover_prob
        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size
        self.repititions = repititions
        self.experiment_name = experiment_name
        self.complex = complex

    def __getstate__(self):
        """
        Used for serializing the class`
        """
        return self.__dict__.copy()

    def __setstate__(self, state):
        """
        Used for restoring the class
        """
        self.__dict__.update(state)
