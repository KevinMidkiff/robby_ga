import random
from robby_the_robot.robby_the_robot import RobbyTheRobot


def generate_strategy(size, chars):
    """
    Generates a string os size, "size", composed of the characters, "chars".

    Arguments:
        size  - Size of the string to generate
        chars - List of characters to use in the string
    """
    return str(''.join(random.choice(chars) for _ in range(size)))


def init_generation(sim_params):
    """
    Creates randomly generated generation
    """
    generation = []
    if sim_params.complex:
        size = 19683
        chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    else:
        size = 243
        chars = ['0', '1', '2', '3', '4', '5', '6']

    for i in range(0, sim_params.population_size):
        strategy = generate_strategy(size, chars)
        robby = RobbyTheRobot(sim_params, strategy)
        generation.append(robby)
    return generation


def crossover(sim_params, strategy1, strategy2):
    """
    Function for crossing-over the two given strategies.

    Returns two new strategies comprised of the two given. If the
    crossover probability was set in the

    Arguments:
        strategy1 - The first strategy to use in the crossover
        strategy2 - The second strategy to use in the crossover
    """
    if random.random() < sim_params.crossover_prob:
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


def mutate(sim_params, strategy):
    """
    Mutates the given strategy
    """
    len_strategy = len(strategy)

    if sim_params.complex:
        max_idx = 10
    else:
        max_idx = 6

    for i in range(0, len_strategy):
        if random.random() < sim_params.mutation_rate:
            strategy = strategy[:i] + str(random.randint(0, max_idx)) +\
                strategy[i:]
    return strategy


def create_next_generation(sim_params, curr_gen):
    """
    Function for creating the next generation from the one given to it.
    """
    num_strategies = sim_params.population_size - 1
    half_gen_size = int(sim_params.population_size / 2)
    tournament_size = sim_params.tournament_size

    new_generation = []

    for i in range(0, half_gen_size):
        tournament = []

        for j in range(0, tournament_size):
            idx = random.randint(0, num_strategies)
            tournament.append(curr_gen[idx])

        parent1 = tournament[0]
        parent2 = tournament[1]

        child1_strategy, child2_strategy = crossover(
            sim_params, parent1.strategy, parent2.strategy)

        # Mutating the strategy
        child1_strategy = mutate(sim_params, child1_strategy)
        child2_strategy = mutate(sim_params, child2_strategy)

        child1 = RobbyTheRobot(sim_params, child1_strategy)
        child2 = RobbyTheRobot(sim_params, child2_strategy)

        new_generation.append(child1)
        new_generation.append(child2)

    return new_generation
