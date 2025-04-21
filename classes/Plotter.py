import matplotlib
import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits.axes_grid1 import make_axes_locatable

class Plotter:
    def __init__(self, model):
        """
        Initialise the Plotter with an A1Model object.
        """
        self.model = model
        self.params = model.params


    def figure_2(self):
        """
        Recreate Figure 2 from the paper.
        """
        p = self.params
        fig, ax = plt.subplots(3, p.P, figsize=(15, 7.5), gridspec_kw={'height_ratios': [2, 1, 1]}, sharex=False, sharey=False)

        time_axis = np.arange(0, p.sim_duration, p.dt)
        P_min, P_max = 0, 15

        for Q in range(P_min, P_max):
            # Plot network activity
            ax[0, Q].plot(time_axis, np.mean(self.model.activity.E[:, Q, :], axis=1))
            ax[0, Q].set_title(f"Col. {Q + 1}")
            ax[0, Q].set_ylim([0, 80])
            if Q == P_min:
                ax[0, Q].set_ylabel("Network Activity (Hz)")
            else:
                ax[0, Q].set_yticklabels([])

            # Plot input amplitude
            ax[1, Q].plot(np.arange(0, p.sim_duration, p.stim_step_size),
                          np.mean(self.model.sensory_input_matrix[:, Q, self.model.spont_index:p.N_E], axis=1))
            ax[1, Q].set_ylim([-0.5, 4.5])
            if Q == P_min:
                ax[1, Q].set_ylabel("Input Amplitude (Hz)")
            else:
                ax[1, Q].set_yticklabels([])

        # Compute max amplitude of s for each column
        max_s = np.max(np.mean(self.model.sensory_input_matrix[:, :, self.model.spont_index:p.N_E], axis=2), axis=0)

        # Remove the last row of subplots to make space for ax2
        for Q in range(p.P):
            fig.delaxes(ax[2, Q])

        # Create a new axis that spans all columns
        ax2 = plt.subplot2grid((3, p.P), (2, P_min), colspan=(P_max - P_min))
        ax2.plot(range(P_min, P_max), max_s[P_min:P_max], marker='o', linestyle='-')
        ax2.set_xlabel("Column")
        ax2.set_ylabel("Max s Amplitude")
        ax2.set_ylim([0, 4.5])
        ax2.set_xlim([-0.35, 14.35])
        ax2.set_xticks(range(0, 15))
        ax2.set_xticklabels(range(1, 16))

        plt.tight_layout()
        plt.subplots_adjust(wspace=0.3)
        plt.show()
    
    
    def figure_2a(self, a1_models, colours, alphas, styles):
        """
        Expand on Figure 2 from the paper.
        """
        plt.rcParams.update({'xtick.labelsize': 12, 'ytick.labelsize': 12})
        
        p = self.params
        
        fig, ax = plt.subplots(3, p.P, figsize=(12, 7), gridspec_kw={'height_ratios': [2, 1, 1]}, sharex=False, sharey=False)
        time_axis = np.arange(0, p.sim_duration, p.dt)
        P_min, P_max = 3, 12
        
        # Remove unused plots
        for Q in range(P_min):
            fig.delaxes(ax[0, Q])
            fig.delaxes(ax[1, Q])
        for Q in range(P_max, p.P):
            fig.delaxes(ax[0, Q])
            fig.delaxes(ax[1, Q])

        for Q in range(P_min, P_max):
            for i, a1_model in enumerate(a1_models):
                ax[0, Q].plot(time_axis, np.mean(a1_model.activity.E[:, Q, :], axis=1),
                              color=colours[i], alpha=alphas[i], linestyle=styles[i])
                ax[0, Q].set_ylim([-2, 110])
                ax[0, Q].set_xlim([-0.05, 0.55])
                ax[0, Q].set_xticklabels([])
                if Q == P_min:
                    ax[0, Q].set_ylabel("Network Activity [Hz]", fontsize=14)
                else:
                    ax[0, Q].set_yticklabels([])
    
            # Plot input amplitude
            ax[1, Q].plot(np.arange(0, p.sim_duration, p.stim_step_size),
                          np.mean(self.model.sensory_input_matrix[:, Q, self.model.spont_index:p.N_E], axis=1),
                          color='black')
            ax[1, Q].set_ylim([-0.5, 4.5])
            ax[1, Q].set_xlim([-0.05, 0.55])
            ax[1, Q].set_xticks([0, 0.5])
            if Q == P_min:
                ax[1, Q].set_ylabel("Input\nAmplitude [Hz]", fontsize=14)
                ax[1, Q].set_xticklabels([0, 500])
            else:
                ax[1, Q].set_yticklabels([])
                ax[1, Q].set_xticklabels([])
            
        fig.text(0.51, 0.288, "Time [ms]", ha='center', fontsize=14)

        # Compute max amplitude of s for each column
        max_s = np.max(np.mean(self.model.sensory_input_matrix[:, :, self.model.spont_index:p.N_E], axis=2), axis=0)

        # Remove the last row of subplots to make space for ax2
        for Q in range(p.P):
            fig.delaxes(ax[2, Q])

        # Create a new axis that spans all columns
        ax2 = plt.subplot2grid((3, p.P), (2, P_min), colspan=(P_max - P_min))
        ax2.plot(range(P_min, P_max), max_s[P_min:P_max], marker='o', linestyle='-', color='black')
        ax2.set_xlabel("Column Index", fontsize=14)
        ax2.set_ylabel(r"Max $s_i$" "\nAmplitude [Hz]", fontsize=14)
        ax2.set_ylim([-0.5, 4.5])
        ax2.set_xlim([2.65, 11.35])
        ax2.set_xticks(range(3, 12))
        ax2.set_xticklabels(range(4, 13))

        #plt.tight_layout()
        plt.subplots_adjust(wspace=0.6, hspace=0.3)
        plt.show()


    def figure_3(self, E_act_store, s_act_store):
        """
        Recreate Figure 3 from the paper.
        """
        fig, ax = plt.subplots(8, 1, figsize=(8, 6), sharex=False, sharey=False, gridspec_kw={'hspace': 0.3})

        custom_cmap = matplotlib.colormaps.get_cmap("jet")
        vmin, vmax = 2, 78

        labels = ["VII", "VI", "V", "IV", "III", "II", "I"]

        for i, (E_act, label) in enumerate(zip(E_act_store, labels)):
            im = ax[i].imshow(E_act, aspect="auto", cmap=custom_cmap, vmin=vmin, vmax=vmax,
                              origin='lower', interpolation='nearest', extent=[0, 15, 0, 50])
            ax[i].set_ylim(0, 50)
            ax[i].set_yticks([0, 50])
            ax[i].set_xticks([])
            ax[i].set_yticklabels(["0", "50"], fontsize=10)
            ax[i].text(14.5, 49, label, va="bottom", ha="center", fontsize=10)

        fig.text(0.06, 0.5, "Time [ms]", va="center", rotation="vertical", fontsize=12)

        P_min, P_max = 0, 15
        colors = ["b", "k", "r"]

        for s_act, color in zip(s_act_store, colors):
            ax[-1].plot(range(P_min, P_max), s_act[P_min:P_max], linestyle='-', color=color, linewidth=1.5)

        ax[-1].set_ylim(0, 10)
        ax[-1].set_xlabel("Column Index", fontsize=12)
        ax[-1].set_ylabel("Input Amp.", fontsize=12)
        ax[-1].set_xlim([-0.35, 14.35])
        ax[-1].set_xticks([3, 7, 11])
        ax[-1].set_xticklabels([4, 8, 12])
        ax[-1].set_yticks([0, 8])
        ax[-1].set_yticklabels([0, 8])

        ax[-1].spines['top'].set_visible(False)
        ax[-1].spines['right'].set_visible(False)

        cbar = fig.colorbar(im, ax=ax.ravel().tolist(), orientation="vertical", shrink=0.355, aspect=4.5,
                            anchor=(0.0, 0.2), pad=0.01)
        cbar.set_ticks([20, 60])
        cbar.set_ticklabels(["20 Hz", "60 Hz"])
        cbar.outline.set_edgecolor('black')
        cbar.outline.set_linewidth(0.5)

        plt.show()


    def figure_4(self, E_weak, I_weak, E_strong, I_strong, output):
        """
        Recreate Figure 4 from the paper.
        """
        # --- Figure 4A: Excitatory and Inhibitory Responses --- #
        fig, ax = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

        for idx, (E_data, I_data, title) in enumerate([(E_weak, I_weak, "Weak"), (E_strong, I_strong, "Strong")]):
            E_diff = np.diff(np.mean(E_data, axis=1), axis=0)
            I_diff = np.diff(np.mean(I_data, axis=1), axis=0)

            E_thrshld = 0.4 * np.max(E_diff)
            I_thrshld = 0.4 * np.max(I_diff)

            E_onset = (np.where(E_diff >= E_thrshld)[0][0]) * self.model.params.dt * 1000
            I_onset = (np.where(I_diff >= I_thrshld)[0][0]) * self.model.params.dt * 1000

            time_axis = np.arange(0, self.model.params.sim_duration * 1000, self.model.params.dt * 1000)

            ax[idx].plot(time_axis, np.mean(E_data, axis=1), label='Excitatory', color='blue')
            ax[idx].plot(time_axis, np.mean(I_data, axis=1), label='Inhibitory', color='red')
            ax[idx].axvline(10, color='k', linestyle='--')
            ax[idx].axvline(E_onset, color='blue', linestyle='--')
            ax[idx].axvline(I_onset, color='red', linestyle='--')
            ax[idx].set_ylabel('Firing rate (Hz)')
            ax[idx].set_ylim([0, 80])
            ax[idx].set_title(f'{title} Stimulus Response')
            ax[idx].legend()

        ax[-1].set_xlabel('Time (ms)')
        plt.tight_layout()

        # --- Figure 4B: Latency of PS vs. Stimulus Amplitude --- #
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(output[:, 0], output[:, 1], marker='o', color='blue', label="Excitatory")
        ax.scatter(output[:, 0], output[:, 2], marker='o', color='red', label="Inhibitory")

        ax.set_xlabel("Tone Amplitude (Hz)")
        ax.set_ylabel("Latency to Response (ms)")
        ax.set_ylim([0, 40])
        ax.legend()

        plt.tight_layout()
        plt.show()

    def figure_5(ftc):
        """
        Recreate Figure 5 from the paper.
        """
        plt.figure(figsize=(8, 6))

        for i, (FTC, marker, style, colour, linewidth, label) in enumerate(ftc):
            plt.plot(FTC, marker=marker, linestyle=style, color=colour,
                     linewidth=linewidth, label=label)
        plt.ylim([0, 10])
        plt.xlim([0, 14])
        plt.xticks(range(0, 15), range(1, 16))
        plt.legend(loc="lower left", frameon=False)
        plt.xlabel("Column Index")
        plt.ylabel("Input Amplitude (Hz)")   
        
        plt.tight_layout()
        plt.show()
    
    def figure_5a(ftc_list):
        """
        Create second figure for reproducibility section.
        """        
        fig, ax = plt.subplots(2, 2, figsize=(10, 7))
        ax = ax.flatten()
        
        labels = ['A', 'C', 'B', 'D']
        
        for i, ftc in enumerate(ftc_list):
            for j, (FTC, marker, style, colour, linewidth, label) in enumerate(ftc):
                ax[i].plot(FTC, marker=marker, linestyle=style, color=colour,
                         linewidth=linewidth, label=label)
            ax[i].set_ylim([-1, 10])
            ax[i].set_xlim([0, 14])
            ax[i].set_xticks(range(0, 15), range(1, 16))
            ax[i].set_xlabel('Column Index', fontsize=14)
            ax[i].set_ylabel('Input Amplitude [Hz]', fontsize=14)   
            ax[i].legend(loc='lower left', bbox_to_anchor=(-0.01, -0.06), frameon=False, fontsize=14)
            
            if i // 2 == 0:
                ax[i].tick_params(axis='x', labelbottom=False)
                ax[i].set_xlabel('')
            if i % 2 != 0:
                ax[i].tick_params(axis='y', labelleft=False)
                ax[i].set_ylabel('')
            
            ax[i].text(0, 10.3, labels[i], va="bottom", ha="center", fontsize=14)
        
        plt.tight_layout(w_pad=0)
        plt.show()

    def figure_6(self, outputs, time_axes, ratio_A, ratio_F, ISI, A_vals, c_vals):
        """
        Recreate Figure 6 from the paper.
        """
        fig, ax = plt.subplots(3, 1, figsize=(5, 10), gridspec_kw={'hspace': 0.3})

        # Panel A: Network Activity
        for output, time_axis in zip(outputs, time_axes):
            ax[0].plot(time_axis, np.mean(output[:, 7, :], axis=1), color='black', linewidth=0.8)
        ax[0].set_ylabel('Network Activity [Hz]', fontsize=12, fontweight='bold')
        ax[0].set_xlim([-0.1, 4.2])
        ax[0].set_ylim([-0.1, 85])
        ax[0].tick_params(axis='both', labelsize=10)

        # Panel B: P2/P1 Ratio vs. Input Amplitude
        markers = ['+', 'o', 's']  # Different markers for each amplitude
        linestyles = ['dashed', 'dotted', 'solid']  # Line styles to differentiate
        for i in range(ratio_A.shape[0]):
            ax[1].plot(ISI, ratio_A[i], marker=markers[i], linestyle=linestyles[i], color='black',
                       label=f'Input Amplitude {A_vals[i]}', markersize=6)
        ax[1].set_ylabel('P2/P1 Ratio', fontsize=12, fontweight='bold')
        ax[1].set_xlim([-0.1, 4.2])
        ax[1].set_ylim([0, 1])
        ax[1].tick_params(axis='both', labelsize=10)
        ax[1].legend(fontsize=10, loc='lower right', frameon=False)

        # Panel C: P2/P1 Ratio vs. Column Number
        markers = ['+', 'o', 's', 'x', 'd']  # Different markers for each column
        linestyles = ['dashed', 'dotted', 'solid', 'dashdot', (0, (3, 1, 1, 1))]  # Matching line styles
        for i in range(ratio_F.shape[0]):
            ax[2].plot(ISI, ratio_F[i], marker=markers[i], linestyle=linestyles[i], color='black',
                       label=f'Column {c_vals[i] + 1}', markersize=6)
        ax[2].set_xlabel(r'Inter-Stimulus Interval [$\tau_{\mathrm{rec}}$]', fontsize=12, fontweight='bold')
        ax[2].set_ylabel('P2/P1 Ratio', fontsize=12, fontweight='bold')
        ax[2].set_xlim([-0.1, 4.2])
        ax[2].set_ylim([0, 1])
        ax[2].tick_params(axis='both', labelsize=10)
        ax[2].legend(fontsize=10, loc='lower right', frameon=False)

        plt.show()


    def figure_8(self, output_masker, outputs, ISI_labels, A_values):
        """
        Recreate Figure 8 from the paper.
        """
        # --- Plot Figure 8 --- #
        plt.figure(figsize=(12, 8))
        # Plot FTC for the masker (baseline)
        transition_x_masker = []
        transition_y_masker = []
        for col in range(output_masker.shape[1]):
            for row in range(output_masker.shape[0]):
                if output_masker[row, col] == 1:
                    transition_x_masker.append(col)
                    transition_y_masker.append(A_values[row])
                    break  # Stop at the first transition point from 0 to 1
        plt.plot(transition_x_masker, transition_y_masker, marker='o', linestyle='-', color='black',
                 label="Masker FTC (Response to First Input)")

        # Plot FTC for the probe at different ISIs
        for i, output_probe in enumerate(outputs):
            transition_x_probe = []
            transition_y_probe = []

            for col in range(output_probe.shape[1]):
                for row in range(output_probe.shape[0]):
                    if output_probe[row, col] == 1:
                        transition_x_probe.append(col)
                        transition_y_probe.append(A_values[row])
                        break  # Stop at the first transition point from 0 to 1

            plt.plot(transition_x_probe, transition_y_probe, marker='o', linestyle='--',
                     label=f"Probe FTC (ISI = {ISI_labels[i]})")

        plt.xlabel("Column Index")
        plt.ylabel("Input Amplitude (Hz)")
        plt.ylim([0, 10])
        plt.xlim([0, 14])
        plt.xticks(range(0, 15), labels=range(1, 16))
        plt.legend()
        plt.tight_layout()
        plt.show()

    def figure_9(self, figure_data, steps_A, A_values):
        

        fig, ax = plt.subplots(2, 2, figsize=(34, 8), sharex=False, sharey=False, gridspec_kw={'wspace': 0.2, "hspace": 0.3})
        custom_cmap = matplotlib.colormaps.get_cmap("jet")

        for ax_idx, figure in enumerate(figure_data):
            ax = ax.reshape(-1)

            output = "output_masker" if figure == "A" else "output_probe"

            data = np.array(figure_data[figure][output])

            vmin, vmax = 5, 28
            im1 = ax[ax_idx].imshow(data, aspect='auto', vmin=vmin, vmax=vmax, cmap=custom_cmap)


            ax[ax_idx].set_ylim(0, steps_A)
            ax[ax_idx].set_xticks([0, 7, 14])
            ax[ax_idx].set_yticks(np.arange(0, steps_A, 5))
            ax[ax_idx].set_yticklabels([f"{int(val)}" for val in A_values[::5]], fontsize=18) 
            ax[ax_idx].set_xticklabels([1, 8, 15], fontsize=18) 

            masker = 'M'
            probe_offset = 1

            masker_margin = 0

            if(figure == "D"):
                masker = '                 M                 '
                masker_margin = 3.5
                probe_offset = 8

            if(figure == "C"):
                probe_offset = 8

                ax[ax_idx].text(3.9, data.shape[0] + 0.7, '                                                                     ', 
                    ha='center', va='bottom', fontsize=6, fontweight='bold', 
                    bbox=dict(facecolor='white', edgecolor='black', boxstyle='rarrow,pad=0.0001'))


            ax[ax_idx].text(masker_margin, data.shape[0] + 0.7, masker, 
                    ha='center', va='bottom', fontsize=12, fontweight='bold', 
                    bbox=dict(facecolor='white', edgecolor='black', boxstyle='square,pad=0.3'))
            
            if(figure != "A"):
                ax[ax_idx].text(probe_offset, data.shape[0] + 0.7, 'P', 
                        ha='center', va='bottom', fontsize=12, fontweight='bold', 
                        bbox=dict(facecolor='white', edgecolor='black', boxstyle='square,pad=0.3'))



        cbar1 = fig.colorbar(im1, ax=ax.ravel().tolist(), orientation="vertical", shrink=0.8, pad=0.02)
        cbar1.set_ticks([10, 20])
        cbar1.set_ticklabels(["10 Hz", "20 Hz"], fontsize=18)
        cbar1.outline.set_edgecolor('black')
        cbar1.outline.set_linewidth(0.5)

        fig.supxlabel('Stimulus Column Index', x= 0.45, y=0.01, fontsize=20)
        fig.supylabel('Stimulus Amplitude [Hz]', x=0.075, fontsize=20)

        plt.show()


    def figure_13(self):
        """
        Recreate Figure 13 from the paper.
        """
        E_act_mean = np.mean(self.model.activity.E, axis=2)

        fig, ax = plt.subplots(1, 2, figsize=(12, 4), sharex=False, sharey=False, gridspec_kw={'wspace': 0.1})
        custom_cmap = matplotlib.colormaps.get_cmap("jet")

        vmin, vmax = 0, 8
        im1 = ax[0].imshow(self.model.stim_matrix, aspect='auto', cmap=custom_cmap, interpolation='nearest', vmin=vmin,
                           vmax=vmax, origin='lower', extent=[0, 2.5, 0.5, 15.5])
        cbar1 = fig.colorbar(im1, ax=ax[0], orientation="vertical", shrink=0.8, pad=0.02)
        cbar1.set_ticks([1, 4, 7])
        cbar1.set_ticklabels(["1 Hz", "4 Hz", "7 Hz"])
        cbar1.outline.set_edgecolor('black')
        cbar1.outline.set_linewidth(0.5)

        vmin, vmax = 2, 78
        im2 = ax[1].imshow(E_act_mean.T, aspect="auto", cmap=custom_cmap, vmin=vmin, vmax=vmax, origin='lower',
                           interpolation='nearest', extent=[0, 2.5, 0.5, 15.5])
        cbar2 = fig.colorbar(im2, ax=ax[1], orientation="vertical", shrink=0.8, pad=0.02)
        cbar2.set_ticks([20, 60])
        cbar2.set_ticklabels(["20 Hz", "60 Hz"])
        cbar2.outline.set_edgecolor('black')
        cbar2.outline.set_linewidth(0.5)

        plt.show()

    def figure_11(
            self, factor, stim_dur, stim_times,
            act_other_all, act_8_all, act_other_spont, act_8_spont,
            x_8_all, x_other_all, x_8_spont, x_other_spont,
            y_8_all, y_other_all, y_8_spont, y_other_spont
    ):
        time_steps = self.model.params.sim_duration/self.model.params.dt
        time_axes = np.arange(time_steps) * (self.model.params.dt / self.model.params.tau_rec)

        fig, ax = plt.subplots(3, 2, figsize=(12, 10), dpi=300,
                               gridspec_kw={'height_ratios': [2, 1, 1]},
                               constrained_layout=True)

        stim_color = 'red'
        sustained_color = 'blue'

        line_width = 1.5
        stim_bar_alpha = 0.1
        time_range = [time_axes[0], time_axes[-1]]

        ax[0, 0].plot(time_axes, act_other_all, color='grey', linewidth=line_width, linestyle="--")
        ax[0, 0].plot(time_axes, act_8_all, color='black', linewidth=line_width)

        for i, stim in enumerate(stim_times):
            if i == 0:
                ax[0, 0].axvspan(stim, stim + stim_dur, color=stim_color, alpha=stim_bar_alpha,label="Clicks")
            else:
                ax[0, 0].axvspan(stim, stim + stim_dur, color=stim_color, alpha=stim_bar_alpha)
        ax[0, 0].axvspan(1 * factor, 4.5 * factor, color=sustained_color, alpha=stim_bar_alpha,
                         label="Sustained Stimulus")

        ax[0, 0].set_title("Network Activity (All Neurons)", fontsize=14)
        ax[0, 0].set_ylabel("Mean Firing Rate (Hz)")
        ax[0, 0].legend()

        ax[0, 1].plot(time_axes, act_other_spont, color='grey', linewidth=line_width, linestyle="--",
                      label = "All Columns Excluding 8")
        ax[0, 1].plot(time_axes, act_8_spont, color='black', linewidth=line_width,
                      label = "Only Column 8")

        for stim in stim_times:
            ax[0, 1].axvspan(stim, stim + stim_dur, color=stim_color, alpha=stim_bar_alpha)
        ax[0, 1].axvspan(1 * factor, 4.5 * factor, color=sustained_color, alpha=stim_bar_alpha)

        ax[0, 1].set_title("Network Activity (Spontaneous Neurons)", fontsize=14)
        ax[0, 1].legend()

        ax[1, 0].plot(time_axes, x_8_all, color='black', linewidth=line_width,label="x")
        ax[1, 0].plot(time_axes, y_8_all, color='black', linewidth=line_width, linestyle="--",label="y")

        for stim in stim_times:
            ax[1, 0].axvspan(stim, stim + stim_dur, color=stim_color, alpha=stim_bar_alpha)
        ax[1, 0].axvspan(1 * factor, 4.5 * factor, color=sustained_color, alpha=stim_bar_alpha)

        ax[1, 0].set_title("Column 8 Resources (All Neurons)", fontsize=14)
        ax[1, 0].set_ylabel("Resource Fraction")
        ax[1, 0].set_ylim(0.3, 0.7)
        ax[1, 0].legend()

        ax[1, 1].plot(time_axes, x_8_spont, color='black', linewidth=line_width)
        ax[1, 1].plot(time_axes, y_8_spont, color='black', linewidth=line_width, linestyle="--")

        for stim in stim_times:
            ax[1, 1].axvspan(stim, stim + stim_dur, color=stim_color, alpha=stim_bar_alpha)
        ax[1, 1].axvspan(1 * factor, 4.5 * factor, color=sustained_color, alpha=stim_bar_alpha)

        ax[1, 1].set_title("Column 8 Resources (Spontaneous Neurons)", fontsize=14)
        ax[1, 1].set_ylim(0.3, 0.7)

        ax[2, 0].plot(time_axes, x_other_all, color='black', linewidth=line_width)
        ax[2, 0].plot(time_axes, y_other_all, color='black', linewidth=line_width, linestyle="--")

        for stim in stim_times:
            ax[2, 0].axvspan(stim, stim + stim_dur, color=stim_color, alpha=stim_bar_alpha)
        ax[2, 0].axvspan(1 * factor, 4.5 * factor, color=sustained_color, alpha=stim_bar_alpha)

        ax[2, 0].set_title("Other Column Resources (All Neurons)", fontsize=14)
        ax[2, 0].set_ylabel("Resource Fraction")
        ax[2, 0].set_ylim(0.3, 0.7)
        ax[2, 0].set_xlabel("Time (s)")

        ax[2, 1].plot(time_axes, x_other_spont, color='black', linewidth=line_width)
        ax[2, 1].plot(time_axes, y_other_spont, color='black', linewidth=line_width, linestyle="--")

        for stim in stim_times:
            ax[2, 1].axvspan(stim, stim + stim_dur, color=stim_color, alpha=stim_bar_alpha)
        ax[2, 1].axvspan(1 * factor, 4.5 * factor, color=sustained_color, alpha=stim_bar_alpha)

        ax[2, 1].set_title("Other Column Resources (Spontaneous Neurons)", fontsize=14)
        ax[2, 1].set_ylim(0.3, 0.7)
        ax[2, 1].set_xlabel("Time (s)")

        for a in ax.ravel():
            a.set_xlim(time_range)
            a.spines['top'].set_visible(False)
            a.spines['right'].set_visible(False)
            a.grid(True, linestyle="--", alpha=0.5)

        plt.show()
    
    
    def fft_1(self, signal, signal_reconstructed, frequencies,
            fft_signal, fft_reconstructed):
        """
        Create first figure for reproducibility section.
        """
        p = self.params
        
        plt.figure(figsize=(7, 10.5))

        # Original deviation
        plt.subplot(2, 1, 1)
        plt.plot(signal, linestyle='-', color='green', label=r'$e^E$ Random')
        plt.plot(signal_reconstructed, linestyle='--', color='black', label=r'$e^E$ Reconstructed')
        plt.axhline(0, linestyle=':', color='black', alpha=0.3, linewidth=1)
        plt.legend(frameon=False, fontsize=12)
        plt.text(-5, 1.45, 'A', va="bottom", ha="center", fontsize=14)
        plt.xlabel('Neurone Index', fontsize=14)
        plt.ylabel(r'Deviation of $e^E$ from Linear [Hz]', fontsize=14)

        # FFT Spectrum
        plt.subplot(2, 1, 2)
        plt.plot(frequencies[:p.N_E // 2], np.abs(fft_signal)[:p.N_E // 2], 
                 linestyle='-', color='green', label=r'$e^E$ Random')
        plt.plot(frequencies[:p.N_E // 2], np.abs(fft_reconstructed)[:p.N_E // 2],
                 linestyle='--', color='black', label=r'$e^E$ Reconstructed')
        plt.legend(frameon=False, fontsize=12)
        plt.text(-0.025, 53.3, 'B', va="bottom", ha="center", fontsize=14)
        plt.xlabel('Normalised Spatial Frequency', fontsize=14)
        plt.ylabel('FFT Component Magnitude', labelpad=15, fontsize=14)

        plt.tight_layout()
        plt.show()
    
    def fft_2(self, ftc, ftc_linear, ftc_components, y_min, y_max):
        """
        Create second figure for reproducibility section.
        """
        p = self.params
        space = np.arange(p.N_E)
        
        num_components = len(ftc_components)
        fig, axes = plt.subplots(round((num_components + 1) / 2), 2,
                                 figsize=(7, 7), constrained_layout=True)
        axes = axes.flatten()
        
        labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        
        for i, (FTC, freq, comp) in enumerate(ftc_components):
            ax = axes[i]
            ax.plot(ftc_linear, marker='o', linestyle='-', color='red', linewidth=2, label=r'$e^E$ Linear')
            ax.plot(FTC, marker='x', linestyle='--', color='black', linewidth=1, label=f"Freq. {freq:.2f}")
            ax.set_ylim([-1, 10])
            ax.set_xlim([0, 14])
            ax.set_xticks([0, 2, 4, 6, 8, 10, 12, 14])
            ax.set_xticklabels([1, 3, 5, 7, 9, 11, 13, 15])
            ax.legend(loc="lower left", frameon=False, bbox_to_anchor=(-0.03, -0.1), fontsize=12)
            
            if i // 2 != 3:
                ax.tick_params(axis='x', labelbottom=False)
            if i % 2 != 0:
                ax.tick_params(axis='y', labelleft=False)
            
            # Add inset plot of cosine component
            inset_ax = ax.inset_axes([0.63, 0.08, 0.35, 0.35])
            inset_ax.axhline(0, color="gray", linestyle="dashed", linewidth=0.5)
            inset_ax.plot(space, comp, color='blue')
            inset_ax.set_xlim(space[0], space[-1])
            inset_ax.set_ylim(y_min, y_max)
            inset_ax.set_xticks([])
            inset_ax.set_yticks([])
            
            ax.text(0, 10.5, labels[i], va="bottom", ha="center", fontsize=12)
        
        j = i + 1
        ax = axes[j]
        for i, (FTC, marker, style, colour, linewidth, label) in enumerate(ftc):
            plt.plot(FTC, marker=marker, linestyle=style, color=colour,
                     linewidth=linewidth, label=label)
        ax.set_ylim([-1, 10])
        ax.set_xlim([0, 14])
        ax.set_xticks([0, 2, 4, 6, 8, 10, 12, 14])
        ax.set_xticklabels([1, 3, 5, 7, 9, 11, 13, 15])
        ax.legend(loc="lower left", frameon=False, bbox_to_anchor=(-0.03, -0.1), fontsize=12)
        ax.tick_params(axis='y', labelleft=False)
        ax.text(0, 10.5, labels[j], va="bottom", ha="center", fontsize=12)
        
        fig.text(-0.03, 0.5, "Input Amplitude [Hz]", va="center", rotation="vertical", fontsize=14)
        fig.text(0.46, -0.03, "Column Index", va="center", fontsize=14)
        
        plt.show()

    def ssa(self, figure_data):

        # --- Plot --- #
        p = self.params
        fig, ax = plt.subplots(2, 2, figsize=(44, 7.5), gridspec_kw={'width_ratios': [4, 1], 'wspace': 0.15, "hspace": 0.2}, sharex=False, sharey=False, )

        time_axis = np.arange(0, p.sim_duration, p.dt)

        ax[0, 0].plot(time_axis, figure_data["mean_E"], color="black")
        ax[0, 0].set_ylim([-10, 80])
        ax[0, 0].set_xlim([-0.5, 35.5])
        ax[0, 0].set_ylabel("Network Activity (Hz)")
        ax[0, 0].set_xlabel("Time (sec)")

        for i, t in enumerate(figure_data["time_steps"]):
            if(figure_data["stimuli_type"][0][i] == 1):
                ax[0, 0].text(t, -8, ' ', 
                        ha='center', va='bottom', fontsize=8, fontweight='bold', 
                        bbox=dict(facecolor="cornflowerblue", edgecolor='cornflowerblue', boxstyle='square,pad=0.01'))
                
            if(figure_data["stimuli_type"][0][i] == 0):
                ax[0, 0].text(t, -4, ' ', 
                        ha='center', va='bottom', fontsize=8, fontweight='bold', 
                        bbox=dict(facecolor="lightcoral", edgecolor="lightcoral", boxstyle='square,pad=0.01'))

        mean_x = np.array(figure_data["mean_x"])

        im1 = ax[1, 0].imshow(mean_x[:, ::100], vmax=0.7, aspect='auto', cmap=plt.get_cmap("gray_r"))
        
        cbar = fig.colorbar(im1, ax=ax[1, 0], orientation = 'horizontal', location="bottom", shrink=0.5, pad=0.02,)
        cbar.outline.set_edgecolor('black')
        cbar.outline.set_linewidth(0.5)
        ax[1, 0].set_ylim([4, 14])
        ax[1, 0].set_xlim([-5, 355])

        ax[1, 0].set_ylabel("Column Index")
        ax[1, 0].set_xlabel("Time (sec)")
        ax[1, 0].set_xticks([])


        ax[0, 1].plot(np.mean(figure_data["deviant_responses1"], axis=1), color="lightcoral")
        ax[0, 1].plot(np.mean(figure_data["standard_responses1"], axis=1), color="cornflowerblue")

        ax[0, 1].set_ylabel("Average Response Activity")
        ax[0, 1].legend(["f1 - 90%", "f2 - 10%"])

        ax[1, 1].plot(np.mean(figure_data["deviant_responses2"], axis=1), color="lightcoral")
        ax[1, 1].plot(np.mean(figure_data["standard_responses2"], axis=1), color="cornflowerblue")

        ax[1, 1].set_xlabel("Time (ms)")
        ax[1, 1].legend(["f2 - 90%", "f1 - 10%"])

        ax[1, 1].text(25, 1.5, '                                                                   ', 
        ha='center', va='bottom', fontsize=3, fontweight='bold', 
        bbox=dict(facecolor="black", edgecolor='black', boxstyle='square,pad=0.01'))
                
        ax[1, 1].text(25, 3, 'Tone', 
        ha='center', va='bottom', fontsize=8, fontweight='bold', 
        bbox=dict(facecolor="white", edgecolor='white', boxstyle='square,pad=0.01'))
                
        ax[0, 0].spines[['right', 'top']].set_visible(False)
        ax[0, 1].spines[['right', 'top']].set_visible(False)
        ax[1, 0].spines[['right', 'top']].set_visible(False)
        ax[1, 1].spines[['right', 'top']].set_visible(False)
        plt.tight_layout()
        plt.subplots_adjust(wspace=0.3)
        plt.show()

