import numpy as np

from classes.A1Model import A1Model
from classes.Params import Params
from classes.Plotter import Plotter

# --- Get Model Parameters --- #
params = Params(sim_duration=0.05, seed=47)
params.time_constant = params.tau_rec

# --- Initialise Model --- #
a1_model = A1Model(params)

# --- Initialise Amplitude Range --- #
A_range = 16
A_step = 0.2  # Set to 0.1 for best accuracy
steps_A = int(A_range / A_step)
A_values = np.linspace(0, A_range - A_step, steps_A)

# --- Initialise Outputs --- #
output_masker = np.zeros((steps_A, a1_model.params.P))

for a in range(steps_A):
    # --- Define the Stimuli --- #
    a1_model.add_stimulus(8, A_values[a], 0, 0.05)

    # --- Run Simulation --- #
    a1_model.run()

    E_activity = a1_model.get_activity().E

    # Detect population spikes (PS) in response to the masker
    thrshld = 20  # Set threshold for population spike
    E_activity_col_max = np.max(np.mean(E_activity, axis=2), axis=0)

    for Q in range(a1_model.params.P):
        if E_activity_col_max[Q] > thrshld:
            output_masker[a, Q] = 1

# --- Define ISIs for Forward Masking --- #
ISIs = [0.5, 1, 2]
# ISI_labels = ['ISI of 𝛕rec/2', 'ISI of 𝛕rec', 'ISI of 2*𝛕rec', 'Response to First Input']
ISI_labels = [r'ISI of $\tau_{\mathrm{rec}} \, / \, 2$', r'ISI of $\tau_{\mathrm{rec}}$',
              r'ISI of $2 \cdot \tau_{\mathrm{rec}}$', 'Response to First Input']

# --- Run Simulation for Different ISIs --- #
outputs = []
for isi in ISIs:
    output = np.zeros((steps_A, a1_model.params.P))
    a1_model.update_params(sim_duration=isi + 0.05)
    for a in range(steps_A):
        # --- Define the Stimuli --- #
        a1_model.add_stimulus(8, A_values[a], 0, 0.05)
        a1_model.add_stimulus(8, A_values[a], isi, isi + 0.05)

        # --- Run Simulation --- #
        a1_model.run()

        E_activity = a1_model.get_activity().E

        E_activity_probe = E_activity[int(isi * a1_model.params.time_constant / a1_model.params.dt):int(
            (isi + 0.05) * a1_model.params.time_constant / a1_model.params.dt), :, :]

        # Detect population spikes (PS) in response to the probe
        thrshld = 20  # Set threshold for population spike
        E_activity_col_max = np.max(np.mean(E_activity_probe, axis=2), axis=0)

        for Q in range(a1_model.params.P):
            if E_activity_col_max[Q] > thrshld:
                output[a, Q] = 1

    outputs.append(output)

# --- Plot Figure 6 --- #
plotter = Plotter(a1_model)
plotter.figure_8(output_masker, outputs, ISI_labels, A_values)