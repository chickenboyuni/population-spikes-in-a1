import numpy as np

from classes.A1Model import A1Model
from classes.Params import Params
from classes.Plotter import Plotter

# --- Define a Function to Compute Frequency Tuning Curves --- #
def compute_ftc(a1_model):    
    A_max, A_step = 16, 0.2
    A_range = np.arange(0, A_max + A_step, A_step)
    ftc = np.full(Params.P, np.nan)
    
    for Q in range(Params.P):
        for i, A in enumerate(A_range):
                # Simulate model
            a1_model.add_stimulus(Q+1, A, 0.01, 0.1)
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


# --- Initialise the Model --- #
params = Params(sim_duration=0.5)
a1_model = A1Model(params)
a1_model.update_params(sim_duration=0.1, dt=0.001)


# --- I-C Connections --- #
ftc_1 = []

#a1_model.update_params(J_1_EE=0.045, J_1_IE=0.0035, J_2_EE=0.015, J_2_IE=0.0015)
label = 'With I-C'
#ftc_1.append((compute_ftc(a1_model), 'o', '-', 'black', 2, label))
ftc_1.append(([12.2,10.8,9.4,8,6.4,4.8,3.6,1.6,3.6,4.8,6.4,8,9.4,10.8,12.2],
              'o', '-', 'black', 2, label))

#a1_model.update_params(J_1_EE=0, J_1_IE=0, J_2_EE=0, J_2_IE=0)
label = 'Without I-C'
#ftc_1.append((compute_ftc(a1_model), 'o', ':', 'black', 2, label))
ftc_1.append(([16,14.4,12.8,11,9.2,7.4,5.2,1.6,5.2,7.4,9.2,11,12.8,14.4,16],
              'o', ':', 'black', 2, label))



# --- Recurrent Inhibition --- #
ftc_2 = []

a1_model.update_params(J_1_EE=0.045, J_1_IE=0.0035, J_2_EE=0.015, J_2_IE=0.0015,
                       J_0_EI=-2)
label = rf'$J^{{0}}_{{EI}} = {a1_model.params.J_0_EI:.0f}$'
ftc_2.append((compute_ftc(a1_model), 'o', '-', 'black', 2, label))

a1_model.update_params(J_0_EI=-6)
label = rf'$J^{{o}}_{{EI}} = {a1_model.params.J_0_EI:.0f}$'
ftc_2.append((compute_ftc(a1_model), 'o', ':', 'black', 2, label))


# --- Asymmetry --- #
ftc_3 = []

a1_model.update_params(J_0_EI=-4)
label = rf'$\delta_{{left}} = {a1_model.params.delta_left:.0f}$'
#ftc_3.append((compute_ftc(a1_model), 'o', '-', 'black', 2, label))
ftc_3.append(([12.2,10.8,9.4,8,6.4,4.8,3.6,1.6,3.6,4.8,6.4,8,9.4,10.8,12.2],
             'o', '-', 'black', 2, label))

a1_model.update_params(delta_left=8)
label = rf'$\delta_{{left}} = {a1_model.params.delta_left:.0f}$'
#ftc_3.append((compute_ftc(a1_model), 'o', ':', 'black', 2, label))
ftc_3.append(([12.2,10.8,9.4,8,6.4,4.8,3.6,1.6,4,6,8.2,10.4,12.4,14.6,np.nan],
             'o', ':', 'black', 2, label))


a1_model.update_params(delta_left=16)
label = rf'$\delta_{{left}} = {a1_model.params.delta_left:.0f}$'
#ftc_3.append((compute_ftc(a1_model), 'x', '-', 'black', 2, label))
ftc_3.append(([12.2,10.8,9.4,8,6.4,4.8,3.6,1.6,4.6,8.2,12,15.8,np.nan,np.nan],
             'x', '-', 'black', 2, label))


a1_model.update_params(delta_left=32)
label = rf'$\delta_{{left}} = {a1_model.params.delta_left:.0f}$'
#ftc_3.append((compute_ftc(a1_model), 'x', ':', 'black', 2, label))
ftc_3.append(([12.2,10.8,9.4,8,6.4,4.8,3.6,1.6,5.4,11.6,np.nan,np.nan,np.nan,np.nan],
             'x', ':', 'black', 2, label))



# --- U-Shaped FTC --- #
ftc_4 = []

a1_model.update_params(delta_left=5,
                       J_1_EE=0.045, J_2_IE=0.0015)
label = rf'$J^{{1}}_{{EE}} = {a1_model.params.J_1_EE:.3f}, \, J^{{2}}_{{IE}} = {a1_model.params.J_2_IE:.4f}$'
ftc_4.append((compute_ftc(a1_model), 'o', '-', 'black', 2, label))

a1_model.update_params(J_1_EE=0.070, J_2_IE=0.0070)
label = rf'$J^{{1}}_{{EE}} = {a1_model.params.J_1_EE:.3f}, \, J^{{2}}_{{IE}} = {a1_model.params.J_2_IE:.4f}$'
ftc_4.append((compute_ftc(a1_model), 'o', ':', 'black', 2, label))


# --- Plot FTCs --- #
ftc_list = [
   ftc_1,
   ftc_2,
   ftc_3,
   ftc_4,
]

Plotter.figure_5a(ftc_list)
