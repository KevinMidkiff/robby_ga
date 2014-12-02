import random
from operator import sub as subtract
from operator import add

from .utils import Point


class Environment(object):
    """
    Class representation of an environment for Robby
    """
    def __init__(self, x, y, can_density, point_system):
        """
        Envrionment Class constructor

        Arguments:
            <ADD DOCUMENTATION>
        """
        self.can_density = can_density
        self.point_system = point_system
        self.map = [[self._has_can() for j in range(x)] for i in range(y)]
        self.cur_pos = Point(0, y - 1)

    def _has_can(self):
        """
        Private function for determining if a site has a can
        """
        return random.random() < self.can_density

    def _move(self, move_x=False, move_y=False):
        """
        Moves in the map
        """
        points = 0
        position = Point(self.cur_pos.x, self.cur_pos.y)

        if move_x:
            position.x = move_x(position.x, 1)

        if move_y:
            position.y = move_y(position.y, 1)

        try:
            # Verifying that neither of the positions are equal to -1
            assert position.y != -1 and position.x != -1

            # Trying to get the value of the box at the new position
            self.map[position.y][position.x]

            # It only gets here if all goes well
            # print 'Setting current position'
            self.cur_pos = position
        except (IndexError, AssertionError):
            # Ran into wall
            # print 'Error:', e
            # print 'Position:', position
            points = -self.point_system.wall_penalty
        return points

    def cur_pos_value(self):
        """
        Returns the current positions value
        """
        return self.map[self.cur_pos.y][self.cur_pos.x]

    def move_north(self):
        """
        Tries to move North in the environment.

        Returns the number of points given by the movement.
        """
        return self._move(move_y=subtract)

    def move_northwest(self):
        return self._move(move_x=subtract, move_y=subtract)

    def move_west(self):
        return self._move(move_x=subtract)

    def move_southwest(self):
        return self._move(move_x=subtract, move_y=add)

    def move_south(self):
        return self._move(move_y=add)

    def move_southeast(self):
        return self._move(move_x=add, move_y=add)

    def move_east(self):
        return self._move(move_x=add)

    def move_northeast(self):
        return self._move(move_x=add, move_y=subtract)

    def pick_up(self):
        """
        Tries to pick up a can in the current site
        """
        if self.cur_pos_value():
            points = self.point_system.can_reward
        else:
            points = -self.point_system.pickup_penalty
        return points

    def stay(self):
        """
        Stay in current position
        """
        return self.point_system.stay_put
