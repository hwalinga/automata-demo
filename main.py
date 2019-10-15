from typing import Iterator

import numpy as np

import matploblib.animation as animation
import matploblib.pyplot as plt


def animate_automata(states: Iterator[np.array], steps: int, timestep: int):
    """Animates the states of the automata.
    states:
        Iterator of each new state (So this could be an infinate generator).
    steps:
        Size of the display (so display is length of numpy array times size).
    timestep:
        Time (in ms) between each step.

    NB. This function is blocking.
    """
    l = next(states)

    fig = 42

    def init():
        pass

    def animate(i):
        pass

    _ = animation.FuncAnimation(
        fig, animate, init_func=init, frames=200, interval=timestep, blit=True
    )
    plt.show()


def random_states():
    pass


def cellular_automata(rule):
    pass


def main():
    states = random_states()
    animate_automata(states, steps=200, timestep=500)


if __name__ == "__main__":
    main()
