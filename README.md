# Simulation of a planar three-body problem
This project simulates and visualizes the trajectories of the planar three-body-problem. The links to the corresponding papers the simualtion is based on, are provided in the [threebproblem.ipynp](https://github.com/dantona02/projects/blob/main/threebproblem.ipynb) notebook.
All the underlying basic physical and mathematical concepts of the simualatio and the n can also be found in this notebook.

## Setup of the notebook
The main purspose of this project is, to simualte a special cases of the three-body-problem with **zero angular momentum**. The papers introduces very specific inital conditions, even though a few parameters can be changed. Those are $m_3$, $v_1$ and $v_2$. All the other paramters are set according to the inital conditions.

The four video files provided in this repsoitory show the simulation of three bodies with equal mass, i.e. $m_1=m_2=m_3=$, of the sun $m_{sun}=1.98892\cdot10^{30}\text{kg}$ and an initial distance of one astronomical unit ($L=1.495978707\cdot10^{11}\text{m}$) to each other, but different $v_1$ and $v_2$.
One can change the parameters a little and try to find other stable periodic orbits.

## Module `animation`
There are a few custom classes implemented in the code that need a little bit of explanation. The module has the following classes:
- class `HaloPoint`
  An object of the class `HaloPoint` can be created like the following:
  ```python
  halopoint = HaloPoint(ax, mass, color_decay, color1, color2='white')
  ```
  - `ax` 
