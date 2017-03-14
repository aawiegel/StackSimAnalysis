# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 10:38:10 2017

@author: Aaron
"""

import os
import zipfile

import StackSim
import numpy as np
import pandas as pd
from matplotlib import ticker
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib as mpl
import re
import natsort

# Create subdirectories for data if they do not exist

subdir = os.path.join(os.path.curdir, "difdata")

if not os.path.isdir(subdir):
    os.mkdir(subdir)
    
out_subdir = os.path.join(os.path.curdir, "dif_summary")
 
if not os.path.isdir(out_subdir):
    os.mkdir(out_subdir)


# Unzip XML files (.zip file available on Github repository)

with zipfile.ZipFile("diffusion series.zip", "r") as zip_ref:
    zip_ref.extractall(subdir)
    

diffusion = ["D15", "D16", "D17", "D18", "SC"]
condition = ["ft", "cfstr", "day"]

# Generate filename strings

files = dict()

for cond in condition:
    for coefficient in diffusion:
        filename = "tri_"+cond+"_"+coefficient+".xml"
        files[cond+"_"+coefficient] = filename

# Additional conditions for flow tube and CFSTR
files["ft_D11"] = "tri_ft_D11.xml"
files["ft_D12"] = "tri_ft_D12.xml"
files["ft_D13"] = "tri_ft_D13.xml"
files["ft_D14"] = "tri_ft_D14.xml"
files["cfstr_D13"] = "tri_cfstr_D13.xml"
files["cfstr_D14"] = "tri_cfstr_D14.xml"

# Diffusion dictionary

D_string_conv = {"SC" : "Instantaneous", "D11" : 1E-11, "D12" : 1E-12, "D13" : 1E-13,
                "D14" : 1E-14, "D15" : 1E-15, "D16" : 1E-16,
                "D17" : 1E-17, "D18" : 8.39E-19}

# Convenience function - see StackSim.py or Postprocessing.ipynb for details on how the simulation data is processed.

Scenarios = StackSim.ProcessTriSimulation(files, subdir)

# Create empty dictionary to hold scenario data frames and panels
ScenarioData = dict()

Scenarios["ft_D11"].calcContourInterpolated("Tri", reverse_axis = True)
position_vector = Scenarios["ft_D11"].position_int


# Set up color map levels

N_levels = 26
  
levels = np.array([0])
levels = np.append(levels, np.logspace(-4, 0, num=N_levels, base = np.e))
labels = np.logspace(-4, 0, num=6, base = 10)
    
cmap = mpl.cm.get_cmap('inferno', N_levels)
    
norm = mpl.colors.BoundaryNorm(levels, cmap.N)

# create data frames and panels for each scenario

for scenario in natsort.natsorted(files.keys()):
    # Create reference to current simulation to save on typing
    simulation = Scenarios[scenario]
    
    # Find OH exposure
    if "ft" in scenario:
        OH = 5.04E10
    elif "cfstr" in scenario:
        OH = 5.04E8
    elif "day" in scenario:
        OH = 5E6
    else:
        OH = 1E5
    
    OH_exp = OH*simulation.time
    
    # Initialize data frame with OH exposure
    SimData = pd.DataFrame({"OH exposure" : OH_exp})
        
    # Find diameter of particle using length of stack.
    # If a single compartment simulation, use the volume of the compartment instead.
    if not "SC" in scenario:
        last_cmpt = simulation.compartments[(0, simulation.num_rows-1, 0)]
        diameter = 2*(last_cmpt.positions["y"]+last_cmpt.dimensions["y"])/1E-7
        stack_vs_sphere = 1
        
        # Calculate contour maps for each species
        simulation.calcContourInterpolated("Tri", reverse_axis = True)
        simulation.calcContourInterpolated("OO_sec", reverse_axis = True)
        simulation.calcContourInterpolated("O/C ratio", reverse_axis = True)

        # Place data into panel

        contour_data = {"Triacontane (normalized)": 
                        simulation.species_contour["Tri"]/simulation.species_contour["Tri"][0,0],
                       "Peroxy radicals": simulation.species_contour["OO_sec"],
                       "O/C ratio": simulation.species_contour["O/C ratio"]}
    else:
        volume = simulation.compartments[(0,0,0)].volume
        diameter = 2*(volume*3/4/np.pi)**(1/3)/1E-7
        stack_vs_sphere = (1.31668E-6**2*2E-5)/volume
        
        # Create dummy contour maps
        Tri = np.empty((position_vector.size, OH_exp.size))
        Peroxy = np.random.binomial(1, 0.025, size=Tri.shape)
        OC_ratio = np.empty_like(Tri)
        for i in range(0, OH_exp.size):
            Tri[:, i] = simulation.species["Tri"][i]/simulation.species["Tri"][0]
            OC_ratio[:, i] = simulation.species["O/C ratio"][i]
            
        contour_data = {"Triacontane (normalized)" : Tri,
                       "Peroxy radicals" : Peroxy,
                       "O/C ratio" : OC_ratio}


    ScenarioData[scenario+" contours"] = pd.Panel(contour_data, 
                                                  major_axis = position_vector,
                                                 minor_axis = OH_exp)
    
    # Find initial mass and carbon amount to normalize quantities
    tri_init = simulation.species["Tri_r"][0]
    mass_init = simulation.species["mass_r"][0]
    carbon_init = simulation.species["carbon_r"][0]
    
    # Find total of functional groups
    alcohols = simulation.species["OHCH2_prim"] + simulation.species["OHCH_alpha"] + \
                    simulation.species["OHCH_sec"]
    ketones = simulation.species["OC_sec"] + simulation.species["OC_alpha"]
    
    
    # Add average data to data frame
    new_data = {"Triacontane (normalized)" : simulation.species["Tri_r"]/tri_init,
                "Mass (normalized)" : simulation.species["mass_r"]/mass_init,
                "Diameter (nm)" : diameter, 
                "Average Hydrogen" : simulation.species["hydrogen_r"]/carbon_init*30, 
                "Average Carbon" : simulation.species["carbon_r"]/carbon_init*30, 
                "Average Oxygen" : simulation.species["oxygen_r"]/carbon_init*30, 
                "H/C ratio" : simulation.species["H/C ratio"], 
                "O/C ratio" : simulation.species["O/C ratio"],
                "Alcohols" : alcohols*stack_vs_sphere,
                "Ketones" : ketones*stack_vs_sphere,
                "Aldehydes" : simulation.species["OCH_prim"]*stack_vs_sphere,
                "Carboxyllic acids" : simulation.species["HOOC_prim"]*stack_vs_sphere}

    SimData = SimData.assign(**new_data)
    
    # Generate carbon list
    
    carbon_list = ["nC"+str(i) for i in range(2, 31)]
    
    # Add carbon number data to data frame
    for carbon in carbon_list:
        carbondata = {carbon : simulation.species[carbon+"_r"]}
        SimData = SimData.assign(**carbondata)

    # Find rate coefficient and uptake coefficient for equivalent
    # of 12 hours of daytime atmospheric oxidation
    
    index = (np.abs(OH_exp-5E6*12*3600)).argmin()
    
    regress = stats.linregress(x = OH_exp[0:index],
                               y=SimData["Triacontane (normalized)"][0:index])
    
    k_het = -1*regress[0]
    eff_uptake = 2*k_het*(200*1E-7)*0.81*6.02E23/3/6.092E4/422
    
    ScenarioData[scenario+" averages"] = SimData
    

    
    writer = pd.ExcelWriter(os.path.join(out_subdir, scenario+".xlsx"),
                            engine='xlsxwriter')
    workbook = writer.book
    
    # Add a sheet that summarizes the model
    summary = workbook.add_worksheet("model summary")
    
    # Summarize files
    summary.write('A1', scenario)
    summary.write('A2', simulation.sim_file)
    summary.write('B1', 'XML file')
    summary.write('B2', files[scenario])
    
    # Write compartment dimensions
    comp = simulation.compartments[(0,0,0)]
    
    summary.write('C1', 'x (cm)')
    summary.write('C2', comp.dimensions["x"][0])
    summary.write('D1', 'y (cm)')
    summary.write('D2', comp.dimensions["y"][0])
    summary.write('E1', 'z (cm)')
    summary.write('E2', comp.dimensions["z"][0])
    
    # Write initial diameter
    summary.write('F1', 'Initial diameter (nm)')
    summary.write('F2', diameter[0])
    
    # Write OH concentration
    
    summary.write('G1', 'OH concentration (molecules cm-3)')
    summary.write('G2', OH)
    
    # Write diffusion coefficient
    
    D = scenario.split("_")[1]
    D = D_string_conv[D]
    
    summary.write('H1', 'Diffusion coefficient (cm2 s-1)')
    summary.write('H2', D)
    
    # Write rate coefficient and uptake coefficient
    summary.write('I1', 'Rate coefficient (cm3 molecules-1 s-1)')
    summary.write('I2', k_het)
    summary.write('J1', 'Effective Uptake')
    summary.write('J2', eff_uptake)
    
    # Write average and contour data to separate sheets
    ScenarioData[scenario+" averages"].to_excel(writer, sheet_name='average data')
    for species, data in ScenarioData[scenario+" contours"].iteritems():
        sheet_name = re.sub("/", " to ", species)
        data.to_excel(writer, sheet_name=sheet_name, 
                      index_label="Distance from center (cm)", startrow=1)
        
        worksheet = writer.sheets[sheet_name]
        worksheet.write(0, 1, "OH exposure (molecules cm-3 s) ->")
    
    # Close writer and save output to excel
    writer.save()
    
    