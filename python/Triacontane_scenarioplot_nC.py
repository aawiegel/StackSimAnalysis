#!/usr/bin/env python3

from scipy import stats
import StackSim

import datetime
import numpy as np
import math
from scipy import interpolate
from xml.dom import minidom
from matplotlib import ticker
from cycler import cycler
import matplotlib.pyplot as plt
import matplotlib.cm as cm
     

# Define file name dictionary for looping

ScenarioFiles = {'Scenario 1' : "tri_109nm_sc1.xml", 'Scenario 1A' : "tri_109nm_sc1a.xml", 'Scenario 2' : 'tri_109nm_sc2.xml', 'Scenario 1A UL' : 'tri_10xevap_109nm_sc1a.xml', 'Scenario 1A LL' : 'tri_tenthevap_109nm_sc1a.xml', 'Scenario 1 atm' : 'tri_109nm_atm_sc1.xml', 'Scenario 1A atm' : 'tri_109nm_atm_sc1a.xml'}

# Define scenario dictionary

Scenarios = {}

# Create lists for finding aggregate species

carbon_min, carbon_max = 1, 30

missing_carbon_no = [1, 30]

#carbon_list = [["C30", 30], ["C30_COOH", 30], ["C30_COOH_O", 30], ["C30_HOOCCOOH", 30], ["C30_O2", 30], ["C30_O", 30]]

carbon_no_dict = {"nC30" : [["C30", 1], ["C30_COOH", 1], ["C30_COOH_O", 1], ["C30_HOOCCOOH", 1], ["C30_O2", 1], ["C30_O", 1]]}

# Initalize list of lists

carbon_list = [["nC30", 30]]

for i in range(carbon_min, carbon_max+1, 1):
    if i in missing_carbon_no:
        pass
    else:
        no_C = "C"+str(i)        
        
        carbon_no_dict["n"+no_C] = [[no_C, 1], [no_C+"_O2", 1], [no_C+"_COOH", 1], [no_C+"_COOH_O", 1], [no_C+"_HOOCCOOH", 1]]
        
        carbon_list.append(["n"+no_C, i])        
        
        #carbon_list.append(["C"+str(i), i])
        #carbon_list.append(["C"+str(i)+"_OC", i])
        #carbon_list.append(["C"+str(i)+"_OH", i])
        #carbon_list.append(["C"+str(i)+"_O2", i])
        #carbon_list.append(["C"+str(i)+"_COOH_O", i])
        #carbon_list.append(["C"+str(i)+"_COOH", i])
        #carbon_list.append(["C"+str(i)+"_HOOCCOOH", i])
        #carbon_list.append(["C"+str(i)+"_R", i])
        #carbon_list.append(["C"+str(i)+"_COOOH", i])

oxygen_list = [["OC_sec", 1], ["OCH_prim", 1], ["OHCH2_prim", 1], ["OHCH_sec", 1], ["OC_alpha", 1], ["OHCH_alpha", 1], ["HO_OOC_prim", 3], ["HOOCH2_prim", 2], ["HOOCH_alpha", 2], ["HOOCH_sec", 2], ["HOOC_prim", 2]]

oxygen_list_2diff = [["OC_sec", 1], ["OCH_prim", 1], ["OHCH2_prim", 1], ["OHCH_sec", 1], ["OC_alpha", 1], ["OHCH_alpha", 1], ["HO_OOC_prim", 3], ["HOOCH2_prim", 2], ["HOOCH_alpha", 2], ["HOOCH_sec", 2], ["HOOC_prim", 2], ["OC_sec_f", 1], ["OCH_prim_f", 1], ["OHCH2_prim_f", 1], ["OHCH_sec_f", 1], ["HOOC_prim_f", 2], ["HO_OOC_prim_f", 3], ["HOOCH2_prim_f", 2], ["HOOCH_sec_f", 2]]

hydrogen_list = [["CH3_prim", 3], ["CH3_prim_s", 3], ["CH2_sec", 2], ["CH2_alpha", 2], ["OCH_prim", 1], ["OHCH_sec", 2], ["OHCH2_prim", 3], ["OHCH_alpha", 2], ["HO_OOC_prim", 1], ["HOOCH2_prim", 3], ["HOOCH_alpha", 2], ["HOOCH_sec", 2], ["HOOC_prim", 1]]

hydrogen_list_2diff = [["CH3_prim", 3], ["CH3_prim_s", 3], ["CH3_prim_f", 3], ["CH2_sec", 2], ["CH2_sec_f", 2], ["CH2_alpha", 2], ["OCH_prim", 1], ["OCH_prim_f", 1], ["OHCH_sec", 2], ["OHCH_sec_f", 2], ["OHCH2_prim", 3], ["OHCH2_prim_f", 3], ["OHCH_alpha", 2], ["HO_OOC_prim", 1], ["HO_OOC_prim_f", 1], ["HOOCH2_prim", 3], ["HOOCH2_prim_f", 3], ["HOOCH_alpha", 2], ["HOOCH_sec", 2], ["HOOCH_sec_f", 2], ["HOOC_prim", 1], ["HOOC_prim_f", 1]]
        
mass_list = [["carbon", 12], ["oxygen", 16], ["hydrogen", 1]]

mass_list_r = [["carbon_r", 12], ["oxygen_r", 16], ["hydrogen_r", 1]]

# Calculate aggregate species and radial corrections for each simulation

for scenario in ScenarioFiles.keys():
    
    # Load and process simulation data from simulation    
    Scenarios[scenario] = StackSim.SimulationData(ScenarioFiles[scenario])
    
    # Calculate aggregate carbon species and radial correction
    for carbon_no in carbon_no_dict.keys():
        Scenarios[scenario].calcAggregateSpecies(carbon_no, carbon_no_dict[carbon_no])
        Scenarios[scenario].calcRadialCorrection(carbon_no, reverse_axis=True)
    

    # Calculate each element and mass    
    Scenarios[scenario].calcAggregateSpecies("carbon", carbon_list)

    Scenarios[scenario].calcAggregateSpecies("oxygen", oxygen_list)

    Scenarios[scenario].calcAggregateSpecies("hydrogen", hydrogen_list)     
    
    Scenarios[scenario].calcAggregateSpecies("mass", mass_list)
    
    # Calculate radial correction for each element and mass    
    
    Scenarios[scenario].calcRadialCorrection("mass", reverse_axis=True)
    Scenarios[scenario].calcRadialCorrection("oxygen", reverse_axis=True)
    Scenarios[scenario].calcRadialCorrection("carbon", reverse_axis=True)
    Scenarios[scenario].calcRadialCorrection("hydrogen", reverse_axis=True)
    
    # Calculate radial correction for triacontane    
    
    Scenarios[scenario].calcRadialCorrection("Tri", reverse_axis=True)
    
    # Calculate mass of aerosol    
    
    Scenarios[scenario].calcAggregateSpecies("mass_r", mass_list_r)
    
    Scenarios[scenario].calcSpeciesRatio("O/C ratio", "oxygen_r", "carbon_r")
    Scenarios[scenario].calcSpeciesRatio("H/C ratio", "hydrogen_r", "carbon_r")
    
    Scenarios[scenario].calcContourInterpolated("O/C ratio", reverse_axis = True)
    Scenarios[scenario].calcContourInterpolated("H/C ratio", reverse_axis = True)
    

# Utility function
        
#def getDepthProfile(scenario, position, contour, time_slice, depth_slice=5E-7, reverse_axis=True):
#    """ Generates sum of a species 'data' at a certain depth profile 
#        from a contour map, time_slice, and depth_slice.
#        ContourMap of data must be generated first.
#    """
#    
#    # Find closest index to time slice        
#    time_i = (np.abs(scenario.time-time_slice)).argmin()
#        
#    # Find position of top compartment
#    if(reverse_axis):
#        max_position = scenario.compartments[(0, scenario.num_rows-1, 0)].positions["y"][time_i]
#    else:
#        max_position = scenario.compartments[(0, 0, 0)].positions["y"][time_i]
#         
#    min_position = max_position - depth_slice
#    
#    # Find closest index to min and max position
#    max_pos_i = (np.abs(position - max_position)).argmin()
#    min_pos_i = (np.abs(position - min_position)).argmin()
#    
#   return np.sum(contour[min_pos_i:max_pos_i])