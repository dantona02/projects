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


class Trajectory:
    def __init__(self, ax, size_main, size_side, datarange, color_decay, color, edgecolor):
        self.trajectory_main = [ax.plot([], [], c=color, linewidth=size_main, alpha=0, zorder=4)[0] for _ in
                                range(datarange - 1, 0, -1)]
        self.trajectory_side = [ax.plot([], [], c=edgecolor, linewidth=size_side, alpha=0, zorder=3)[0] for _ in
                                range(datarange - 1, 0, -1)]
        self.trajectory_top = [ax.plot([], [], c='white', linewidth=size_side, alpha=0, zorder=5)[0] for _ in
                               range(datarange - 1, 0, -1)]
        self.color_decay = color_decay
        self.datarange = datarange

    def set_data(self, x, y, frame):
        if len(x) != len(y):
            raise ValueError("x and y must have the same number of elements")
        # for traj in self.trajectory_main + self.trajectory_side:
        #     traj.set_data([], [])
        start_index = max(0, frame - self.datarange)
        subset_x = x[start_index:frame + 1]
        subset_y = y[start_index:frame + 1]

        num_segments = min(len(self.trajectory_main), len(subset_x) - 1)  # segments available

        for s in range(num_segments):
            segment_start = s  # start point of segment
            segment_end = s + 1  # end point of segment
            traj_index = num_segments - 1 - s  # position in list of trajectories in reversed order
            fraction = 1 - (s / num_segments)
            alpha = np.exp(-self.color_decay * fraction) * (1 - fraction)

            self.trajectory_main[traj_index].set_data(subset_x[segment_start:segment_end + 1],
                                                      subset_y[segment_start:segment_end + 1])
            self.trajectory_side[traj_index].set_data(subset_x[segment_start:segment_end + 1],
                                                      subset_y[segment_start:segment_end + 1])
            self.trajectory_top[traj_index].set_data(subset_x[segment_start:segment_end + 1],
                                                     subset_y[segment_start:segment_end + 1])
            self.trajectory_main[traj_index].set_alpha(alpha)
            self.trajectory_side[traj_index].set_alpha(alpha * 0.2)
            self.trajectory_top[traj_index].set_alpha(np.exp(-15 * fraction) * (1 - fraction))

    def get_artists(self):
        return self.trajectory_main + self.trajectory_side + self.trajectory_top
