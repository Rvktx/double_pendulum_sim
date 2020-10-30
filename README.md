# double_pendulum_sim
 Double pendulum simulation animated with pygame.

### Prerequisites
I have written this in Python 3.8 so it would be ideal to use this version.
To install dependencies in your environment run:

```bash
$ pip3 install -r requirements.txt
```

## How to run
You can run default case with:

```bash
$ cd src
$ python run.py
```

## Usage

    usage: run.py [-h] [--res RES RES] [--fps FPS] [--time TIME] [--dt DT] [--scale SCALE] [--speed SPEED] [--path-depth PATH_DEPTH]
              [--ag AG] [--mass MASS MASS] [--length LENGTH LENGTH] [--theta THETA THETA] [--dtheta DTHETA DTHETA]

    Double pendulum simulator

    optional arguments:
      -h, --help            show this help message and exit
      --res RES RES         Resolution of the simulation window. [px] Enter in format: --res x y
      --fps FPS             Frame rate of the simulation. [fps]
      --time TIME           Length of the simulation. [s]
      --dt DT               Length of the smallest step in simulation. [s]
      --scale SCALE         Scale of the simulation. Scale of 100 means that 1m is equal to 100px.
      --speed SPEED         Playback speed multiplier. High values may cause inaccuracy.
      --path-depth PATH_DEPTH
                            Number of previous positions to track and show on path. 0 means infinite depth.
      --ag AG               Value of teh gravitational acceleration used in simulation. [m/s^2];
      --mass MASS MASS      Masses of bodies in pendulum. [kg] Enter in format: --mass M1 M2
      --length LENGTH LENGTH
                            Lengths of rods in pendulum. [m] Enter in format: --length L1 L2
      --theta THETA THETA   Initial angles of bodies in pendulum. [deg] Enter in format: --theta t1 t2
      --dtheta DTHETA DTHETA
                            Initial angular velocities of bodies in pendulum. [deg/s] Enter in format: --dtheta dt1 dt2
## Author

Mikołaj Knysak

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details