import numpy as np
from display import Display
from double_pendulum import DoublePendulum


class Simulation:
    def __init__(self, res, fps, time, dt, scale, speed, path_depth, ag, mass, length, theta, d_theta):
        self.running = False  # Simulation not started yet at this point

        # Setting simulation variables
        self.width, self.height = res
        self.fps = fps
        self.time, self.dt = time, dt
        self.points_count = self.time / self.dt
        self.scale = scale
        self.speed = speed
        self.path_depth = path_depth
        self.path = []

        # Setting variables for solve method.
        self.time_range = np.arange(0, self.time + self.dt, self.dt)  # Range of time points
        self.ag = ag  # Gravitational acceleration

        # Creating display and pendulum objects; Solving equations
        self.pendulum = DoublePendulum(mass, length, theta, d_theta)
        self.pendulum.solve(self.time_range, self.ag)
        self.display = Display(res)

    def run(self):
        """ Simulation loop. """

        # Start the simulation
        self.running = True

        i = 0  # Iterable for simulation frames
        di = int((1 / self.fps / self.dt) * self.speed)  # Step size based on time density and frame rate

        # Loop
        while self.running:
            # Getting start point and all of the pendulum positions
            x_start, y_start = (int(self.width / 2), int(self.height / 3))
            x_1_scaled, y_1_scaled, x_2_scaled, y_2_scaled = self.pendulum.get_scaled_positions(i, self.scale)
            start_pos = (x_start, y_start)
            x_1_pos = (x_start + x_1_scaled, y_start - y_1_scaled)
            x_2_pos = (x_start + x_2_scaled, y_start - y_2_scaled)

            # Getting raw positions and velocities to show live info
            x_1_raw, y_1_raw, x_2_raw, y_2_raw = self.pendulum.get_positions(i)
            angle_1, angle_2 = self.pendulum.get_angles(i)
            velocity_1, velocity_2 = self.pendulum.get_angular_velocities(i)

            # Setting strings ready to be drawn on display
            info_str = 'Mass {} X: {:05.2f}m, Y: {:05.2f}m, Angle: {:05.1f}deg, Velocity: {:06.1f}deg/s'
            m_1_info_str = info_str.format(1, x_1_raw, y_1_raw, angle_1 % 360, velocity_1)
            m_2_info_str = info_str.format(2, x_2_raw, y_2_raw, angle_2 % 360, velocity_2)

            # Drawing rods
            self.display.draw_rod(start_pos, x_1_pos)
            self.display.draw_rod(x_1_pos, x_2_pos)

            self.display.draw_path(self.path, self.path_depth)  # Drawing path

            # Drawing bodies
            self.display.draw_body(x_1_pos)
            self.display.draw_body(x_2_pos)

            # Drawing live info
            self.display.draw_info(m_1_info_str, (10, 10))
            self.display.draw_info(m_2_info_str, (10, 38))

            # Handling events and transition into next iteration
            self.display.next_frame(int(1000 / self.fps))
            self.display.handle_events()

            # Inserting current second pendulum position into path
            self.path.append(x_2_pos)

            # Iterating and stopping the simulation at the end of solved time range
            i += di
            if i > self.points_count:
                self.running = False
