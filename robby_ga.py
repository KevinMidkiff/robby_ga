import os
import json
import argparse
import traceback

from robby_the_robot.simulator import Simulation
from robby_the_robot.simulation_params import SimulationParams


def json_sim_params(json_configs):
    """
    Returns a SimulationParams object from the given JSON file
    """
    params = []

    for config_file in json_configs:
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                json_dict = json.load(f)
            params.append(SimulationParams(**json_dict))
        else:
            raise RuntimeError('{0} JSON file does not exist'
                               .format(config_file))
    return params


def parse_args():
    """
    Command line argument parser
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('json_configs', type=str, nargs='+',
                        help='JSON file containing the configuration '
                             'for the simulation')
    parser.add_argument('-num-workers', dest='num_workers', type=int,
                        default=4,
                        help='Number of processes to use to run the '
                             'simulation')
    return parser.parse_args()


def main():
    """
    Main function
    """
    args = parse_args()
    params = json_sim_params(args.json_configs)

    try:
        for param in params:
            simulator = Simulation(param, args.num_workers)
            simulator.run_simulation()
    except KeyboardInterrupt:
        pass
    except:
        print('Encountered the following error:')
        traceback.print_exc()


if __name__ == '__main__':
    main()
