import numpy as np

from classes.Plotter import Plotter
from classes.A1Model import A1Model
from classes.Params import Params
from utils.Helper import set_locking_stimuli_for_all_columns

# --- Get Model Parameters --- #
factor = 6 # 1 for the same time duration as in the paper
stim_dur = 0.05 # maybe 0.025 or less if factor = 1
amp_factor = 1 # 1.6 seems to be good if factor = 1
amp_2_factor = 1 # 1.6 seems to be good if factor = 1
params = Params(sim_duration=4.5 * factor, seed=12)
params.time_constant = params.tau_rec

# --- Initialise the model --- #
a1_model = A1Model(params)

# --- Run for all neurons --- #
stim_times = set_locking_stimuli_for_all_columns(a1_model, 0.7 * amp_factor, 1.3 * factor, stim_dur)
a1_model.add_stimulus(8, 0.6 * amp_2_factor, 1 * factor, 4.5 * factor)
a1_model.run(all_neurons=True)

outputs = a1_model.get_activity().E
act_8_all = np.mean(outputs[:, 7, :], axis=1)
act_other_all = np.mean(np.mean(np.delete(outputs, 7, axis=1), axis = 1), axis = 1)
x = a1_model.get_activity().x
y = a1_model.get_activity().y
x_8_all = np.mean(x[:,7,:], axis = 1)
x_other_all = np.mean(np.mean(np.delete(x, 7, axis=1), axis = 1), axis = 1)
y_8_all = np.mean(y[:,7,:], axis = 1)
y_other_all = np.mean(np.mean(np.delete(y, 7, axis=1), axis = 1), axis = 1)

# --- Run for spontaneous neurons --- #
set_locking_stimuli_for_all_columns(a1_model, 1.2 * amp_factor, 1.3 * factor, stim_dur)
a1_model.add_stimulus(8, 1.1 * amp_2_factor, 1 * factor, 4.5 * factor)
a1_model.run()

outputs = a1_model.get_activity().E
act_8_spont = np.mean(outputs[:, 7, :], axis=1)
act_other_spont = np.mean(np.mean(np.delete(outputs, 7, axis=1), axis = 1), axis = 1)
x = a1_model.get_activity().x
y = a1_model.get_activity().y
x_8_spont = np.mean(x[:,7,:], axis = 1)
x_other_spont = np.mean(np.mean(np.delete(x, 7, axis=1), axis = 1), axis = 1)
y_8_spont = np.mean(y[:,7,:], axis = 1)
y_other_spont = np.mean(np.mean(np.delete(y, 7, axis=1), axis = 1), axis = 1)

plotter = Plotter(a1_model)
plotter.figure_11(factor, stim_dur, stim_times,
            act_other_all, act_8_all, act_other_spont, act_8_spont,
            x_8_all, x_other_all, x_8_spont, x_other_spont,
            y_8_all, y_other_all, y_8_spont, y_other_spont)