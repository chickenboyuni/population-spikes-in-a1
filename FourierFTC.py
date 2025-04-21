import numpy as np

from classes.A1Model import A1Model
from classes.Params import Params
from classes.Plotter import Plotter


# --- Initialise the Model --- #
params = Params(sim_duration=0.5)
a1_model = A1Model(params)
a1_model.update_params(sim_duration=0.1, dt=0.001)


# --- Define a Function to Compute Frequency Tuning Curves --- #
def compute_ftc(e_E_distribution):    
    a1_model.update_params(e_E=e_E_distribution)  # Initialise model
    
    A_max, A_step = 16, 0.2
    A_range = np.arange(0, A_max + A_step, A_step)
    ftc = np.zeros(Params.P)
    
    for Q in range(Params.P):
        for i, A in enumerate(A_range):
                # Simulate model
            a1_model.add_stimulus(Q+1, A, 0.01, 0.06)
            a1_model.run()
                # Retrieve maximal activity
            E_activity = a1_model.get_activity().E
            E_activity_col_max = np.max(np.mean(E_activity, axis=2), axis=0)
                # Extract population spikes
            thrshld = 20
            if E_activity_col_max[7] > thrshld:
                ftc[Q] = A
                break
    return ftc


# --- Apply FFT on Background Input & Reconstruct --- #
    # Set random seed
np.random.seed(Params.seed)
    # Compute linear distribution of e_E
e_E_linear = np.linspace(Params.e_E_1, Params.e_E_NE, Params.N_E)
    # Compute random distribution of e_E
e_E_random = np.sort(np.random.uniform(Params.e_E_1, Params.e_E_NE, Params.N_E))
    # Normalise e_E so that it ranges from e_E_1 to e_E_NE
e_E_random = -10 + (((e_E_random - e_E_random[0]) * 20) / (e_E_random[-1] - e_E_random[0]))
    # Extract the difference of e_E from the linear dist
signal = e_E_random - e_E_linear
    # Apply FFT
fft_signal = np.fft.fft(signal)
frequencies = np.fft.fftfreq(Params.N_E)
    # Define FFT restrictions
cutoff_amp = 0.07 * np.max(np.abs(fft_signal))  # Retain components >7% of max amplitude
cutoff_freq = 0.3  * np.max(frequencies)  # Retain components > 30% of max frequency
    # Restrict FFT by amplitude and frequency
fft_reconstructed = np.copy(fft_signal)
for i in range(len(frequencies)):
    if np.abs(frequencies[i]) > cutoff_freq or np.abs(fft_signal[i]) < cutoff_amp:
        fft_reconstructed[i] = 0
signal_reconstructed = np.fft.ifft(fft_reconstructed).real
    # Reconstruct e_E with restricted FFT
e_E_reconstructed = signal_reconstructed + e_E_linear


# --- Extract Individual Components --- #
space = np.arange(Params.N_E)
components = []

for i in range(Params.N_E // 2):
    amplitude = np.abs(fft_reconstructed[i]) / Params.N_E
    phase = np.angle(fft_reconstructed[i])
    frequency = frequencies[i]
    
    if amplitude > 0:
        component = amplitude * np.cos(2 * np.pi * frequency * space + phase)
        components.append((frequency, component))

y_min = min(np.min(comp) for _, comp in components[1:])
y_max = max(np.max(comp) for _, comp in components[1:])


# --- Compute FTCs for Individual Components --- #
print("Computing FTC for Linear e_E ...")
ftc_linear = compute_ftc(e_E_linear)

ftc_components, freq_components = [], []
for i, (freq, comp) in enumerate(components[1:]):
    e_E_component = comp + e_E_linear
    print(f"Computing FTC for component {i+1} of {len(components)-1} ...")
    ftc_components.append((compute_ftc(e_E_component), freq, comp))
    freq_components.append(freq)


# --- Compute FTCs for Random & Reconstructed Distributions --- #
ftc = []

print("Computing FTC for Random e_E ...")
ftc.append((compute_ftc(e_E_random), 'o', '-', 'green', 2, r'$e^E$ Random'))

print("Computing FTC for reconstructed e_E ...")
ftc.append((compute_ftc(e_E_reconstructed), 'x', '--', 'black', 1, r'$e^E$ Reconstructed'))


# --- Plot FFT Reconstruction --- #
plotter = Plotter(a1_model)
plotter.fft_1(signal, signal_reconstructed, frequencies,
            fft_signal, fft_reconstructed)

plotter.fft_2(ftc, ftc_linear, ftc_components, y_min, y_max)
