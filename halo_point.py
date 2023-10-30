import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap
import sys
from matplotlib.animation import FFMpegWriter


class HaloPoint:
    def __init__(self, ax, mass, color_decay, color1, color2='white'):
        self.halo_points_color1 = [ax.plot([], [], 'o', c=color1, markersize=0, alpha=0,
                                           markeredgecolor='none', zorder=6)[0] for _ in range(100)]
        self.halo_points_white = [ax.plot([], [], 'o', c=color2, markersize=0, alpha=0,
                                          markeredgecolor='none', zorder=7)[0] for _ in range(100)]
        self.mass = mass
        self.color_decay = color_decay

    def set_data(self, x, y):
        radius = np.linspace(2, 20, 100)
        for index, i in enumerate(radius):
            self.halo_points_color1[index].set_data([x], [y])
            self.halo_points_white[index].set_data([x], [y])

            self.halo_points_color1[index].set_markersize(self.mass * i)
            self.halo_points_color1[index].set_alpha(np.exp(-(i - 2)) ** self.color_decay)

            self.halo_points_white[index].set_markersize(self.mass * i)
            self.halo_points_white[index].set_alpha(np.exp(-(i - 2)) ** 1)

    def get_artists(self):
        return self.halo_points_color1 + self.halo_points_white


class Trajectory:
    def __init__(self, ax, size_main, size_side, datarange, color_decay, decay_white, color, edgecolor):
        self.trajectory_main = [ax.plot([], [], c=color, linewidth=size_main, alpha=0, zorder=4)[0] for _ in
                                range(datarange - 1, 0, -1)]
        self.trajectory_side = [ax.plot([], [], c=edgecolor, linewidth=size_side, alpha=0, zorder=3)[0] for _ in
                                range(datarange - 1, 0, -1)]
        self.trajectory_top = [ax.plot([], [], c='white', linewidth=size_side, alpha=0, zorder=5)[0] for _ in
                               range(datarange - 1, 0, -1)]
        self.color_decay = color_decay
        self.decay_white = decay_white
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
            self.trajectory_top[traj_index].set_alpha(np.exp(-self.decay_white * fraction) * (1 - fraction))

    def get_artists(self):
        return self.trajectory_main + self.trajectory_side + self.trajectory_top


class TrajectoryOpt:
    def __init__(self, ax, size_main, size_side, datarange, color1, color2):
        self.datarange = datarange
        self.colors = ['black', color1, color2, 'white']
        custom_cmap = LinearSegmentedColormap.from_list("custom", self.colors, N=256)

        self.line1 = LineCollection([], cmap=custom_cmap, linewidths=size_main, zorder=3)
        self.line2 = LineCollection([], cmap=custom_cmap, linewidths=size_side, zorder=2, alpha=.4)
        self.line3 = LineCollection([], cmap=custom_cmap, linewidths=size_side + .5, zorder=1, alpha=.2)
        ax.add_collection(self.line1)
        ax.add_collection(self.line2)
        ax.add_collection(self.line3)

    def set_data(self, x, y, frame):
        start = max(0, frame - self.datarange)
        end = frame
        xs = x[start:end]
        ys = y[start:end]

        points = np.array([xs, ys]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-2], points[1:-1], points[2:]], axis=1)
        self.line1.set_segments(segments)
        self.line2.set_segments(segments)
        self.line3.set_segments(segments)

        indices = np.linspace(start, end - 1, len(xs))  # color coding based on index
        self.line1.set_array(indices)
        self.line2.set_array(indices)
        self.line3.set_array(indices)

        self.line1.set_clim(start, end)  # setting boundaries for color based on index
        self.line2.set_clim(start, end)
        self.line3.set_clim(start, end)

    def get_artists(self):
        return [self.line1, self.line2, self.line3]


class ProgressWriter(FFMpegWriter):
    def __init__(self, total_frames, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.total_frames = total_frames
        self.frame_count = 0

    def grab_frame(self, **savefig_kwargs):
        super().grab_frame(**savefig_kwargs)
        self.frame_count += 1
        sys.stdout.write(f"\rExporting: {self.frame_count}/{self.total_frames} frames")
        sys.stdout.flush()
