import random


class Point(object):
    """
    Represents a point in the environment
    """
    def __init__(self, x, y):
        """
        Point class constructor

        Arguments:
            x - x coordinate
            y - y coordinate
        """
        self.x = x
        self.y = y

    def __str__(self):
        """
        String representation of the Point class
        """
        return '({0}, {1})'.format(self.x, self.y)

    def __getstate__(self):
        """
        Used for serializing between the processes
        """
        return self.__dict__.copy()

    def __setstate__(self, state):
        """
        Used for restoring after being serialized
        """
        self.__dict__.update(state)


def generate_strategy(size, chars):
    """
    Generates a string os size, "size", composed of the characters, "chars".

    Arguments:
        size  - Size of the string to generate
        chars - List of characters to use in the string
    """
    return str(''.join(random.choice(chars) for _ in range(size)))
