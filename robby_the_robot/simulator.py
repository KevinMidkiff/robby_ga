import signal
import multiprocessing as mp

import datetime
import csv

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


def worker(rep_idx, sim_params, out_q):
    """
    Pool worker method
    """
    num_gens = sim_params.num_generations
    curr_gen = utils.init_generation(sim_params)
    pool = mp.Pool(processes=8,
                   initializer=init_worker)
    results = []

    def signal_handler(signum, frame):
        """
        Signal handler
        """
        pool.terminate()
        pool.join()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    for i in range(0, num_gens):
        start = datetime.datetime.now()
        curr_gen = pool.map(pool_worker, curr_gen)
        results.append(list(curr_gen))
        curr_gen = utils.create_next_generation(sim_params, curr_gen)
        print('Repetition', rep_idx, '- Generation', i, 'Run time',
              datetime.datetime.now() - start)
    out_q.put(results)


def write_results(results, name):
    """
    Writes results for the simulation.

    Arguments:
        results - Results to record
        name    - Name of the simulation
    """
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
    """
    Runs the simulation
    """
    out_q = mp.Queue()
    num_procs = sim_params.repititions
    start_timestamp = datetime.datetime.now()
    procs = []

    def signal_handler(signum, frame):
        """
        Signal handler to take care of the processes
        """
        print('Quitting...')
        for proc in procs:
            proc.terminate()
            proc.join()

    print('Running experiment:', sim_params.experiment_name)

    # Starting processes
    for i in range(num_procs):
        p = mp.Process(
            target=worker,
            args=(i, sim_params, out_q))
        procs.append(p)
        p.start()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    results = []
    for i in range(num_procs):
        results.append(out_q.get())

    print('Writing results to CSV...')
    write_results(results, sim_params.experiment_name)
    print('Finished', datetime.datetime.now() - start_timestamp)
