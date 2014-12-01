from .point_system import PointSystem


class SimulationParams(object):
    """
    Class representation of the simulation parameters
    """
    def __init__(self, can_reward, pickup_penalty, wall_penalty, stay_put,
                 iterations, steps_per_iter, can_density, env_x, env_y,
                 population_size, num_generations, crossover_prob,
                 mutation_rate, tournament_size, csv_file):
        """
        SimulationParams constructor

        Arguments:
            <TODO - Add documentation>
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
        self.csv_file = csv_file

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
