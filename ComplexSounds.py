from classes.A1Model import A1Model
from classes.Params import Params
from classes.Plotter import Plotter
from utils.Helper import set_white_noise, set_complex_sound_stimuli_C

# --- Get Model Parameters --- #
params = Params(sim_duration=2.5)
params.time_constant = params.tau_rec

# --- Initialise the model --- #
a1_model = A1Model(params)

# --- Define the Stimuli --- #
set_complex_sound_stimuli_C(a1_model)

# --- Run Simulation --- #
a1_model.run()

# --- Plot Results --- #
plotter = Plotter(a1_model)
plotter.figure_13()

# --- White Noise --- #
set_white_noise(a1_model, 2.5, 0.5, 2, 20)

# --- Run Simulation --- #
a1_model.run()

# --- Plot Results --- #
plotter = Plotter(a1_model)
plotter.figure_13()