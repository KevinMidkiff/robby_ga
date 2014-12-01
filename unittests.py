import unittest
from robby_the_robot.robby_the_robot import RobbyTheRobot
from robby_the_robot.utils import generate_strategy
from robby_the_robot.simulation_params import SimulationParams


class RobbyUnitTests(unittest.TestCase):
    def test_robby_the_robot(self):
        """
        Tests the running of a single instance of Robby the Robot
        """
        params = SimulationParams(
            can_reward=10,
            pickup_penalty=1,
            wall_penalty=5,
            stay_put=0,
            iterations=20,
            steps_per_iter=100,
            can_density=0.5,
            env_x=10,
            env_y=10,
            population_size=200,
            num_generations=50,
            crossover_prob=0,
            mutation_rate=0.05,
            tournament_size=15,
            csv_file='test_result.csv')
        strategy = generate_strategy()
        rr = RobbyTheRobot(params, strategy)
        rr.run()


if __name__ == '__main__':
    unittest.main()
