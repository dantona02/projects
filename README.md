# Simulation of a planar three-body problem
This project simulates and visualizes the trajectories of the planar three-body-problem. The links to the corresponding papers the simualtion is based on, are provided in the [threebproblem.ipynp](https://github.com/dantona02/projects/blob/main/threebproblem.ipynb) notebook.
All the underlying basic physical and mathematical concepts of the simualatio and the n can also be found in this notebook.

## Setup of the notebook
The main purspose of this project is, to simualte a special cases of the three-body-problem with **zero angular momentum**. The papers introduces very specific inital conditions, even though a few parameters can be changed. Those are $m_3$, $v_1$ and $v_2$. All the other paramters are set according to the inital conditions.

The four video files provided in this repsoitory show the simulation of three bodies with equal mass, i.e. $m_1=m_2=m_3=$, of the sun $m_{\text{sun}}=1.98892\cdot10^{30}\text{kg}$ and an initial distance of one astronomical unit ($L=1.495978707\cdot10^{11}\text{m}$) to each other, but different $v_1$ and $v_2$.
One can change the parameters a little and try to find other stable periodic orbits.

## Module `animation`
There are a few custom classes implemented in the code that need a little bit of explanation. The module has the following classes:
- ### class `HaloPoint`
  An object of the class `HaloPoint` can be created like the following:
  ```python
  halopoint = HaloPoint(ax, mass, color_decay, color1, color2='white')
  ```
  - `ax` corresponds to the current instance of `Axes` of the animation.
  - `mass` is a parameter to change the the size of `halopoint` according to the mass, even if that doesn't reflect the physical reality.
  - `color_decay` changes the decay of the halo. The larger the value of `color_decay`, the smaller the halo.
  - `color1` sets the color of the point.
  - `color2` should generally not be changed.
  **It is very importand to note, that the `get_artists()` method returns a list of `Artists`, which must then be merged into one list to be returned by the update-function.
    This applies to all other animation classes contained in this module.**
    Here's an example how multiple artists can be implemented in the update-function:
    ```python
    artists = (point1.get_artists() +
               point2.get_artists() +
               point3.get_artists())
    return artists
    ```
- ### class `TrajectoryOpt`
  This is the recommended class for animating the trajectories of the three bodies, as this class is much more computational efficient than `Trajectory` due to its core, which is based on matplotlibs `LineCollection`.
  An object of the class `TrajectoryOpt` can be created like the following:
  trajectoryOpt = TrajectoryOpt(ax, mass, color_decay, color1, color2='white')



  
