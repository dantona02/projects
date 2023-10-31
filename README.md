# Simulation of the planar three-body problem
This project simulates and visualizes the trajectories of the planar three-body problem. The [threebproblem.ipynp](https://github.com/dantona02/projects/blob/main/threebproblem.ipynb) notebook provides links to the corresponding papers on which the simulation is based.
All the underlying basic physical and mathematical concepts of the simulation can also be found in this notebook.

## Setup of the notebook
The main purpose of this project is to simulate special cases of the three-body problem with **zero angular momentum**. The papers introduce very specific initial conditions, even though a few parameters can be changed. Those are $m_3$, $v_1$ and $v_2$. All the other parameters are set according to the initial conditions.

The four video files provided in this repository show the simulation of three bodies with equal mass, i.e. $m_1=m_2=m_3$ of the sun $m_{\text{sun}}=1.98892\cdot10^{30}\ \text{kg}$ and an initial distance of one astronomical unit 
($L=1.495978707\cdot10^{11}\ \text{m}$) to each other, but different $v_1$ and $v_2$.
One can change the parameters a little and try to find other stable periodic orbits.

## Module `animation`
There are a few custom classes implemented in the code that need a little bit of explanation. The module [animation](https://github.com/dantona02/projects/blob/main/animation.py) has the following classes:
- ### class `HaloPoint`
  An object of the class `HaloPoint` can be created like the following:
  ```python
  halopoint = HaloPoint(ax, mass, color_decay, color1, color2='white')
  ```
  - `ax` corresponds to the current instance of `Axes` of the animation.
  - `mass` is a parameter to change the size of `halopoint` according to the mass, even if that doesn't reflect the physical reality.
  - `color_decay` changes the decay of the halo. The larger the value of `color_decay`, the smaller the halo.
  - `color1` sets the color of the point.
  - `color2` should generally not be changed.
    
  **It is very important to note that the `get_artists()` method returns a list of `Artists`, which must then be merged into one list to be returned by the update-function.
    This applies to all other animation classes contained in this module.**
    Here's an example how multiple artists can be implemented in the update-function:
    ```python
    artists = (point1.get_artists() +
               point2.get_artists() +
               point3.get_artists())
    return artists
    ```
- ### class `TrajectoryOpt`
  This is the recommended class for animating the trajectories of the three bodies, as this class is much more computationally efficient than `Trajectory` due to its core, which is based on matplotlib's `LineCollection`.
  An object of the class `TrajectoryOpt` can be created like the following:
  ```python
  trajectoryOpt = TrajectoryOpt(ax, size_main, size_side, datarange, color1, color2)
  ```
  - `ax` corresponds to the current instance of `Axes` of the animation.
  - `size_main` sets the width of the main trajectory.
  - `size_side` is intended to be slightly larger than `size_main` to achieve some sort of 'fade-out' effect to the sides.
  - `datarange` changes the effective length of the trajectory. It should always be set relative to the total datapoints but should not be too large.
  - `color1` sets the color towards the end of the trajectory. It is preferably set to a darker tone to achieve a smooth fade out.
  - `color2` sets the color towards the beginning of the trajectory. It should be the same color like the parameter `color1` of the instance of `HaloPoint`.
- ### class `Trajectory`
  The core of this class is based on iterative visualization and is less efficient. Creating an object works like the following:
  ```python
  trajectory = Trajectory(ax, size_main, size_side, datarange, color_decay, decay_white, color, edgecolor)
  ```
  - `ax`, `size_main`, `size_side` and `datarange` work like the parameters of `TrajectoryOpt`.
  - `color_decay` changes the transparency towards the end of the trajectory.
  - `decay_white` changes the transparency of the white part at the beginning of the trajectory.
  - `color` sets the color of main trajectory. It should equal the color of the halopoint.
  - `edgecolor` sets the color towards the side of the trajectory.
- ### class `ProgressWriter`
  This class uses an instance of `FFMpegWriter` and shows the progress of the saving process. An instance of `ProgressWriter` can be created analogously to one of `FFMpegWriter`.
- ### class `ProgressPillowWriter`
  This class uses an instance of `PillowWriter` and shows the progress of the saving process. An instance of `ProgressPillowWriter` can be created analogously to one of `PillowWriter`.

## Required packages
`matplotlib`, `numpy`, and `scipy`. The plots and animations in this notebook are processed by the backend-renderer `QT5Agg`, as this ensures a much more convenient option to show plots and animations.
