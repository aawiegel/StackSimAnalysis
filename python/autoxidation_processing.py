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

subdir = os.path.join(os.path.curdir, "autodata")

if not os.path.isdir(subdir):
    os.mkdir(subdir)
    
out_subdir = os.path.join(os.path.curdir, "auto_summary")
 
if not os.path.isdir(out_subdir):
    os.mkdir(out_subdir)


# Unzip XML files (.zip file available on Github repository)

with zipfile.ZipFile("daynight.zip", "r") as zip_ref:
    zip_ref.extractall(subdir)
    

diffusion = ["D15", "D16", "D17", "D18", "SC"]
condition = ["day", "night", "diurnal"]

# Generate filename strings

files = dict()

for cond in condition:
    for coefficient in diffusion:
        
        
        filename = "tri_"+cond+"_"+coefficient+".xml"
        files[cond+"_"+coefficient] = filename
                
        filename_ao = "tri_"+cond+"_ao_"+coefficient+".xml"
        files[cond+"_"+coefficient+"_ao"] = filename_ao

files["night_D14_ao"] = "tri_night_ao_D14.xml"

# Diffusion dictionary

D_string_conv = {"SC" : "Instantaneous", "D14" : 1E-14, "D15" : 1E-15, "D16" : 1E-16,
                "D17" : 1E-17, "D18" : 8.39E-19}

# Convenience function - see StackSim.py or Postprocessing.ipynb for details on how the simulation data is processed.

Scenarios = StackSim.ProcessTriSimulation(files, subdir)

# Create empty dictionary to hold scenario data frames and panels
ScenarioData = dict()

Scenarios["day_D18"].calcContourInterpolated("Tri", reverse_axis = True)
position_vector = Scenarios["day_D18"].position_int


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
    if "day" in scenario:
        OH = 5E6
        OH_exp = simulation.time*5E6
    elif "night" in scenario:
        OH = 1E5
        OH_exp = simulation.time*1E5
    else:  
        OH = "Diurnal Cycle"
        OH_exp = simulation.time*5E6
    
    
    # Initialize data frame with time and reaction markers
    SimData = pd.DataFrame({"Time (s)" : simulation.time,
                            "desorb" : simulation.species["desorb"]})
    
    # get additional markers from autoxidation simulations    
    if "ao" in scenario:
        marker_data = {"OHprop" : simulation.species["OHprop"],
                            "ROprop" : simulation.species["ROprop"],
                            "RO2prop_alc" : simulation.species["RO2prop_alc"],
                            "RO2prop_ald" : simulation.species["RO2prop_ald"],
                            "RO2prop_ch2" : simulation.species["RO2prop_ch2"],
                            "RO2prop_rooh" : simulation.species["RO2prop_rooh"]}
        
        SimData = SimData.assign(**marker_data)
    # Find diameter of particle using length of stack.
    # If a single compartment simulation, use the volume of the compartment instead.
    if not "SC" in scenario:
        last_cmpt = simulation.compartments[(0, simulation.num_rows-1, 0)]
        diameter = 2*(last_cmpt.positions["y"]+last_cmpt.dimensions["y"])/1E-7
        
        
        # Calculate contour maps for each species
        simulation.calcContourInterpolated("Tri", reverse_axis = True)
        simulation.calcContourInterpolated("OO_sec", reverse_axis = True)
        simulation.calcContourInterpolated("O/C ratio", reverse_axis = True)

        # Place data into panel

        contour_data = {"Triacontane (normalized)": 
                        simulation.species_contour["Tri"]/simulation.species_contour["Tri"][0,0],
                       "Peroxy radicals": simulation.species_contour["OO_sec"],
                       "O/C ratio": simulation.species_contour["O/C ratio"]}
        
        if "ao" in scenario:
            simulation.calcContourInterpolated("O2", reverse_axis = True)
            simulation.calcContourInterpolated("ROprop", reverse_axis = True)
            simulation.calcContourInterpolated("RO2prop_ch2", reverse_axis = True)
            
            contour_data["RO2+RO2"] = simulation.species_contour["O2"]
            contour_data["ROprop"] = simulation.species_contour["ROprop"]
            contour_data["RO2prop_ch2"] = simulation.species_contour["RO2prop_ch2"]
            
            simulation.calcRadialCorrection("ROprop")
            simulation.calcRadialCorrection("RO2prop_ch2")
            simulation.calcRadialCorrection("RO2prop_alc")
            simulation.calcRadialCorrection("RO2prop_ald")
            simulation.calcRadialCorrection("RO2prop_rooh")
            simulation.calcRadialCorrection("OHprop")
            simulation.calcRadialCorrection("O2")
            
            marker_data = {"RO2+RO2" : simulation.species["O2_r"],
                            "OHprop" : simulation.species["OHprop_r"],
                            "ROprop" : simulation.species["ROprop_r"],
                            "RO2prop_alc" : simulation.species["RO2prop_alc_r"],
                            "RO2prop_ald" : simulation.species["RO2prop_ald_r"],
                            "RO2prop_ch2" : simulation.species["RO2prop_ch2_r"],
                            "RO2prop_rooh" : simulation.species["RO2prop_rooh_r"],
                            "RO2prop_tot" : simulation.species["RO2prop_ch2_r"] + \
                                            simulation.species["RO2prop_alc_r"] + \
                                            simulation.species["RO2prop_ald_r"] + \
                                            simulation.species["RO2prop_rooh_r"]}
        else:
            simulation.calcContourInterpolated("O2", reverse_axis = True)
            
            simulation.calcRadialCorrection("O2")
            
            contour_data["RO2+RO2"] = simulation.species_contour["O2"]
            
            marker_data = {"RO2+RO2" : simulation.species["O2_r"]}
        
        SimData = SimData.assign(**marker_data)
            
        # Find radial correction for alcohol species
        simulation.calcRadialCorrection("OHCH2_prim")
        simulation.calcRadialCorrection("OHCH_alpha")
        simulation.calcRadialCorrection("OHCH_sec")
        
        # Find total of alcohol groups
        alcohols = simulation.species["OHCH2_prim_r"] + simulation.species["OHCH_alpha_r"] + \
                        simulation.species["OHCH_sec_r"]
                        
        # Find radial correction for ketone species
        simulation.calcRadialCorrection("OC_sec")
        simulation.calcRadialCorrection("OC_alpha")
        
        # Find total of ketone groups
        ketones = simulation.species["OC_sec_r"] + simulation.species["OC_alpha_r"]
        
        # Find radial correction for aldehydes and acids
        simulation.calcRadialCorrection("OCH_prim")
        simulation.calcRadialCorrection("HOOC_prim")
        
        aldehydes = simulation.species["OCH_prim_r"]
        acids = simulation.species["HOOC_prim_r"]
        
        # Find radial correction for hydroperoxides
        simulation.calcRadialCorrection("HOOCH2_prim")
        simulation.calcRadialCorrection("HOOCH_alpha")
        simulation.calcRadialCorrection("HOOCH_sec")
        
        hydroperoxides = simulation.species["HOOCH2_prim_r"] + simulation.species["HOOCH_alpha_r"] + \
                    simulation.species["HOOCH_sec_r"]
                    
        # Find radial correction for peracids
        simulation.calcRadialCorrection("HO_OOC_prim")
        peracids = simulation.species["HO_OOC_prim"]
            
    else:
        volume = simulation.compartments[(0,0,0)].volume
        diameter = 2*(volume*3/4/np.pi)**(1/3)/1E-7
        
        # Create dummy contour maps
        Tri = np.empty((position_vector.size, simulation.time.size))
        Peroxy = np.random.binomial(1, 0.025, size=Tri.shape)
        OC_ratio = np.empty_like(Tri)
        for i in range(0, simulation.time.size):
            Tri[:, i] = simulation.species["Tri"][i]/simulation.species["Tri"][0]
            OC_ratio[:, i] = simulation.species["O/C ratio"][i]
            
        contour_data = {"Triacontane (normalized)" : Tri,
                       "Peroxy radicals" : Peroxy,
                       "O/C ratio" : OC_ratio}
        if "ao" in scenario:
            marker_data = {"RO2+RO2" : simulation.species["O2"],
                            "OHprop" : simulation.species["OHprop"],
                            "ROprop" : simulation.species["ROprop"],
                            "RO2prop_alc" : simulation.species["RO2prop_alc"],
                            "RO2prop_ald" : simulation.species["RO2prop_ald"],
                            "RO2prop_ch2" : simulation.species["RO2prop_ch2"],
                            "RO2prop_rooh" : simulation.species["RO2prop_rooh"],
                            "RO2prop_tot" : simulation.species["RO2prop_ch2"] + \
                                            simulation.species["RO2prop_alc"] + \
                                            simulation.species["RO2prop_ald"] + \
                                            simulation.species["RO2prop_rooh"]}
        else:
            marker_data = {"RO2+RO2" : simulation.species["O2"]}
        
        SimData = SimData.assign(**marker_data)
        
        # Find total of alcohol groups
        alcohols = simulation.species["OHCH2_prim"] + simulation.species["OHCH_alpha"] + \
                        simulation.species["OHCH_sec"]
                        
        # Find total of ketone groups
        ketones = simulation.species["OC_sec"] + simulation.species["OC_alpha"]
        
        # Find total of aldehydes and acids
        aldehydes = simulation.species["OCH_prim"]
        acids = simulation.species["HOOC_prim"]
        
        # Find total of hydroperoxides and peracids
        hydroperoxides = simulation.species["HOOCH2_prim"] + simulation.species["HOOCH_alpha"] + \
                    simulation.species["HOOCH_sec"]
        peracids = simulation.species["HO_OOC_prim"]
        
        

    ScenarioData[scenario+" contours"] = pd.Panel(contour_data, 
                                                  major_axis = position_vector,
                                                 minor_axis = simulation.time)
    new_data = dict()
    
    for species in contour_data.keys():
        species_df = pd.DataFrame(contour_data[species])
        new_data[species+" COV"] = species_df.std(0)/species_df.mean(0)
        
    SimData = SimData.assign(**new_data)
    
    # Find initial mass and carbon amount to normalize quantities
    tri_init = simulation.species["Tri_r"][0]
    mass_init = simulation.species["mass_r"][0]
    carbon_init = simulation.species["carbon_r"][0]
    
    # Sum up different functional groups
    hydroperoxides = simulation.species["HOOCH2_prim"] + simulation.species["HOOCH_alpha"] + \
                    simulation.species["HOOCH_sec"]
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
                "Hydroperoxides" : hydroperoxides,
                "Alcohols" : alcohols,
                "Ketones" : ketones,
                "Aldehydes" : aldehydes,
                "Carboxyllic acids" : acids,
                "Peracids" : peracids}

    SimData = SimData.assign(**new_data)
    
    # Generate carbon list
    
    carbon_list = ["nC"+str(i) for i in range(2, 31)]
    
    # Add carbon number data to data frame
    for carbon in carbon_list:
        carbondata = {carbon : simulation.species[carbon+"_r"]}
        SimData = SimData.assign(**carbondata)

    # Find rate coefficient and uptake coefficient for
    # 12 hours of daytime atmospheric oxidation
    
    index = (np.abs(simulation.time-12*3600)).argmin()
    
    regress = stats.linregress(x = OH_exp[0:index],
                               y=SimData["Triacontane (normalized)"][0:index])
    
    k_het = -1*regress[0]
    eff_uptake = 2*k_het*(200*1E-7)*0.81*6.02E23/3/6.092E4/422
    
    ScenarioData[scenario+" averages"] = SimData
    

    
    with pd.ExcelWriter(os.path.join(out_subdir, scenario+".xlsx"),
                            engine='xlsxwriter',
                            options={'nan_inf_to_errors': True}) as writer:
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
        
        # Write whether autoxidation was included or not
        if "ao" in scenario:
            flag = "yes"
        else:
            flag = "no"
        summary.write('K1', 'Autoxidation Included?')
        summary.write('K2', flag)
        
        # Write average and contour data to separate sheets
        ScenarioData[scenario+" averages"].to_excel(writer, sheet_name='average data', na_rep=0)
        for species, data in ScenarioData[scenario+" contours"].iteritems():
            sheet_name = re.sub("/", " to ", species)
            data.to_excel(writer, sheet_name=sheet_name, 
                          index_label="Distance from center (cm)", startrow=1, na_rep=0)
            
            worksheet = writer.sheets[sheet_name]
            worksheet.write(0, 1, "Time (s) ->")
        
        # Close writer and save output to excel
        writer.save()
    
    