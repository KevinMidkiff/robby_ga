class PointSystem(object):
    """
    Point System Class
    """
    def __init__(self, can_reward, pickup_penalty, wall_penalty, stay_put):
        """
        PointSystem constructor

        Arguments:
            can_reward     - Amount of points to award for picking up a can
            pickup_penalty - Amount of points to deduct for trying to pick up
                             a can on an empty site
            wall_penalty   - Amount of points to deduct for running into a wall
            stay_put       - Amount of points to award for staying put
        """
        self.can_reward = can_reward
        self.pickup_penalty = pickup_penalty
        self.wall_penalty = wall_penalty
        self.stay_put = stay_put
