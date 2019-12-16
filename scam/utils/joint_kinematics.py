from numpy import trapz


class TrajectoryGenerator:
    def __init__(self, theta_start, theta_end, num_cycles):
        self.theta_start = theta_start
        self.theta_end = theta_end
        self.num_cycles = num_cycles

    @staticmethod
    def get_concave_parabola(C, k, clock):
        """
        A downwards concave parabola of form:
            f(x) = -c(x)(x - a)
        Here:
            C     -> x
            k     -> c
            clock -> a
        """
        return -1 * k * C * (C - clock)

    def generate_parabolic_path(self):
        # get the area we wish to match
        area_linear = self.theta_end - self.theta_start

        # get the area of a parabola scaled to 1.00
        cycles = list(range(0, self.num_cycles + 1))
        d_theta_prescaled = [self.get_concave_parabola(c, k=1.0, clock=self.num_cycles) for c in cycles]
        area_prescaled = trapz(d_theta_prescaled)

        # get the new scaling constant
        new_constant = area_linear / area_prescaled

        # and now scale down parabola to match the area of the linear fit
        d_theta_normalized = [self.get_concave_parabola(c, k=new_constant, clock=self.num_cycles) for c in cycles]
        return d_theta_normalized

    def generate_linear_path(self):
        return (self.theta_end - self.theta_start) / self.num_cycles
