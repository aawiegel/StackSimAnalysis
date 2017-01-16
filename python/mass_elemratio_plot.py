# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 10:51:30 2016
Run Triacontane_scenarioplot.py first!!
@author: Aaron
"""

import seaborn as sns
from matplotlib import container
from cycler import cycler
import natsort

sns.set_context("paper")
sns.set_style("white")   
sns.set_style("ticks")

# Adjust for lifetime, OH exposure, etc.
time_factor = (2.5E11, r'OH exposure (molecules cm$\mathregular{^{-3}}$ s)')
time_slice = 30


    
sns.set_color_codes()


# Set Parameters for figures



#t_expt = np.array([0, 0.37, 0.75, 1.17, 1.72, 2.08, 3.23, 4.59, 5.47, 6.26, 6.90, 8.08, 9.81, 11.05])
#t_expt = np.array([0, 3.07E11, 6.33E11, 9.89E11, 1.45E12, 1.75E12, 2.72E12, 3.86E12, 4.61E12, 5.27E12, 5.80E12, 6.80E12, 8.26E12, 9.30E12])
t_expt = np.array([0, 3.06E11, 6.30E11, 9.84E11, 1.44E12, 1.75E12, 2.70E12, 3.84E12, 4.59E12, 5.24E12, 5.78E12, 6.77E12, 8.22E12, 9.26E12])
#carbon_expt = np.array([30., 29.93, 27.90, 24.12, 23.71, 23.30, 21.20, 18.74, 18.00, 17.50, 16.01, 15.14, 14.20, 13.62])
#carbon_expt = np.array([30, 29.9498, 26.6332, 24.0254, 23.573, 23.0582, 20.556, 17.4048, 16.305, 15.5206, 13.997, 12.9218, 11.8532, 11.2517])
carbon_expt = np.array([30, 29.949, 27.656, 26.785, 26.668, 26.395, 23.714, 20.234, 19.155, 19.118, 16.361, 15.251, 14.215, 13.482])
#carbon_expt = np.array([30, 29.93, 27.90, 26.77, 26.32, 25.86, 23.53, 20.80, 19.97, 19.43, 17.78, 16.8, 15.76, 15.12])
carbon_err = carbon_expt*0.1
#oxygen_expt = np.array([0, 0.69, 1.32, 3.24, 4.05, 4.63, 6.12, 7.15, 7.48, 7.8, 7.53, 7.48, 7.41, 7.34])
#oxygen_expt = np.array([0, 0.486, 2.433, 3.173, 4.031, 4.696, 6.526, 8.101, 8.717, 9.263, 9.021, 9.135, 9.166, 9.106])
oxygen_expt = np.array([0, 0.486, 2.527, 3.537, 4.560, 5.376, 7.528, 9.417, 10.241, 11.409, 10.545, 10.781, 10.992, 10.911])
#oxygen_expt = np.array([0, 0.69, 1.32, 3.59, 4.50, 5.14, 6.80, 7.94, 8.30, 8.66, 8.36, 8.31, 8.23, 8.15])
oxygen_err = oxygen_expt*0.2
#hydrogen_expt = np.array([62, 62, 56.5, 44.61, 42.2, 40.27, 33.27, 26.66, 24.68, 23.17, 20.52, 18.80, 16.97, 15.83])
#hydrogen_expt = np.array([63.18, 62.19, 51.08, 44.06, 41.54, 39.35, 31.93, 24.99, 22.69, 21.06, 18.62, 16.73, 14.96, 14.00])
hydrogen_expt = np.array([63.18, 62.19, 53.04, 49.12, 46.99, 45.05, 36.84, 29.06, 26.65, 25.94, 21.77, 19.74, 17.94, 16.77])
#hydrogen_expt = np.array([63.09, 62.11, 56.49, 49.51, 46.84, 44.70, 36.93, 29.60, 27.40, 25.72, 22.78, 20.87, 18.87, 17.57])
hydrogen_err = hydrogen_expt*0.1
mass_expt_uncorr = np.array([1, 1.01, 0.97, 0.90, 0.92, 0.92, 0.90, 0.86, 0.84, 0.84, 0.78, 0.75, 0.72, 0.70])
#mass_expt = np.array([1, 1.011, 0.951, 0.885, 0.893, 0.895, 0.868, 0.818, 0.805, 0.799, 0.744, 0.715, 0.685, 0.644])
mass_expt = np.array([1, 1.02, 1.01, 1.01, 1.04, 1.06, 1.05, 1.00, 1.00, 1.04, 0.92, 0.89, 0.86, 0.84])
#mass_expt = np.array([1, 1.046, 0.864, 0.910, 0.938, 0.954, 0.942, 0.901, 0.896, 0.933, 0.824, 0.800, 0.777, 0.753])
#mass_expt = np.array([1, 1.046, 1.069, 1.127, 1.160, 1.181, 1.165, 1.114, 1.109, 1.155, 1.020, 0.990, 0.961, 0.931])
mass_err = mass_expt*0.1
#volume_expt = np.array([1, 0.99, 0.75, 0.64, 0.61, 0.59, 0.53, 0.47, 0.44, 0.46, 0.40, 0.38, 0.37, 0.35])
volume_expt = np.array([1, 0.965, 0.872, 0.708, 0.674, 0.659, 0.585, 0.517, 0.495, 0.508, 0.443, 0.424, 0.412, 0.394])
volume_ellipsoid_expt = np.array([1, 1, 0.91, 0.90, 0.86, 0.84, 0.75, 0.66, 0.63, 0.65, 0.57, 0.54, 0.53, 0.50])
density_expt = np.array([0.728, 0.768, 0.842, 1.040, 1.126, 1.172, 1.302, 1.410, 1.467, 1.486, 1.506, 1.526, 1.526, 1.547])
HC_ratio_expt = np.array([2.1, 2.077, 1.918, 1.834, 1.762, 1.707, 1.553, 1.436, 1.391, 1.357, 1.331, 1.295, 1.262, 1.244])
#HC_ratio_expt = np.array([2.10, 2.08, 1.91, 1.83, 1.76, 1.71, 1.55, 1.44, 1.39, 1.36, 1.33, 1.29, 1.26, 1.24])
HC_ratio_err = HC_ratio_expt*0.1
OC_ratio_expt = np.array([0, 0.016, 0.091, 0.132, 0.171, 0.204, 0.317, 0.465, 0.535, 0.597, 0.645, 0.707, 0.773, 0.809])
#OC_ratio_expt = np.array([0, 0.016, 0.091, 0.132, 0.171, 0.204, 0.317, 0.465, 0.535, 0.597, 0.645, 0.707, 0.773, 0.809])
OC_ratio_err = OC_ratio_expt*0.1
radius_expt = np.array([56.6, 56.45, 51.35, 48.7, 47.9, 47.55, 45.7, 43.85, 43.2, 43.6, 41.65, 41.05, 40.65, 40.06])
radius_corr_expt = np.array([54.6, 54, 52.2, 48.7, 47.9, 47.55, 45.7, 43.85, 43.2, 43.6, 41.65, 41.05, 40.65, 40.06])
#radius_expt = np.array([51, 51, 51.35, 48.7, 47.9, 47.55, 45.7, 43.85, 43.2, 43.6, 41.65, 41.05, 40.65, 40.05])

ElementData = {'oxygen' : oxygen_expt, 'hydrogen' : hydrogen_expt, 'carbon' : carbon_expt}

ScenarioList1 = ["Scenario 1", "Scenario 2"]



linecycle = cycler('linestyle', ['-', '--', '-.', ':'])
linecycle2 = cycler('linestyle', ['-', '-', '-', '--', '--', '--', '-.', '-.', ':', ':'])

def plotScenariosMassElemRatio(ScenarioList, save_fig=''):

    fig, axarr = plt.subplots(2, sharex=True)

    fig.set_figwidth(8.7/2.54)
    fig.set_dpi(600)


    
    axarr[0].errorbar(t_expt, mass_expt_uncorr, yerr=mass_err, fmt='*g', label='Uncorrected', capthick=1)
    axarr[0].errorbar(t_expt, mass_expt, yerr=mass_err, fmt='om', label='Corrected', capthick=1)
    axarr[1].errorbar(t_expt, HC_ratio_expt, yerr=HC_ratio_err, fmt='vb', label='H/C ratio', capthick=1)
    axarr[1].errorbar(t_expt, OC_ratio_expt, yerr=OC_ratio_err, fmt='^r', label='O/C ratio', capthick=1)
    axarr[0].set_prop_cycle(linecycle)
    axarr[1].set_prop_cycle(linecycle2)
    for scenario in natsort.natsorted(ScenarioList):
        mass_r = Scenarios[scenario].species['mass_r']
        mass_r = mass_r/mass_r[0]
        axarr[0].plot(Scenarios[scenario].time*time_factor[0], mass_r, label=scenario, color='m')
                
        axarr[1].plot(Scenarios[scenario].time*time_factor[0], Scenarios[scenario].species["H/C ratio"], color='b')
        axarr[1].plot(Scenarios[scenario].time*time_factor[0], Scenarios[scenario].species["O/C ratio"], color='r')
    
    fig.tight_layout()
    fig.subplots_adjust(wspace=0, hspace=0)
    
    axarr[0].set_xlim([-0.5E12, 1E13])
    axarr[0].set_ylim([0, 1.2])
    axarr[1].set_ylim([-0.1, 2.39])
    
    axarr[0].yaxis.set_major_locator(ticker.MaxNLocator(7))
    axarr[1].yaxis.set_major_locator(ticker.MaxNLocator(10))
    axarr[1].xaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
    
    axarr[0].text(0.93E13, 1.05, 'A')
    axarr[1].text(0.93E13, 2.1, 'B')
    
    axarr[1].set_xlabel(time_factor[1])
    axarr[0].set_ylabel('Mass (normalized)')
    axarr[1].set_ylabel('Elemental ratio')
    
    handles, labels = axarr[0].get_legend_handles_labels()
    handles = [h[0] if isinstance(h, container.ErrorbarContainer) else h for h in handles]
    
    axarr[0].legend(handles, labels, loc='lower left')
    
    handles, labels = axarr[1].get_legend_handles_labels()
    handles = [h[0] if isinstance(h, container.ErrorbarContainer) else h for h in handles]
    
    axarr[1].legend(handles, labels, loc='center left')
    
    if(save_fig):
        plt.savefig(save_fig+'.tif', format='tif', dpi=600, bbox_inches='tight')
    
    plt.show()

def plotScenariosElem(ScenarioList, save_fig=''):
    
    fig, axarr = plt.subplots(3, sharex=True)
    
    fig.set_figwidth(8.7/2.54)
    fig.set_dpi(600)
    
    axarr[0].errorbar(t_expt, hydrogen_expt, yerr=hydrogen_err, fmt='vb', label='Experiment', capthick=1)
    axarr[1].errorbar(t_expt, carbon_expt, yerr=carbon_err, fmt='ok', label='Experiment', capthick=1)
    axarr[2].errorbar(t_expt, oxygen_expt, yerr=oxygen_err, fmt='^r', label='Experiment', capthick=1)
    
    fig.tight_layout()
    fig.subplots_adjust(wspace=0, hspace=0)   
    
    for ax in axarr:
        ax.set_prop_cycle(linecycle)
        
    for scenario in natsort.natsorted(ScenarioList):
        
        oxygen_r = Scenarios[scenario].species['oxygen_r']
        carbon_r = Scenarios[scenario].species['carbon_r']
        hydrogen_r = Scenarios[scenario].species['hydrogen_r']
        
        init_c = carbon_r[0]
        carbon_r = carbon_r/init_c*30
        oxygen_r = oxygen_r/init_c*30
        hydrogen_r = hydrogen_r/init_c*30
        
        time = Scenarios[scenario].time*time_factor[0]
        
        axarr[0].plot(time, hydrogen_r, color='b', label=scenario)
        axarr[1].plot(time, carbon_r, color='k', label=scenario)
        axarr[2].plot(time, oxygen_r, color='r', label=scenario)
    
    axarr[0].set_xlim([-0.5E12, 1E13])
    axarr[1].xaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
    
    axarr[0].set_ylim([0, 69.8])
    axarr[0].yaxis.set_major_locator(ticker.MaxNLocator(7))
    
    axarr[1].set_ylim([0, 34.8])
    axarr[1].yaxis.set_major_locator(ticker.MaxNLocator(7))
    
    axarr[2].set_ylim([0, 15.8])
    axarr[2].yaxis.set_major_locator(ticker.MaxNLocator(8))
    
    axarr[0].text(0.93E13, 60, 'A')
    axarr[1].text(0.93E13, 30, 'B')
    axarr[2].text(0.93E13, 14, 'C')
    
    axarr[2].set_xlabel(time_factor[1])
    
    axarr[0].set_ylabel('Average Hydrogen')
    axarr[1].set_ylabel('Average Carbon')
    axarr[2].set_ylabel('Average Oxygen')
    
    for ax in axarr:    
        handles, labels = ax.get_legend_handles_labels()
        handles = [h[0] if isinstance(h, container.ErrorbarContainer) else h for h in handles]
        ax.legend(handles, labels, loc='lower left')

    axarr[2].legend(loc = 'upper left')
    
    if(save_fig):
        plt.savefig(save_fig+'.tif', format='tif', dpi=600, bbox_inches='tight')    
    
    plt.show()

plotScenariosMassElemRatio(ScenarioList1)#, save_fig='sc1and2_mass_elemratio_comp')

plotScenariosElem(ScenarioList1, save_fig='sc1and2_elem_comp')