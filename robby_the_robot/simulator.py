import signal
import math
from queue import Queue
import multiprocessing as mp
import time

import datetime
import csv
from concurrent.futures import ThreadPoolExecutor

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


def repitition_worker(params):
    """
    Worker for a repitition
    """
    rep_idx, sim_params = params
    num_gens = sim_params.num_generations
    curr_gen = utils.init_generation(sim_params)
    results = []

    with ThreadPoolExecutor(max_workers=4) as executor:
        for i in range(0, num_gens):
            print('Repetition:', str(rep_idx), '- Generation:', str(i))
            curr_gen = list(executor.map(pool_worker, curr_gen))
            results.append(list(curr_gen))
            curr_gen = utils.create_next_generation(sim_params, curr_gen)

    return results


def worker(rep_idx, sim_params, out_q):
    num_gens = sim_params.num_generations
    curr_gen = utils.init_generation(sim_params)
    pool = mp.Pool(processes=8)
    results = []

    for i in range(0, num_gens):
        start = datetime.datetime.now()
        curr_gen = pool.map(pool_worker, curr_gen)
        results.append(list(curr_gen))
        curr_gen = utils.create_next_generation(sim_params, curr_gen)
        print('Repetition', rep_idx, '- Generation', i, 'Run time',
              datetime.datetime.now() - start)
    out_q.put(results)


def write_results(results, name):
    num_results = len(results)
    for i in range(num_results):
        csv_name = '{0}_run_{1}.csv'.format(name, str(i))
        csv_writer = csv.DictWriter(
            open(csv_name, 'w'),
            fieldnames=['Generation', 'Fitness'],
            delimiter=',', lineterminator='\n')
        jdx = 1

        csv_writer.writeheader()

        for result in results[i]:
            result = sorted(result, reverse=True)
            csv_writer.writerow(
                {'Generation': str(jdx),
                 'Fitness': result[0].fitness})
            jdx += 1


def run_simulation(sim_params):
    out_q = mp.Queue()
    num_procs = sim_params.repititions
    start_timestamp = datetime.datetime.now()
    procs = []

    print('Running experiment:', sim_params.experiment_name)

    # Starting processes
    for i in range(num_procs):
        p = mp.Process(
            target=worker,
            args=(i, sim_params, out_q))
        procs.append(p)
        p.start()

    results = []
    for i in range(num_procs):
        results.append(out_q.get())

    print('Writing results to CSV...')
    write_results(results, sim_params.experiment_name)
    print('Finished', datetime.datetime.now() - start_timestamp)


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
        self.start_timestamp = None
        self.gen_results = {}

    def run_simulation(self):
        """
        Runs the simulation
        """
        self.pool = mp.Pool(processes=self.num_workers,
                            initializer=init_worker)
        self.start_timestamp = datetime.datetime.now()
        reps = self.sim_params.repititions
        params = []

        for i in range(0, reps):
            params.append((i+1, self.sim_params))

        print('Running simulation...')
        self.gen_results = self.pool.map(repitition_worker, params)

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

    def _signal_handler(self, signum, frame):
        """
        Private method to handle CTRL-C being pressed, cleans up all process
        pool.
        """
        pass
