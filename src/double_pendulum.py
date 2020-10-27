import numpy as np
from scipy.integrate import odeint


def deg_to_rad(theta_deg):
    """ Convert degrees to radians. """
    return theta_deg * 0.0174532925


def rad_to_deg(theta_rad):
    """ Convert radians to degrees. """
    return theta_rad * 57.2957795


class DoublePendulum:
    def __init__(self, mass, length, theta, d_theta):
        # Setting constants and initial variables
        self.mass_1, self.mass_2 = mass
        self.length_1, self.length_2 = length
        self.initial_theta_1_deg, self.initial_theta_2_deg = theta
        self.initial_d_theta_1_deg, self.initial_d_theta_2_deg = d_theta

        # Converting initial variables to radians for solving ODEs
        self.initial_theta_1 = deg_to_rad(self.initial_theta_1_deg)
        self.initial_theta_2 = deg_to_rad(self.initial_theta_2_deg)
        self.initial_d_theta_1 = deg_to_rad(self.initial_d_theta_1_deg)
        self.initial_d_theta_2 = deg_to_rad(self.initial_d_theta_2_deg)

        # Initializing result variables before solving ODEs
        self.theta_1, self.theta_2 = (None, None)
        self.d_theta_1, self.d_theta_2 = (None, None)
        self.x_1, self.y_1, self.x_2, self.y_2 = (None, None, None, None)

    def derive(self, y, _, ag, ag2):
        """ Differential equations used in the simulation.
        Source: https://www.math24.net/double-pendulum/"""

        theta_1, d_theta_1, theta_2, d_theta_2 = y
        sine, cosine = np.sin(theta_1 - theta_2), np.cos(theta_1 - theta_2)

        theta_1_dot, theta_2_dot = d_theta_1, d_theta_2

        d_theta_1_dot = ((self.mass_2 * ag * np.sin(theta_2) * cosine - self.mass_2 * sine *
                          (self.length_1 * d_theta_1 ** 2 * cosine + self.length_2 * d_theta_2 ** 2) -
                          (self.mass_1 + self.mass_2) * ag * np.sin(theta_1)) / self.length_1 /
                         (self.mass_1 + self.mass_2 * sine ** 2))

        d_theta_2_dot = (((self.mass_1 + self.mass_2) * (self.length_1 * d_theta_1 ** 2 * sine - ag * np.sin(theta_2) +
                         ag * np.sin(theta_1) * cosine) + self.mass_2 * self.length_2 * d_theta_2 ** 2 *
                         sine * cosine) / self.length_2 / (self.mass_1 + self.mass_2 * sine ** 2))

        return theta_1_dot, d_theta_1_dot, theta_2_dot, d_theta_2_dot

    def solve(self, time_range, ag):
        """ Solve ODEs in given time range, using given gravitational acceleration. """

        # Converting initial values to numpy array
        initial_conditions = np.array([self.initial_theta_1, self.initial_d_theta_1,
                                       self.initial_theta_2, self.initial_d_theta_2])

        # Solving ODEs
        result = odeint(self.derive, initial_conditions, time_range, args=(ag, ag))
        self.theta_1, self.d_theta_1 = result[:, 0], result[:, 1]
        self.theta_2, self.d_theta_2 = result[:, 2], result[:, 3]

        self.convert_to_cartesian()

    def convert_to_cartesian(self):
        """ Convert solution to cartesian units. """
        self.x_1 = self.length_1 * np.sin(self.theta_1)
        self.y_1 = -self.length_1 * np.cos(self.theta_1)
        self.x_2 = self.x_1 + self.length_2 * np.sin(self.theta_2)
        self.y_2 = self.y_1 - self.length_2 * np.cos(self.theta_2)

    def get_positions(self, i):
        """ Get raw cartesian positions. """
        return self.x_1[i], self.y_1[i], self.x_2[i], self.y_2[i]

    def get_scaled_positions(self, i, scale):
        """ Get scaled for display cartesian positions using given scale factor. """
        scaled_x_1 = self.x_1[i] * scale
        scaled_y_1 = self.y_1[i] * scale
        scaled_x_2 = self.x_2[i] * scale
        scaled_y_2 = self.y_2[i] * scale

        return scaled_x_1, scaled_y_1, scaled_x_2, scaled_y_2

    def get_angles(self, i):
        """ Get angles in degrees. """
        return rad_to_deg(self.theta_1[i]), rad_to_deg(self.theta_2[i])

    def get_angular_velocities(self, i):
        """ Get angular velocities in degrees per second. """
        return rad_to_deg(self.d_theta_1[i]), rad_to_deg(self.d_theta_2[i])
