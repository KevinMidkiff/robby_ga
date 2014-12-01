from robby_the_robot.simulator import Simulation
from robby_the_robot.simulation_params import SimulationParams
from robby_the_robot.robby_the_robot import RobbyTheRobot
from robby_the_robot.utils import generate_strategy


def main():
    params = SimulationParams(10, 1, 5, 0, 20, 200, 0.5, 10, 10, 100, 100, 0, 0.05, 15, 'test_result.csv')
    simulator = Simulation(params, 20)
    simulator.run_simulation()


if __name__ == '__main__':
    main()
    # r = RobbyTheRobot(
    #     SimulationParams(10, 1, 5, 0, 20, 100, 0.5, 10, 10, 100, 0, 0.5, 0.05, 15),
    #     generate_strategy())
    # r.run()
    # print 'Fitness:', r.fitness
