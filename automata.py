import sys

import matplotlib
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use("TkAgg")


# define rule creator
# Interesting ones: 30, 90, 110, 184
def get_rule(rule_num: int) -> dict:
    scaffold = ["111", "110", "101", "100", "011", "010", "001", "000"]
    binary = format(rule_num, '08b')
    return dict(zip(scaffold, binary))


class Automata:

    #
    def __init__(self, rule: dict, steps: int, size: int, timestep: int):
        """constructor for the Automata class.
        rule:
            Rule that this CA will simulate
        steps:
            Amount of consequent steps displayed on the display (height of display).
        size:
            Width of display
        timestep:
            Time (in ms) between each step.
        """

        # set object parameters
        self.rule = rule
        self.steps = steps
        self.size = size
        self.timestep = timestep

        # initialize current state
        self.current_state = np.zeros(size, dtype=int)
        # self.current_state[int(np.round(self.size / 2))] = int(1)
        self.current_state = np.random.binomial(1, 0.5, self.size)

        # initialize data and image frame
        self.x = np.zeros((self.steps, self.size))
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.get_xaxis().set_visible(False)
        self.ax.get_yaxis().set_visible(False)
        plt.tight_layout()

        self.image = self.ax.imshow(
            self.x, vmin=0, vmax=1, cmap="Greys", interpolation="none"
        )

    def get_self_biasing_random(self):
        """
        Method to get random next state based on previous states.
        :return: new random state (self.current_state also updated).
        """
        p = sum(self.current_state) / self.size
        p += (-1 if p > 0.5 else 1) * 0.01
        self.current_state = np.random.binomial(1, p, self.size)
        return self.current_state

    def _rule_update(self):
        """
        Method to apply the defined rule to compute the new state.
        :return: new state after rule has been applied.
        """

        # Apply rolling window over state (size 3, because only rule 0-255 are implemented currently)
        windows = self._window(3)

        # compute update for every cell in state and concat to string
        new_state = ",".join(
            self.rule[np.array2string(pat, separator="")[1:-1]] for pat in windows
        )

        # create numpy array from string resulting in new state
        self.current_state = np.fromstring(new_state, sep=",", dtype=int)

    def _window(self, stride=3):
        """
        Method to compute all subarrays of state using rolling window.
        :param stride: size of rolling window.
        :return: Iterator containing all subarrays of the current state (uses padding to incorporate edges).
        """

        # create padded 1D array
        padded = np.zeros(self.current_state.size + 2, dtype=int)
        padded[1:-1] = self.current_state

        # use rolling window to generate all subarrays.
        for index in range(len(padded) - stride + 1):
            yield padded[index : index + stride]

    def animate(self, frames=None):
        """
        Method to create animation of the CA.
        :return: animation object containing the animation of the set rule.
        """

        anim = animation.FuncAnimation(
            self.fig,
            self._animate,
            init_func=self._init_animator,
            interval=self.timestep,
            blit=True,
            frames=frames,
            repeat=False,
        )
        return anim

    def _init_animator(self):
        """
        Method to initialize the first data of the animation object.
        :return: Iterable containing initial data.
        """
        # self.image.set_data(self.x)
        return [self.image]

    def _animate(self, i):
        """
        Method to update the animation object's data.
        :param i: current timestep.
        :return: Iterable containing updated data for the animation object.
        """

        # update state
        self._rule_update()

        # if amount of current rows larger than window height
        if i >= self.steps:
            # shift data upwards and insert new state into last row
            self.x = np.roll(self.x, -1, axis=0)
            self.x[-1] = self.current_state
        else:
            # insert data into correct row
            self.x[i, :] = self.current_state

        # update the data container
        self.image.set_array(self.x)
        return [self.image]


if __name__ == "__main__":
    """
    Main method used to simulate the CAs
    """

    # create automata with certain rule, window height and width and update speed
    rule = get_rule(int(sys.argv[1]) if len(sys.argv) > 1 else 110)
    automaat = Automata(rule, 512, 512, 1)

    # simulate rule, specify frames to set video record duration (duration is frames/fps seconds)
    # use None for continuous animation (video stops after certain amount of frames by default)
    anim = automaat.animate(frames=None)

    # functions used to save simulation to video
    # file_location = "demo_videos/animation.mp4"
    #
    # Writer = animation.writers['ffmpeg']
    # writer = Writer(fps=20, metadata=dict(artist='Tim & Hielke'), bitrate=1800)
    #
    # anim.save(file_location, writer)
    plt.show()
