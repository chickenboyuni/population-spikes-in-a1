#import numpy as np

from classes.A1Model import A1Model
from classes.Params import Params
from classes.Plotter import Plotter

a1_models = []

# --- Get Model Parameters --- #
params_2 = Params(sim_duration=0.5, seed=2)

# --- Initialise the model --- #
a1_model_2 = A1Model(params_2)

# --- Define the Stimuli --- #
a1_model_2.add_stimulus(8, 4, 0.35, 0.5)

# --- Run Simulation with Seed 2 --- #
a1_model_2.run()

# --- Save Simulation Results --- #
a1_models.append(a1_model_2)


# --- Get Model Parameters --- #
params_28 = Params(sim_duration=0.5, seed=28)

# --- Initialise the model --- #
a1_model_28 = A1Model(params_28)

# --- Define the Stimuli --- #
a1_model_28.add_stimulus(8, 4, 0.05, 0.5)

# --- Run Simulation with Seed 28 --- #
a1_model_28.run()

# --- Save Simulation Results --- #
a1_models.append(a1_model_28)


# --- Get Model Parameters --- #
params_47 = Params(sim_duration=0.5, seed=47)

# --- Initialise the model --- #
a1_model_47 = A1Model(params_47)

# --- Define the Stimuli --- #
a1_model_47.add_stimulus(8, 4, 0.15, 0.5)

# --- Run Simulation with Seed 47 --- #
a1_model_47.run()

# --- Save Simulation Results --- #
a1_models.append(a1_model_47)


# --- Get Model Parameters --- #
params_64 = Params(sim_duration=0.5, seed=64)

# --- Initialise the model --- #
a1_model_64 = A1Model(params_64)

# --- Define the Stimuli --- #
a1_model_64.add_stimulus(8, 4, 0.25, 0.5)

# --- Run Simulation with Seed 64 --- #
a1_model_64.run()

# --- Save Simulation Results --- #
a1_models.append(a1_model_64)


# --- Plot Figure 2 --- #
colours = ['red', 'blue', 'black', 'green']
alphas = [0.7, 0.7, 1, 0.7]
styles = ['-', '-', '-', '-']

plotter = Plotter(a1_model_47)
plotter.figure_2a(a1_models, colours, alphas, styles)
