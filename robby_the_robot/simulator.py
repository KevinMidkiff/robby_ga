import signal
import multiprocessing as mp
import random
import datetime
import csv

# Robby the robot library imports
from .robby_the_robot import RobbyTheRobot
from .utils import generate_strategy


def init_worker():
    """
    Function to initialize a worker
    """
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def pool_worker(robby):
    """
    Worker function for running one instance of Robby the Robot
    """
    robby.run()
    return robby


class Simulation(object):
    """
    Class representation of the simulation.
    """
    def __init__(self, simulation_params, num_workers):
        """
        Simulation class constructor

        Arguments:
            <ADD DOCUMENTATION>
        """
        # Setting up signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        self.sim_params = simulation_params
        self.num_workers = num_workers
        self.pool = None
        self.current_generation = []
        self.start_timestamp = None
        self.result_generations = []

    def run_simulation(self):
        """
        Runs the simulation
        """
        self.pool = mp.Pool(processes=self.num_workers,
                            initializer=init_worker)
        self._init_first_generation()
        self.start_timestamp = datetime.datetime.now()
        print('Running simulation...')

        for i in range(0, self.sim_params.num_generations):
            self.current_generation = self.pool.map(pool_worker,
                                                    self.current_generation)
            self.result_generations.append(list(self.current_generation))
            self._create_next_generation()

        self._write_results()
        self.pool.close()
        self.pool.terminate()
        self.pool.join()
        print('Finished', datetime.datetime.now() - self.start_timestamp)

    def _write_results(self):
        """
        Private method to write the results of the experiment
        """
        print('Creating results CSV...')
        csv_writer = csv.DictWriter(
            open(self.sim_params.csv_file, 'w'),
            fieldnames=['Generation', 'Best Average Fitness', 'Run Time'],
            delimiter=',', lineterminator='\n')
        idx = 1

        csv_writer.writeheader()

        for gen in self.result_generations:
            gen = sorted(gen, reverse=True)
            csv_writer.writerow(
                {'Generation': str(idx),
                 'Best Average Fitness': gen[0].fitness,
                 'Run Time': gen[0].run_time})
            idx += 1

    def _init_first_generation(self):
        """
        Creates the initial randomly generated generation
        """
        for i in range(0, self.sim_params.population_size):
            strategy = generate_strategy()
            robby = RobbyTheRobot(self.sim_params, strategy)
            self.current_generation.append(robby)

    def _create_next_generation(self):
        """
        Private function for creating the next generation from the one given
        to it.
        """
        num_strategies = self.sim_params.population_size - 1
        half_gen_size = int(self.sim_params.population_size / 2)

        new_generation = []

        for i in range(0, half_gen_size):
            tournament = []

            for j in range(0, self.sim_params.tournament_size):
                idx = random.randint(0, num_strategies)
                tournament.append(self.current_generation[idx])

            parent1 = tournament[0]
            parent2 = tournament[1]

            child1_strategy, child2_strategy = self._crossover(
                parent1.strategy, parent2.strategy)
            # parent1.strategy = child1
            # parent2.strategy = child2

            # Mutating the strategy
            child1_strategy = self._mutate(child1_strategy)
            child2_strategy = self._mutate(child2_strategy)

            child1 = RobbyTheRobot(self.sim_params, child1_strategy)
            child2 = RobbyTheRobot(self.sim_params, child2_strategy)

            new_generation.append(child1)
            new_generation.append(child2)

            # print '##########################################'
            # print 'Parent1 strategy:\n\t', parent1.strategy
            # print 'Parent2 strategy:\n\t', parent2.strategy
            # print 'Child1 strategy:\n\t', child1.strategy
            # print 'Child2s strategy:\n\t', child2.strategy
            # print '##########################################\n'

        self.current_generation = new_generation

    def _crossover(self, strategy1, strategy2):
        """
        Private function for crossing-over the two given strategies.

        Returns two new strategies comprised of the two given. If the
        crossover probability was set in the

        Arguments:
            strategy1 - The first strategy to use in the crossover
            strategy2 - The second strategy to use in the crossover
        """
        if random.random() < self.sim_params.crossover_prob:
            strategy_len = len(strategy1)
            split_point = random.randint(0, strategy_len)
            child1 = strategy1[0:split_point] + \
                strategy2[split_point:strategy_len]
            child2 = strategy2[0:split_point] + \
                strategy1[split_point:strategy_len]
        else:
            child1 = strategy1
            child2 = strategy2

        return child1, child2

    def _mutate(self, strategy):
        """
        Mutates the given strategy
        """
        len_strategy = len(strategy)
        for i in range(0, len_strategy):
            if random.random() < self.sim_params.mutation_rate:
                strategy = strategy[:i] + str(random.randint(0, 9)) +\
                    strategy[i:]
        return strategy

    def _signal_handler(self, signum, frame):
        """
        Private method to handle CTRL-C being pressed, cleans up all process
        pool.
        """
        # pass
        # Terminating process pool
        if self.pool is not None:
            # if self.pool.is_alive():
            self.pool.terminate()

        # Writing any results
        # if self.result_generations:
            # self._write_results()
