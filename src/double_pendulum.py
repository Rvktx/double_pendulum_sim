import argparse
import pygame
import numpy as np
from scipy.integrate import odeint


def handle_args(parser):
    parser.add_argument('--res', nargs=2, type=tuple, required=False, default=(1280, 720),
                        help='Resolution of the simulation window. [px]; Enter in format: --res x y')
    parser.add_argument('--fps', type=int, required=False, default=60,
                        help='Framerate of the simulation. [fps]')
    parser.add_argument('--time', type=int, required=False, default=240,
                        help='Length of the simulation. [s]')
    parser.add_argument('--scale', type=int, required=False, default=120,
                        help='Scale of the simulation; Scale of 100 means that 1m is equal to 100px.')
    parser.add_argument('--speed', type=float, required=False, default=1,
                        help='Playback speed multiplier')
    parser.add_argument('--path-depth', type=int, required=False, default=50,
                        help='Number of previous positions to track and show on path.')
    parser.add_argument('--dt', type=float, required=False, default=0.01,
                        help='Length of the smallest step in simulation. [s]')
    parser.add_argument('--ag', type=float, required=False, default=9.81,
                        help='Value of teh gravitational acceleration used in simulation. [m/s^2];')
    parser.add_argument('--mass', nargs=2, type=tuple, required=False, default=(1, 1),
                        help='Masses of bodies in pendulum. [kg]; Enter in format: --mass M1 M2')
    parser.add_argument('--length', nargs=2, type=tuple, required=False, default=(1.1, 1),
                        help='Length of rods in pendulum. [m]; Enter in format: --length L1 L2')
    parser.add_argument('--theta', nargs=2, type=tuple, required=False, default=(100, 60),
                        help='Initial angles of bodies in pendulum. [deg]; Enter in format: --theta t1 t2')
    parser.add_argument('--dtheta', nargs=2, type=tuple, required=False, default=(0, 0),
                        help='Initial velocities of bodies in pendulum. [???]; Enter in format: --dtheta dt1 dt2')

    return parser.parse_args()


def deg_to_rad(theta_1_deg, theta_2_deg):
    theta_1_rad = theta_1_deg * 0.0174532925
    theta_2_rad = theta_2_deg * 0.0174532925

    return theta_1_rad, theta_2_rad


def derive(y, _, m_1, m_2, l_1, l_2, ag):
    # THIS https://www.math24.net/double-pendulum/
    theta_1, d_theta_1, theta_2, d_theta_2 = y
    sine, cosine = np.sin(theta_1 - theta_2), np.cos(theta_1 - theta_2)

    theta_1_dot, theta_2_dot = d_theta_1, d_theta_2

    d_theta_1_dot = ((m_2 * ag * np.sin(theta_2) * cosine - m_2 * sine *
                      (l_1 * d_theta_1 ** 2 * cosine + l_2 * d_theta_2 ** 2) -
                      (m_1 + m_2) * ag * np.sin(theta_1)) / l_1 / (m_1 + m_2 * sine ** 2))

    d_theta_2_dot = (((m_1 + m_2) * (l_1 * d_theta_1 ** 2 * sine - ag * np.sin(theta_2) +
                                     ag * np.sin(theta_1) * cosine) + m_2 * l_2 * d_theta_2 ** 2 * sine * cosine) /
                     l_2 / (m_1 + m_2 * sine ** 2))

    return theta_1_dot, d_theta_1_dot, theta_2_dot, d_theta_2_dot


class DoublePendulumSimulator:
    COLORS = {
        'BLACK': (0, 0, 0),
        'RED': (255, 0, 0),
        'WHITE': (255, 255, 255)
    }

    def __init__(self, args):
        self.running = False
        self.window = None
        self.theta_1, self.d_theta_1 = (None, None)
        self.theta_2, self.d_theta_2 = (None, None)
        self.x_1, self.y_1, self.x_2, self.y_2 = (None, None, None, None)

        self.width, self.height = args.res
        self.fps = args.fps

        self.time, self.dt = args.time, args.dt
        self.points_count = self.time / self.dt
        self.scale = args.scale
        self.speed_multiplier = args.speed
        self.path_depth = args.path_depth
        self.path = []

        self.ag = args.ag
        self.mass_1, self.mass_2 = args.mass
        self.length_1, self.length_2 = args.length

        self.initial_theta_1, self.initial_theta_2 = deg_to_rad(*args.theta)
        self.initial_d_theta_1, self.initial_d_theta_2 = args.dtheta

        self.time_range = np.arange(0, self.time + self.dt, self.dt)
        self.initial_conditions = np.array([self.initial_theta_1, self.initial_d_theta_1,
                                            self.initial_theta_2, self.initial_d_theta_2])

        self.solve()
        self.get_cartesian()
        self.init_window()

    def init_window(self):
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Double pendulum simulation')
        pygame.display.flip()

    def solve(self):
        result = odeint(derive, self.initial_conditions, self.time_range, args=(self.mass_1, self.mass_2,
                                                                                self.length_1, self.length_2, self.ag))
        self.theta_1 = result[:, 0]
        self.d_theta_1 = result[:, 1]
        self.theta_2 = result[:, 2]
        self.d_theta_2 = result[:, 3]

    def get_cartesian(self):
        self.x_1 = self.length_1 * np.sin(self.theta_1) * self.scale
        self.y_1 = -self.length_1 * np.cos(self.theta_1) * self.scale
        self.x_2 = self.x_1 + self.length_2 * np.sin(self.theta_2) * self.scale
        self.y_2 = self.y_1 - self.length_2 * np.cos(self.theta_2) * self.scale

    def draw_frame(self, i):
        start_pos = (int(self.width / 2), int(self.height / 4))
        m_1_pos = (int(self.width / 2 + self.x_1[i]), int(self.height / 4 - self.y_1[i]))
        m_2_pos = (int(self.width / 2 + self.x_2[i]), int(self.height / 4 - self.y_2[i]))

        self.window.fill(self.COLORS['BLACK'])

        for point_pos in self.path:
            pygame.draw.circle(self.window, self.COLORS['RED'], point_pos, 2)

        pygame.draw.line(self.window, self.COLORS['WHITE'], start_pos, m_1_pos, 3)
        pygame.draw.line(self.window, self.COLORS['WHITE'], m_1_pos, m_2_pos, 3)

        pygame.draw.circle(self.window, self.COLORS['WHITE'], m_1_pos, 20)
        pygame.draw.circle(self.window, self.COLORS['WHITE'], m_2_pos, 20)

        pygame.display.update()
        pygame.time.wait(int(1000 / self.fps))

        self.path.append(m_2_pos)

    def run(self):
        self.running = True
        i = 0
        di = int((1 / self.fps / self.dt) * self.speed_multiplier)

        while self.running:
            self.draw_frame(i)
            i += di

            if len(self.path) > self.path_depth != 0:
                self.path.pop(0)

            if i > self.points_count:
                self.running = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Double pendulum simulator')
    args = handle_args(parser)

    simulation = DoublePendulumSimulator(args)
    simulation.run()
