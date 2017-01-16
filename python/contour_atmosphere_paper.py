# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 10:51:30 2016
Run Triacontane_scenarioplot.py first!!
@author: Aaron
"""

import seaborn as sns
from matplotlib import container
from cycler import cycler

sns.set_context("paper")
sns.set_style("white")   
sns.set_style("ticks")

# Adjust for lifetime, OH exposure, etc.
time_factor = (5E6, r'OH exposure (molecules cm$\mathregular{^{-3}}$ s)')
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
#mass_expt = np.array([1, 1.01, 0.97, 0.90, 0.92, 0.92, 0.90, 0.86, 0.84, 0.84, 0.78, 0.75, 0.72, 0.70])
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

#ScenarioList1 = ["Scenario 1", "Scenario 2"]
#ScenarioList2 = ["Scenario 1", "Scenario 1A", "Scenario 2A"]



Scenario = "Scenario 1A atm"
data = "O/C ratio"
time_slice = 6*3600

pos_factor = (1E7, 'nm')

linecycle = cycler('linestyle', ['-', '-.', '--', ':'])
colorcycle = cycler('color', ['b', 'm', 'k', 'r'])
linecycle2 = cycler('linestyle', ['-.', '-.', '-', '-', '--', '--'])

def plotContourMap(Scenario, data, save_fig=''):
#axarr[0].set_aspect(aspect='equal', adjustable='box-forced')
#axarr[1].set_aspect(aspect='equal', adjustable='box-forced')
    
    Simulation = Scenarios[Scenario]
    
    position = Simulation.position_int
    contour = Simulation.species_contour[data]
    
        
    
    fig, axarr = plt.subplots(2)

    fig.set_figwidth(8.7/2.54)
    fig.set_dpi(600)
      
    levels = np.linspace( 0, 1, num=1001)
    #levels = np.linspace( 0, 2.2, num=2201)
    
    mirrorax = axarr[0].twiny()
    cf = axarr[0].contourf(Simulation.time*time_factor[0], position*pos_factor[0], contour, cmap='inferno', levels=levels)
    
    mirrorax.plot(np.array([time_slice, time_slice])/3600/24, np.array([position[0], position[-1]])*pos_factor[0], '--w', lw=2)
    mirrorax.set_xlabel('Time (days)')
    mirrorax.set_ylim([0, 54])
    mirrorax.set_xlim([0, Simulation.time[-1]/3600/24])    
    
    axarr[0].plot(np.array([time_slice, time_slice])*time_factor[0], np.array([position[0], position[-1]])*pos_factor[0], '--w', lw=2)
    
    axarr[0].set_xlabel(time_factor[1])
    axarr[0].set_ylabel('distance from center of particle ('+pos_factor[1]+')')
    
    fig.tight_layout()
    
    
    
    
    axarr[0].yaxis.set_major_locator(ticker.MaxNLocator(6))
    axarr[0].xaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True, useOffset=False))
    
    axarr[0].get_xaxis().get_offset_text().set_x(1.1)
    
    cb = fig.colorbar(cf, ax=axarr[0], ticks=[0, 0.2, 0.4, 0.6, 0.8, 1])
    #cb = fig.colorbar(cf, ax=axarr[0], ticks=[0, 0.4, 0.8, 1.2, 1.6, 2.0])
    cb.set_label(data)
    
    # Finds index of time closest to time slice
    index = (np.abs(Simulation.time-time_slice)).argmin()
    
    print(Simulation.time[index]*time_factor[0])
    
    average = Simulation.species[data][index]
    average = np.array([average, average])
    dummy_pos = np.array([0, 60])
    
    
    
    axarr[1].plot(position*pos_factor[0], contour[:, index], '-r')
    axarr[1].plot(dummy_pos, average, '--k', label='Average')
    axarr[1].legend(loc='best')
    axarr[1].set_xlabel('distance from center of particle ('+pos_factor[1]+')')
    axarr[1].set_ylabel(data)
    axarr[1].set_ylim([0, 1])
    
    axarr[0].text(0.25E12, 45, 'A', color='w')
    axarr[1].text(3, 0.7, 'B')
    
    cb2 = fig.colorbar(cf, ax=axarr[1], ticks=[0, 0.2, 0.3])
    cb2.ax.set_visible(False)
    cb3 = fig.colorbar(cf, ax=mirrorax, ticks=[1,2])
    cb3.ax.set_visible(False)
    
    if(save_fig):
        plt.savefig(save_fig+'.tif', format='tif', dpi=600, bbox_inches='tight')
    
    plt.show()

plotContourMap(Scenario, data)#, save_fig='OC_ratio_contour_sc1atm')

#ax.plot(t, C, '-k', t, O, '-r', t, H, '-b')
#ax.plot(t, C_r, '-k', t, O_r, '-r', t, H_r, '-b')
#ax.plot(t_expt, hydrogen_expt, 'vb', label='Hydrogen')
#ax.plot(t_expt, carbon_expt, 'ok', label='Carbon')
#ax.plot(t_expt, oxygen_expt, '^r', label='Oxygen')
#ax.errorbar(t_expt, hydrogen_expt, hydrogen_err, fmt='vb', label='Hydrogen')
#ax.errorbar(t_expt, carbon_expt, carbon_err, fmt='ok',  label='Carbon')
#ax.errorbar(t_expt, oxygen_expt, oxygen_err, fmt='^r', label='Oxygen')
#plt.xlabel(r'OH exposure (molecules cm$^{-3}$ s)')

#plt.ylabel('Average elemental composition')
#plt.legend()
#plt.savefig("tri_average_elem_"+str(datetime.date.today())+".png", format='png', dpi=300)
#plt.show()