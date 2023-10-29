import numpy as np


class HaloPoint:
    def __init__(self, ax, mass, color_decay, color1, color2='white'):
        self.halo_points_color1 = [ax.plot([], [], 'o', c=color1, markersize=0, alpha=0,
                                           markeredgecolor='none', zorder=3)[0] for _ in range(100)]
        self.halo_points_white = [ax.plot([], [], 'o', c=color2, markersize=0, alpha=0,
                                          markeredgecolor='none', zorder=4)[0] for _ in range(100)]
        self.mass = mass
        self.color_decay = color_decay
        
    def set_data(self, x, y):
        radius = np.linspace(2, 20, 100)
        for index, i in enumerate(radius):
            self.halo_points_color1[index].set_data([x], [y])
            self.halo_points_white[index].set_data([x], [y])
            
            self.halo_points_color1[index].set_markersize(self.mass*i)
            self.halo_points_color1[index].set_alpha(np.exp(-(i-2))**self.color_decay)
            
            self.halo_points_white[index].set_markersize(self.mass*i)
            self.halo_points_white[index].set_alpha(np.exp(-(i-2))**1)
        
    def get_artists(self):
        return self.halo_points_color1 + self.halo_points_white
