import sys
import matplotlib
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np


# matplotlib.use("TkAgg")


# define rule creator
# Interesting ones: 30, 90, 110, 184
def get_rule(rule_num: int) -> dict:
    binary = format(rule_num, "08b")
    binary_ints = [int(x) for x in binary]
    return dict(zip(range(7, -1, -1), binary_ints))


class Automata:

    #
    def __init__(self, rule: dict, steps: int, size: int, timestep: int, ax: matplotlib.axes.SubplotBase):
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

        self.ax = ax
        self.ax.get_xaxis().set_visible(False)
        self.ax.get_yaxis().set_visible(False)

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
        new_state = np.zeros_like(self.current_state)
        i = 0
        for rule_index in windows:
            new_state[i] = self.rule[rule_index]
            i = i + 1

        # create numpy array from string resulting in new state
        self.current_state = new_state

    def _bool_to_int(self, window):
        y = 0
        for i, j in enumerate(window):
            y += j << i
        return y

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
            yield self._bool_to_int(padded[index: index + stride])

    def animate(self, fig, frames=None):
        """
        Method to create animation of the CA.
        :return: animation object containing the animation of the set rule.
        """

        anim = animation.FuncAnimation(
            fig,
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
    width = int(sys.argv[2]) if len(sys.argv) > 2 else 512
    height = int(sys.argv[3]) if len(sys.argv) > 3 else 512

    rows = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    cols = int(sys.argv[5]) if len(sys.argv) > 5 else 1

    update_rate = int(sys.argv[6]) if len(sys.argv) > 6 else 50

    fig, axs = plt.subplots(rows, cols)
    plt.tight_layout()

    if rows * cols > 1:

        # for each example, create automata with different starting condition
        for axis in axs.flatten():
            automaat = Automata(rule, height, width, update_rate, axis)

            # simulate rule, specify frames to set video record duration (duration is frames/fps seconds)
            # use None for continuous animation (video stops after certain amount of frames by default)
            anim = automaat.animate(fig, frames=None)

            # functions used to save simulation to video
            # file_location = "demo_videos/animation.mp4"
            #
            # Writer = animation.writers['ffmpeg']
            # writer = Writer(fps=20, metadata=dict(artist='Tim & Hielke'), bitrate=1800)
            #
            # anim.save(file_location, writer)

    else:
        automaat = Automata(rule, height, width, update_rate, axs)
        anim = automaat.animate(fig, frames=None)
    plt.show()

    # class 1: code 136
    # class 2: code 73
    # class 3: code 18
    # class 4: code 110
