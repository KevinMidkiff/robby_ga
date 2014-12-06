import signal
import multiprocessing as mp
import random
import datetime
import csv
from concurrent.futures import ThreadPoolExecutor

# Robby the robot library imports
from .robby_the_robot import RobbyTheRobot
# from .utils import generate_strategy
from . import utils


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


def repitition_worker(sim_params):
    """
    Worker for a repitition
    """
    num_gens = sim_params.num_generations
    curr_gen = utils.init_generation(sim_params)
    results = []

    with ThreadPoolExecutor(max_workers=4) as executor:
        for i in range(0, num_gens):
            # print('Running Generation:', i + 1)
            curr_gen = list(executor.map(pool_worker, curr_gen))
            results.append(list(curr_gen))
            curr_gen = utils.create_next_generation(sim_params, curr_gen)

    return results


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
        # self.current_generation = []
        self.start_timestamp = None
        self.gen_results = {}

    def run_simulation(self):
        """
        Runs the simulation
        """
        self.pool = mp.Pool(processes=self.num_workers,
                            initializer=init_worker,
                            maxtasksperchild=10)
        self.start_timestamp = datetime.datetime.now()
        reps = self.sim_params.repititions
        # num_gens = self.sim_params.num_generations
        # name = self.sim_params.experiment_name
        print('Running simulation...')
        # ps = []
        params = []

        # for i in range(0, reps):
            # ps.append(mp.Process(target=repitition_worker,
                                 # args=(self.sim_params,)))
            # ps[-1].start()

        for i in range(0, reps):
            # ps[i].join()
            params.append(self.sim_params)
        self.gen_results = self.pool.map(repitition_worker, params)
        print(len(self.gen_results))

        # for i in range(0, reps):
        #     print('Running Repitition:', i + 1)
        #     results = []
        #     curr_gen = utils.init_generation(self.sim_params)
        #     for j in range(0, num_gens):
        #         print('Running Generation:', j + 1)
        #         curr_gen = self.pool.map(pool_worker, curr_gen)
        #         results.append(list(curr_gen))
        #         curr_gen = utils.create_next_generation(self.sim_params, curr_gen)
        #     key = '{0}_run_{1}'.format(name, str(i))
        #     self.gen_results[key] = list(results)

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
        # print( self.gen_results)
        idx = 1

        for results in self.gen_results:
            name = '{0}_run_{1}.csv'.format(
                self.sim_params.experiment_name,
                str(idx))
            csv_writer = csv.DictWriter(
                open(name, 'w'),
                fieldnames=['Generation', 'Fitness'],
                delimiter=',', lineterminator='\n')
            jdx = 1

            csv_writer.writeheader()

            for result in results:
                result = sorted(result, reverse=True)
                csv_writer.writerow(
                    {'Generation': str(jdx),
                     'Fitness': result[0].fitness})
                jdx += 1
            idx += 1

    # def _init_first_generation(self):
    #     """
    #     Creates the initial randomly generated generation
    #     """
    #     generation = []
    #     if self.sim_params.complex:
    #         size = 19683
    #         chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    #     else:
    #         size = 243
    #         chars = ['0', '1', '2', '3', '4', '5', '6']

    #     for i in range(0, self.sim_params.population_size):
    #         strategy = generate_strategy(size, chars)
    #         robby = RobbyTheRobot(self.sim_params, strategy)
    #         generation.append(robby)
    #     return generation

    # def _create_next_generation(self, curr_gen):
    #     """
    #     Private function for creating the next generation from the one given
    #     to it.
    #     """
    #     num_strategies = self.sim_params.population_size - 1
    #     half_gen_size = int(self.sim_params.population_size / 2)
    #     tournament_size = self.sim_params.tournament_size

    #     new_generation = []

    #     for i in range(0, half_gen_size):
    #         tournament = []

    #         for j in range(0, tournament_size):
    #             idx = random.randint(0, num_strategies)
    #             tournament.append(curr_gen[idx])

    #         parent1 = tournament[0]
    #         parent2 = tournament[1]

    #         child1_strategy, child2_strategy = self._crossover(
    #             parent1.strategy, parent2.strategy)

    #         # Mutating the strategy
    #         child1_strategy = self._mutate(child1_strategy)
    #         child2_strategy = self._mutate(child2_strategy)

    #         child1 = RobbyTheRobot(self.sim_params, child1_strategy)
    #         child2 = RobbyTheRobot(self.sim_params, child2_strategy)

    #         new_generation.append(child1)
    #         new_generation.append(child2)

    #     return new_generation

    # def _crossover(self, strategy1, strategy2):
    #     """
    #     Private function for crossing-over the two given strategies.

    #     Returns two new strategies comprised of the two given. If the
    #     crossover probability was set in the

    #     Arguments:
    #         strategy1 - The first strategy to use in the crossover
    #         strategy2 - The second strategy to use in the crossover
    #     """
    #     if random.random() < self.sim_params.crossover_prob:
    #         strategy_len = len(strategy1)
    #         split_point = random.randint(0, strategy_len)
    #         child1 = strategy1[0:split_point] + \
    #             strategy2[split_point:strategy_len]
    #         child2 = strategy2[0:split_point] + \
    #             strategy1[split_point:strategy_len]
    #     else:
    #         child1 = strategy1
    #         child2 = strategy2

    #     return child1, child2

    # def _mutate(self, strategy):
    #     """
    #     Mutates the given strategy
    #     """
    #     len_strategy = len(strategy)

    #     if self.sim_params.complex:
    #         max_idx = 10
    #     else:
    #         max_idx = 6

    #     for i in range(0, len_strategy):
    #         if random.random() < self.sim_params.mutation_rate:
    #             strategy = strategy[:i] + str(random.randint(0, max_idx)) +\
    #                 strategy[i:]
    #     return strategy

    def _signal_handler(self, signum, frame):
        """
        Private method to handle CTRL-C being pressed, cleans up all process
        pool.
        """
        pass
        # Terminating process pool
        # if self.pool is not None:
            # if self.pool.is_alive():
            # self.pool.terminate()

        # Writing any results
        # if self.result_generations:
            # self._write_results()
