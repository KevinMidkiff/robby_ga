Robby GA
========
## Synopsis

This project runs a genetic algorithm for the following situation:

Robby the Robot is put into an n X m environment where each square either contains an can or does not.  Robby has 9 choices he can make in a given situaion:
    1. Move North
    2. Move Northwest
    3. Move West
    4. Move Southwest
    5. Move South
    6. Move Southeast
    7. Move East
    8. Stay put
    9. Pickup a can

In the configuration file there is a point system specified. There are points awarded for staying put and picking up a can.  There are points deducted for running into a wall or trying to pickup a can in an empty square.

What Robby decides to do is based on a string of integers where each integer corresponds to an action to take.  The best fitness for that Robby is recorded and the time it took to run the simulation.

The simulation runs for the given amount of generations and runs each inidividual Robby for the given amount of iteractions and given amount of ticks (steps) per iteraction.

The simulation is driven from a JSON configuration file.  See the **Code Example** section below for an example.

## Requirements

This library requires Python 2.7.

## Code Example

As mentioned above the simulation is driven off of a configuration file.  An example is shown below.

```json
{
    "experiment_name": "example",
    "complex": true,
    "repititions": 5,
    "can_reward": 10,
    "pickup_penalty": 1,
    "wall_penalty": 5,
    "stay_put": 0,
    "iterations": 20,
    "steps_per_iter": 100,
    "can_density": 0.5,
    "env_x": 10,
    "env_y": 10,
    "population_size": 200,
    "num_generations": 50,
    "crossover_prob": 0,
    "mutation_rate": 0.05,
    "tournament_size": 15,
}
```

To run a configuration from the command line, simply do run the following:

```sh
$ python robby_ga.py example-config.json
```

## Motivation

The motivation behind this project was a class I am taking at Portland State University,

## Installation

The only requirement is Python 2.7.  Then just run robby_ga.py by giving it a JSON file as shown in the **Code Example** section above.

## License

There is no license. This software is provided AS-IS with no support from the developer.
