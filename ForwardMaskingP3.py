import numpy as np
import matplotlib.pyplot as plt
import matplotlib

from classes.A1Model import A1Model
from classes.Params import Params
from classes.Plotter import Plotter


# --- Get Model Parameters --- #
params = Params(sim_duration=2, seed=47)
params.time_constant = params.tau_rec

# --- Initialise Model --- #
a1_model = A1Model(params)


# --- Initialise Amplitude Range --- #
A_range = 10
A_step = 0.5  # Set to 0.1 for best accuracy
steps_A = int(A_range / A_step)
A_values = np.linspace(0, A_range - A_step, steps_A)

# # --- Initialise Stimuli Variables --- #
# probe_col = 8
# probe_amp = 4
# probe_duration = 0.05
# offset = 1.8

# # --- Initialise Outputs --- #
# outputs = []
# figure_data = {
#     "A": {
#         "output_masker": np.zeros((steps_A, a1_model.params.P))
#     },
#     "B": {
#         "output_probe": np.zeros((steps_A, a1_model.params.P))
#     },
#     "C": {
#         "output_probe": np.zeros((steps_A, a1_model.params.P))
#     },
#     "D": {
#         "output_probe": np.zeros((steps_A, a1_model.params.P))
#     }
# }

# # --- Initialise Inputs --- #
# figure_input = {
#     "A": {
#         "stimuli": {
#             "masker": [0, 0.05],
#         }
#     },
#     "B": {
#         "stimuli": {
#             "masker": [0, 0.05],
#             "probe": [0.06, 0.06 + probe_duration] # Small recovery time between masker and probe (10ms)
#         }
#     },
#     "C": {
#         "stimuli": {
#             "masker": [0, 0.05],
#             "probe": [0.06 + offset, 0.06 + probe_duration + offset] # Long recovery time between masker and probe (offset)
#         }
#     },
#     "D": {
#         "stimuli": {
#             "masker": [0, 0.05 + offset], # The masker is as long as C's recovery delay
#             "probe": [0.06 + offset, 0.06 + probe_duration + offset]
#         }
#     }
# }

# # --- Figure 9A --- #
# for figure in figure_input:
#     for amp in range(steps_A):
#         for bf_column in range(a1_model.params.P):

#             masker_input = figure_input[figure]["stimuli"]["masker"]
#             measurement_time_start = 0
#             measurement_time_end = int(masker_input[1] * a1_model.params.time_constant / a1_model.params.dt) 
                                            
#             # --- Define the Stimuli --- #
#             a1_model.add_stimulus(bf_column+1, A_values[amp], masker_input[0], masker_input[1])

#             if(figure != "A"):

#                 probe_input = figure_input[figure]["stimuli"]["probe"]
#                 measurement_time_start = int(probe_input[0] * a1_model.params.time_constant / a1_model.params.dt) 
#                 measurement_time_end = int(probe_input[1] * a1_model.params.time_constant / a1_model.params.dt) 

#                 a1_model.add_stimulus(probe_col, probe_amp, probe_input[0], probe_input[1])


#             # --- Run Simulation --- #
#             a1_model.run()

#             E_activity = a1_model.get_activity().E
#             mean_E = np.mean(np.mean(E_activity[measurement_time_start : measurement_time_end, 7, :], axis=1), axis=0)
            
#             if(figure == "A"):
#                 figure_data["A"]["output_masker"][amp, bf_column] = mean_E

#             else:
#                 figure_data[figure]["output_probe"][amp, bf_column] = mean_E

# a1_model.cache.cache_figure_data(figure_data, "figure9")

figure_data = a1_model.cache.get_figure_data("figure9")

plotter = Plotter(a1_model)
plotter.figure_9(figure_data, steps_A, A_values)

plt.show()