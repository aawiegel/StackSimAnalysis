# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 10:51:30 2016
Run Triacontane_scenarioplot_nC.py first!!
@author: Aaron
"""

import seaborn as sns
from matplotlib import container
from cycler import cycler

sns.set_context("talk")
sns.set_style("white")   
sns.set(style="ticks", font_scale=1.5)


# Adjust for lifetime, OH exposure, etc.
time_factor = (2.5E11, r'OH exposure (molecules cm$\mathregular{^{-3}}$ s)')
time_slice = 30


    
sns.set_color_codes()



Scenario = "Scenario 1"
data = "O/C ratio"
time_slice = 2E12/2.5E11

pos_factor = (1E7, 'nm')

linecycle = cycler('linestyle', ['-', '-.', '--', ':'])
colorcycle = cycler('color', ['b', 'm', 'k', 'r'])
linecycle2 = cycler('linestyle', ['-.', '-.', '-', '-', '--', '--'])

def plotContourMap(Scenario, data, save_fig=''):

    
    Simulation = Scenarios[Scenario]
    
    Simulation.calcContourInterpolated(data, reverse_axis=True)
    
    position = Simulation.position_int
    contour = Simulation.species_contour[data]    
    
    fig, axarr = plt.subplots(1)

    #fig.set_figwidth(8.7/2.54)
    fig.set_dpi(600)
      
    levels = np.linspace( 0, 0.7, num=71)
    
    
    cf = axarr.contourf(Simulation.time*time_factor[0], position*pos_factor[0], contour, cmap='inferno', levels=levels)
    
    
    
    axarr.set_xlabel(time_factor[1])
    axarr.set_ylabel('distance from center of particle ('+pos_factor[1]+')')
    
    
    
    
    
    
    axarr.yaxis.set_major_locator(ticker.MaxNLocator(6))
    axarr.xaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True, useOffset=False))
    
    axarr.get_xaxis().get_offset_text().set_x(1.1)
    
    cb = fig.colorbar(cf, ax=axarr, ticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7])

    cb.set_label(data)
    

    
    
    
    if(save_fig):
        plt.savefig(save_fig+'.tif', format='tif', dpi=600, bbox_inches='tight')
    
    plt.show()

plotContourMap(Scenario, data)#, save_fig='OC_ratio_contour_sc1_presentaiton')
