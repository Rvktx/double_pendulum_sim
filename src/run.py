#!/usr/bin/env python3
import argparse
from simulation import Simulation

if __name__ == '__main__':
    # Initializing args parser
    parser = argparse.ArgumentParser(description='Double pendulum simulator')

    # Adding arguments to parser
    parser.add_argument('--res', nargs=2, type=int, required=False, default=(800, 800),
                        help='Resolution of the simulation window. [px] Enter in format: --res x y')
    parser.add_argument('--fps', type=int, required=False, default=60,
                        help='Frame rate of the simulation. [fps]')
    parser.add_argument('--time', type=int, required=False, default=240,
                        help='Length of the simulation. [s]')
    parser.add_argument('--dt', type=float, required=False, default=0.01,
                        help='Length of the smallest step in simulation. [s]')
    parser.add_argument('--scale', type=int, required=False, default=150,
                        help='Scale of the simulation. Scale of 100 means that 1m is equal to 100px.')
    parser.add_argument('--speed', type=float, required=False, default=1,
                        help='Playback speed multiplier. High values may cause inaccuracy.')
    parser.add_argument('--path-depth', type=int, required=False, default=50,
                        help='Number of previous positions to track and show on path. 0 means infinite depth.')
    parser.add_argument('--ag', type=float, required=False, default=9.81,
                        help='Value of teh gravitational acceleration used in simulation. [m/s^2];')
    parser.add_argument('--mass', nargs=2, type=float, required=False, default=(1, 1),
                        help='Masses of bodies in pendulum. [kg] Enter in format: --mass M1 M2')
    parser.add_argument('--length', nargs=2, type=float, required=False, default=(1.1, 1),
                        help='Lengths of rods in pendulum. [m] Enter in format: --length L1 L2')
    parser.add_argument('--theta', nargs=2, type=float, required=False, default=(40, 160),
                        help='Initial angles of bodies in pendulum. [deg] Enter in format: --theta t1 t2')
    parser.add_argument('--dtheta', nargs=2, type=float, required=False, default=(0, 0),
                        help='Initial angular velocities of bodies in pendulum. [deg/s] '
                             'Enter in format: --dtheta dt1 dt2')

    # Parsing args and starting the simulation
    args = parser.parse_args()
    sim = Simulation(args.res, args.fps, args.time, args.dt, args.scale, args.speed, args.path_depth,
                     args.ag, args.mass, args.length, args.theta, args.dtheta)
    sim.run()
