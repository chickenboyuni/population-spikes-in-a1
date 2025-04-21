import numpy as np


def shift_array(arr, shift):
    # This is to help apply a shift to the array
    # So if I have an array like [1 2 3 4]
    # A shift by 1 would give [0 1 2 3]
    # A shift by -1 would give [2 3 4 0]
    # A shift by 2 would give [0 0 1 2]
    # A shift by -2 would give [3 4 0 0]
    rolled = np.roll(arr, shift, axis=0)
    if shift > 0:
        rolled[:shift] = 0
    elif shift < 0:
        rolled[shift:] = 0
    return rolled


def relu(x):
    return np.maximum(x, 0)


def set_complex_sound_stimuli_C(model):
    model.add_stimulus(2, 5, 1.2, 1.3)
    model.add_stimulus(3, 6, 0.5, 0.8)
    model.add_stimulus(4, 7, 1.3, 1.57)
    model.add_stimulus(4, 6, 1.89, 2.08)
    model.add_stimulus(6, 5, 1.5, 1.76)
    model.add_stimulus(8, 4, 0.28, 0.48)
    model.add_stimulus(8, 3, 1.65, 1.78)
    model.add_stimulus(8, 8, 2.12, 2.38)
    model.add_stimulus(10, 5, 0.85, 0.98)
    model.add_stimulus(12, 4, 0.12, 0.26)
    model.add_stimulus(14, 7, 1.08, 1.32)
    model.add_stimulus(14, 7, 2.38, 2.5)


def set_white_noise(model, sim_end, min_amp, max_amp, max_stim_per_col):
    num_stimuli = np.random.randint(0, max_stim_per_col)
    for column in range(15):
        for _ in range(num_stimuli):
            amplitude = np.random.uniform(min_amp, max_amp)
            begin = np.random.uniform(0, sim_end)
            end = np.random.uniform(begin, sim_end)
            model.add_stimulus(column, amplitude, begin, end)

def set_locking_stimuli(model, column, A, isi, stimulus_duration):
    num_stimuli = int(model.params.sim_duration / isi + 1)
    first_stimulus_time = (model.params.sim_duration - (num_stimuli - 1) * isi) / 2
    stimulus_times = [first_stimulus_time + i * isi for i in range(num_stimuli)]
    for stim_time in stimulus_times:
            model.add_stimulus(column, A, stim_time, stim_time + stimulus_duration)

def set_locking_stimuli_for_all_columns(model, A, isi, stimulus_duration):
    num_stimuli = int((model.params.sim_duration/model.params.time_constant) / isi + 1)
    first_stimulus_time = ((model.params.sim_duration/model.params.time_constant) - (num_stimuli - 1) * isi) / 2
    stimulus_times = [first_stimulus_time + i * isi for i in range(num_stimuli)]
    for column in range(model.params.P):
        for stim_time in stimulus_times:
                model.add_stimulus(column, A, stim_time, stim_time + stimulus_duration)
    return stimulus_times

def set_stimuli_for_all_columns(model, A, start, stimulus_duration):
    for column in range(model.params.P):
          model.add_stimulus(column, A, start, start + stimulus_duration)