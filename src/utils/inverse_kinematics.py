from math import atan2, degrees as deg

class NoSolutionError(Exception):
    """ Return this error if no solution exists to some set of x, y inputs """
    pass

class InverseKinematics:
    """
    Inverse kinematics for 2R portion of a manipulator has both a
    positive and negative solution.

    Input:
        X            -> the solution x coordinate (float)
        Y            -> the solution y coordinate (float)
        L1           -> the length of the first link (float)
        L2           -> the length of the second link (float)
        pos_solution -> this boolean returns the "right" or "left" solution
    Output:
        THETA_1_POS  -> theta_1 angle for "right" solution
        THETA_2_POS  -> theta_2 angle for "right" solution
        ||
        THETA_1_NEG  -> theta_1 angle for "left" solution
        THETA_2_NEG  -> theta_2 angle for "left" solution
    """
    def __init__(self, x_coord, y_coord, link_1_length, link_2_length):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.link_1_length = link_1_length
        self.link_2_length = link_2_length

    def solution_exists(self):
        if (self.x_coord ** 2 + self.y_coord ** 2) ** 0.5 > self.link_1_length + self.link_2_length:
            return False
        elif (self.x_coord ** 2 + self.y_coord ** 2) ** 0.5 < self.link_1_length - self.link_2_length:
            return False
        else:
            return True

    def get_positive_solution(self):
        if self.solution_exists():
            c2_n = self.x_coord ** 2 + self.y_coord ** 2 - self.link_1_length ** 2 - self.link_2_length ** 2
            c2_d = 2 * self.link_1_length * self.link_2_length
            c2 = c2_n / c2_d
            k1 = self.link_1_length + self.link_2_length * c2
            s2_positive = (1 - c2 ** 2) ** 0.5
            theta_2_positive = deg(atan2(s2_positive, c2))
            k2_positive = self.link_2_length * s2_positive
            theta_1_positive = deg(atan2(self.y_coord, self.x_coord) - atan2(k2_positive, k1))
            return theta_1_positive, theta_2_positive
        else:
            return NoSolutionError

    def get_negative_solution(self):
        if self.solution_exists():
            c2_n = self.x_coord ** 2 + self.y_coord ** 2 - self.link_1_length ** 2 - self.link_2_length ** 2
            c2_d = 2 * self.link_1_length * self.link_2_length
            c2 = c2_n / c2_d
            k1 = self.link_1_length + self.link_2_length * c2
            s2_negative = -(1 - c2 ** 2) ** 0.5
            theta_2_negative = deg(atan2(s2_negative, c2))
            k2_negative = self.link_2_length * s2_negative
            theta_1_negative = deg(atan2(self.y_coord, self.x_coord) - atan2(k2_negative, k1))
            return theta_1_negative, theta_2_negative
        else:
            return NoSolutionError
