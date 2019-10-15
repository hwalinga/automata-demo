from typing import Iterator

import numpy as np
from matplotlib import animation
from matplotlib import pyplot as plt


def animate_automata(states: Iterator[np.array], steps: int, timestep: int):
    """Animates the states of the automata.
    states:
        Iterator of each new state (So this could be an infinite generator).
    steps:
        Size of the display (so display is length of numpy array times size).
    timestep:
        Time (in ms) between each step.

    NB. This function is blocking.
    """
    initial_state = next(states)
    state_length = initial_state.size
    size = steps, state_length
    x = np.zeros(size)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    img_data_handler = ax.imshow(x, vmin=0, vmax=1, cmap="Greys", interpolation="none")
    plt.tight_layout()

    def init():
        # Having an init function prevents animate(0) from being called unneeded.
        return [img_data_handler]

    def animate(i):
        new_state = next(states) if i != 0 else initial_state
        if i >= steps:
            nonlocal x  # Python's strange scoping rules.
            # shift data to update
            x = np.roll(x, -1, axis=0)
            x[-1] = new_state
        else:
            x[i] = new_state
        img_data_handler.set_array(x)
        return [img_data_handler]

    # Preventing animation object from being garbage collected.
    # https://github.com/matplotlib/matplotlib/issues/1656
    anim = animation.FuncAnimation(
        fig, animate, init_func=init, interval=timestep, blit=True
    )
    plt.show()  # This will block

    return anim


def self_biasing_random_states(size):
    # Initial state
    current_state = np.random.binomial(1, 0.5, size)
    yield current_state

    # Loop over new state and update p.
    while True:
        p = sum(current_state) / size
        p += (-1 if p > 0.5 else 1) * 0.01
        current_state = np.random.binomial(1, p, size)
        yield current_state


def cellular_automata(size, rule):
    pass


def main():
    states = self_biasing_random_states(100)
    animate_automata(states, steps=100, timestep=20)


if __name__ == "__main__":
    main()
