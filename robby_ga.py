import os
import json
import argparse

from robby_the_robot.simulator import Simulation
from robby_the_robot.simulation_params import SimulationParams


def json_sim_params(args):
    """
    Returns a SimulationParams object from the given JSON file
    """
    if os.path.exists(args.json_config):
        with open(args.json_config, 'r') as f:
            json_dict = json.load(f)
        params = SimulationParams(**json_dict)
    else:
        raise RuntimeError('{0} JSON file does not exist'
                           .format(args.json_config))
    return params


def parse_args():
    """
    Command line argument parser
    """
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(help='sub-commands')

    # JSON file subparser
    json_parser = subparsers.add_parser('json-config', help='json-config')
    json_parser.add_argument('json_config', type=str,
                             help='JSON file containing the configuration'
                                  'for the simulation')
    json_parser.set_defaults(func=json_sim_params)
    # Add other parser here
    return parser.parse_args()


def main():
    """
    Main function
    """
    args = parse_args()

    params = args.func(args)

    simulator = Simulation(params, 8)
    simulator.run_simulation()


if __name__ == '__main__':
    main()
