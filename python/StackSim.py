#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 14:03:22 2016

@author: Aaron W
"""
import numpy as np
import math
import os
from scipy import interpolate
from xml.dom import minidom
from matplotlib import ticker
import matplotlib.pyplot as plt
import matplotlib.cm as cm

class SimulationData:
    """holds and processes simulation data from a compartment simulation"""
    
    def __init__(self, xml_file):
    
        # Parse xml file
        with minidom.parse(xml_file) as data_dom:
            
            # Create empty dictionary of compartments
            self.compartments = dict()
            
            # Store simulation file name
            
            self.sim_file = os.path.basename(data_dom.getElementsByTagName("file")[0].firstChild.nodeValue)
            
            # Get number of compartments and number of time points
            self.num_compartments = int(data_dom.getElementsByTagName("num_compartments")[0].firstChild.nodeValue)
            self.num_points = int(data_dom.getElementsByTagName("num_points")[0].firstChild.nodeValue)
            
            # Get number of rows (y), columns (x), and layers (z).
            self.num_rows = int(data_dom.getElementsByTagName("num_rows")[0].firstChild.nodeValue)
            self.num_columns = int(data_dom.getElementsByTagName("num_columns")[0].firstChild.nodeValue)
            self.num_layers = int(data_dom.getElementsByTagName("num_layers")[0].firstChild.nodeValue) 
            
            # Get time points
            self.time = np.fromstring(data_dom.getElementsByTagName("time_points")[0].firstChild.nodeValue, sep=",")
            
            compt_elem_list = data_dom.getElementsByTagName("compartment")
            
            for compt_elem in compt_elem_list:
                compt = Compartment(compt_elem)
                self.compartments[compt.getComptCoordinates()] = compt
    
            self.calcCartCoordinates()
            
      
            # Initialize species dictionaries for sum of species and for contour of species
            self.species = dict()
            self.species_contour = dict()
            
            # Calculate sum of each species for whole simulation
    
            for species in self.compartments[(0,0,0)].getSpeciesNameList():
                self.calcSpeciesSum(species)
            
            # Initialize volume
            self.volume = np.zeros_like(self.time)
                
            self.calcSimulationVolume()
    
    def calcSpeciesSum(self, species_name):
        """Calculates sum of a species over the whole simulation"""
        
        species_amount = np.zeros_like(self.time)
        
        for compartment in self.compartments.values():
            species_amount += compartment.species[species_name]
        
        self.species[species_name] = species_amount
            
        
    def calcCartCoordinates(self):
        """Calculates Cartesean (x,y,z) coordinates of compartments, 
            need to initialize compartment dictionary first.
        """
      
          
      
        for column in range(self.num_columns):
            for row in range(self.num_rows):
                for layer in range(self.num_layers):
                
                    # If column is not 0, add x length of compartment to x_position of previous compartment, otherwise the x_position is just x
                    if(column > 0):
                        self.compartments[(column, row, layer)].positions["x"] = \
                            self.compartments[(column-1, row, layer)].positions["x"] + self.compartments[(column-1, row, layer)].dimensions["x"]
                    #self.compartments[(column, row, layer)].positions["x"] += self.compartments[(column,row,layer)].dimensions["x"]/2
                    
                        
                    # Similar to above, except for y and rows
                    if(row > 0):
                        self.compartments[(column, row, layer)].positions["y"] = \
                            self.compartments[(column, row-1, layer)].positions["y"] + self.compartments[(column, row-1, layer)].dimensions["y"]
                    #self.compartments[(column, row, layer)].positions["y"] += self.compartments[(column, row, layer)].dimensions["y"]/2
                        
                    # Similar to above, except for z and layers
                    if(layer > 0):
                        self.compartments[(column, row, layer)].positions["z"] = \
                            self.compartments[(column, row, layer-1)].positions["z"] + self.compartments[(column, row, layer-1)].dimensions["z"]
                    #self.compartments[(column, row, layer)].positions["z"] += self.compartments[(column, row, layer)].dimensions["z"]/2
    
    def ReverseCoordinates(self):
        """Reverses order of Cartesean coordinates of compartments"""
        for column in range(self.num_columns):
            for row in range(self.num_rows):
                for layer in range(self.num_layers):
                    pass
    
    def calcSimulationVolume(self):
        """Calculates total volume from each compartment subvolume"""
        
        for compartment in self.compartments.values():
            self.volume += compartment.volume
            
    
    
    def calcAggregateSpecies(self, name, species_list):
        """Calculates an aggregate species from a list of species and their weights for each compartment"""      
        
        for compartment in self.compartments.values():
            compartment.calcAggregateSpecies(name, species_list)
        
        self.calcSpeciesSum(name)
            
    def calcRadialCorrection(self, name, dimension="y", reverse_axis=False):
        """Applies a radical correction to a species, assuming that the 1-D stack represents a core into a sphere"""
        
        
        if(reverse_axis):
            # Get reference to last compartment, defaults to y here (change later for other dimenisons)        
            cmpt = self.compartments[(0, self.num_rows-1, 0)]        
            length = cmpt.positions[dimension] #+ cmpt.dimensions[dimension]
            #print(length)

            
        
        for compartment in self.compartments.values():
            
            # Find beginning and end of compartment
            r_i = compartment.positions[dimension]
            r_f = r_i + compartment.dimensions[dimension]
            
            if(reverse_axis):
                r_i = length - r_i
                r_f = r_i + compartment.dimensions[dimension]
                
        
                
            # Calculate volume of shell
            vol_shell = 4/3*math.pi*(r_f**3 - r_i**3)
            #print(vol_shell)
            
            # Adjust species based on weighted amount per shell
            compartment.species[name+"_r"] = compartment.species[name]*vol_shell/compartment.volume
            
        self.calcSpeciesSum(name+"_r")
            
    def calcSpeciesRatio(self, name, species1, species2):
        """Calculate a species ratio for each compartment, then find sum over whole simulation"""
        
        for compartment in self.compartments.values():
            compartment.calcSpeciesRatio(name, species1, species2)
        
        self.species[name] = self.species[species1]/self.species[species2]
    
   
    def calcContourInterpolated(self, data, res=5, reverse_axis=False, concentration=False): # Saved for multidimensional simulation: , direction="x", start_coord=(0,0,0)):
        """Interpolates position grid from compartment data for use in creating 
            contour plots of one dimension (run calcCartCoordinates first)
           Assigns a position array and an interpolated contour of the data
        """
        
   
        # Initialize numpy arrays
        position = np.zeros((self.num_rows, self.time.size))
        z = np.zeros_like(position)
        volume = np.ones_like(position)
        stack_len = np.zeros_like(self.time)
        
        if(reverse_axis):
            # Get length of stack for reversing coordinates
            last_compt = self.compartments[(0, self.num_rows-1, 0)]
            stack_len = last_compt.positions["y"] #+ last_compt.dimensions["y"]/2

        # Fill arrays with position data and concentration data from simulation        

        for row in range(self.num_rows):
            position[row, :] = self.compartments[(0, row, 0)].positions["y"]
            if(concentration):
                volume[row, :] = self.compartments[(0, row, 0)].volume# 
            z[row, :] = self.compartments[(0, row, 0)].species[data]
        
        # Calculates concentration from volume. If concentration is false, just divides by 1 and returns z
        z = z/volume
      
       
        # Initialize position grid
        position_i = np.linspace(position.min(), position.max(), self.num_rows*res)
        
        z_i = np.zeros((position_i.size, self.time.size))        
        
        # Reinterpolate concentration data to regularly spaced position grid        
        
        for t in range(self.time.size):
            pos = position[:, t]
            z_t = z[:, t]            
            
            if(reverse_axis):
                pos = np.flipud(stack_len[t] - pos)

                z_t = np.flipud(z_t)
                

            
            spl = interpolate.interp1d(pos, z_t, bounds_error=False, fill_value=0.)
            
            z_i[:, t] = spl(position_i)
            
        self.position_int = position_i
        self.species_contour[data] = z_i
        

    def getDepthProfile(self, data, time_slice, depth_slice, reverse_axis=True):
        """ Generates sum of a species 'data' at a certain depth profile 
            from a contour map, time_slice, and depth_slice.
            ContourMap of data must be generated first.
        """
    
        # Find closest index to time slice        
        time_i = (np.abs(self.time-time_slice)).argmin()
        
        # Find position of top compartment
        if(reverse_axis):
            max_position = self.compartments[(0, self.num_rows-1, 0)].positions["y"][time_i]
        else:
            max_position = self.compartments[(0, 0, 0)].positions["y"][time_i]
         
        min_position = max_position - depth_slice
    
        # Find closest index to min and max position
        max_pos_i = (np.abs(self.position_int - max_position)).argmin()
        min_pos_i = (np.abs(self.position_int - min_position)).argmin()
    
        return np.sum(self.species_contour[data][min_pos_i:max_pos_i])     
        
        
    
    def plotCrossSection(self, data, time_slice, time_factor=(1, 'sec'), reverse_axis=False, concentration=False, plot_average=False):
        """Plots a position-interpolated cross section of a species in the simulation (run calcCartCoord first)"""
        
        # Calculates time units. Default: seconds. (Other possibilities include OH exposure, etc.)        
        time = self.time[time_slice]*time_factor[0]
        

        # Initialize arrays            
        position = np.zeros(self.num_rows)
        
        amount = np.zeros_like(position)
        
        volume = np.ones_like(position)
        
        # Assign last compartment to the bottom of the stack, if reverse axis, set it as the top compartment
        last_compt = self.compartments[(0, 0, 0)]        
        
        if(reverse_axis):
            last_compt = self.compartments[(0, self.num_rows-1, 0)]
        
        # Find the length of the stack
        stack_len = last_compt.positions["y"][time_slice]
        
        # Collect data from each compartment, then find concentration if concentration flag is set (defaults to molecules or mol otherwise)
        for row in range(self.num_rows):
            position[row] = self.compartments[(0, row, 0)].positions["y"][time_slice]
            if(concentration):
                volume[row] = self.compartments[(0, row, 0)].volume[time_slice]
            amount[row] = self.compartments[(0, row, 0)].species[data][time_slice]
        
        amount = amount/volume
        
        # Initialize position interpolation array
        position_i = np.linspace(position.min(), position.max(), self.num_rows*10)
        
        if(reverse_axis):
            position = np.flipud(stack_len - position)
            amount = np.flipud(amount)
        
        # Create interpolation function
        spl = interpolate.interp1d(position, amount, bounds_error=False, fill_value=0.) 
        
        # Interpolate data on position interpolation array
        amount_i = spl(position_i)
        
        plt.title(data + " at " + str(time) + " " + time_factor[1], y=1.02)
        
        plt.xlabel('Distance from particle center (nm)')
        plt.ylabel(data)

        
        plt.plot(position_i/1E-7, amount_i, '-k')
        
        # Plot average value if specified
        if(plot_average):
            average = np.zeros_like(position_i) + self.species[data][time_slice]
            plt.plot(position_i/1E-7, average, '--r', label='average')
            plt.legend(loc='best')
        
        
        plt.show()            
        
        
        

class Compartment:
    """holds data from a compartment"""
    
    def __init__(self, element):
    
        # Assign DOM element to compartment
        self.element = element
        
        # load index
        
        self.ID = int(self.element.getElementsByTagName("index")[0].firstChild.nodeValue)
        
        # Load compartment coordinates
        
        self.column = int(self.element.getElementsByTagName("column")[0].firstChild.nodeValue)
        self.row = int(self.element.getElementsByTagName("row")[0].firstChild.nodeValue)
        self.layer = int(self.element.getElementsByTagName("layer")[0].firstChild.nodeValue)
                        
        # Load in initial dimensions
        x_initial = float(self.element.getElementsByTagName("x_initial")[0].firstChild.nodeValue)
        y_initial = float(self.element.getElementsByTagName("y_initial")[0].firstChild.nodeValue)
        z_initial = float(self.element.getElementsByTagName("z_initial")[0].firstChild.nodeValue)
        
        # Load volume data
        
        volume_string = self.element.getElementsByTagName("volume")[0].firstChild.nodeValue
        self.volume = np.fromstring(volume_string, sep=",")
        
        # Create dictionary for dimensions
        
        self.dimensions = dict()
        
        self.dimensions["x"] = np.zeros_like(self.volume)
        self.dimensions["y"] = np.zeros_like(self.volume)
        self.dimensions["z"] = np.zeros_like(self.volume)
        
        self.dimensions["x"][0] = x_initial
        self.dimensions["y"][0] = y_initial
        self.dimensions["z"][0] = z_initial
        
        # Calculate rest of array from volume change
        
        self.calcDimension("x")
        self.calcDimension("y")
        self.calcDimension("z")
        
        # Create position dictionary        
        
        self.positions = dict()    
        
        # Create arrays for position
        
        self.positions["x"] = np.zeros_like(self.volume)
        self.positions["y"] = np.zeros_like(self.volume)
        self.positions["z"] = np.zeros_like(self.volume)
        
        # Load pressure data
        
        self.pressure = np.fromstring( self.element.getElementsByTagName("pressure")[0].firstChild.nodeValue, sep="," )
        
        # Load temperature data
        
        self.temperature = np.fromstring( self.element.getElementsByTagName("temperature")[0].firstChild.nodeValue, sep="," )
        
        # Create empty species dictionary
        self.species = dict()
        
        # Get list of species elements
        species_elements = self.element.getElementsByTagName("species")
        
        # Create dictionary of species based on name
        for species_element in species_elements:
            name = species_element.getElementsByTagName("name")[0].firstChild.nodeValue
            amount = np.fromstring( species_element.getElementsByTagName("amount")[0].firstChild.nodeValue, sep="," )
            self.species[name] = amount
    
    
    def calcDimension(self, dimension="x"):
        self.dimensions[dimension] = (self.volume/self.volume[0])**(1/3.)*self.dimensions[dimension][0]
        
    def getComptCoordinates(self):
        return self.column, self.row, self.layer
    
    def getSpeciesNameList(self):
        return self.species.keys()
    
    def calcAggregateSpecies(self, name, species_list):
        """Calculates an aggregate species from a list of species and their weights"""
        self.species[name] = np.zeros(self.volume.size)
        for species, weight in species_list:
            self.species[name] += weight*self.species[species]
    
    def calcSpeciesRatio(self, name, species1, species2):
        """Calculates a ratio of two species and gives it a new name"""
        self.species[name] = np.nan_to_num(self.species[species1]/self.species[species2])
        
        # Sets infinite values to zero
        self.species[name][self.species[name] > 1E308] = 0




def ProcessTriSimulation(file_dict, subdir):
    """Convenience function for Triacontane simulations
    Takes simulation file name dictionary and subdirectory 
    and returns simulation object dictionary
    With several average values already calculated"""
    
    # Create empty simulation dictionary
    sim_dict = dict()
    
    # Generate lists for finding weighting aggregate species from individual
    # functional group or carbon backbone species
    
    carbon_min, carbon_max = 1, 30
    
    missing_carbon_no = [1, 30]
    
    # Create carbon-30 lumped species from each component
    
    carbon_no_dict = {"nC30" : [["C30", 1], ["C30_COOH", 1], ["C30_COOH_O", 1], ["C30_HOOCCOOH", 1], ["C30_O2", 1], ["C30_O", 1]]}
    
    # Initialize list of lists
    
    carbon_list = [["nC30", 30]]
    
    for i in range(carbon_min, carbon_max+1, 1):
        if i in missing_carbon_no:
            pass
        else:
            no_C = "C"+str(i)
            
            # Add entry to lumped carbon number dictionary
            carbon_no_dict["n"+no_C] = [[no_C, 1], [no_C+"_O2", 1], [no_C+"_COOH", 1], [no_C+"_COOH_O", 1], [no_C+"_HOOCCOOH", 1]]
            
            # Add entry to list of list for carbon number weighting
            carbon_list.append(["n"+no_C, i])
    
    # Generate oxygen and hydrogen species weighting lists
    
    oxygen_list = [["OC_sec", 1], ["OCH_prim", 1], ["OHCH2_prim", 1], ["OHCH_sec", 1],
                   ["OC_alpha", 1], ["OHCH_alpha", 1], ["HO_OOC_prim", 3],
                   ["HOOCH2_prim", 2], ["HOOCH_alpha", 2], ["HOOCH_sec", 2], ["HOOC_prim", 2]]
    
    hydrogen_list = [["CH3_prim", 3], ["CH3_prim_s", 3], ["CH2_sec", 2], ["CH2_alpha", 2], 
                     ["OCH_prim", 1], ["OHCH_sec", 2], ["OHCH2_prim", 3], ["OHCH_alpha", 2],
                     ["HO_OOC_prim", 1], ["HOOCH2_prim", 3], ["HOOCH_alpha", 2], ["HOOCH_sec", 2], ["HOOC_prim", 1]]
    
    # Generate mass weighting lists
    
    mass_list = [["carbon", 12], ["oxygen", 16], ["hydrogen", 1]]
    
    mass_list_r = [["carbon_r", 12], ["oxygen_r", 16], ["hydrogen_r", 1]]
    
    for scenario in file_dict.keys():
        
        # Load and process simulation data from simulation    
        sim_dict[scenario] = SimulationData(os.path.join(subdir, file_dict[scenario]))
        
        # Calculate aggregate carbon species and radial correction
        for carbon_no in carbon_no_dict.keys():
            sim_dict[scenario].calcAggregateSpecies(carbon_no, carbon_no_dict[carbon_no])
            sim_dict[scenario].calcRadialCorrection(carbon_no, reverse_axis=True)
        
    
        # Calculate each element and mass    
        sim_dict[scenario].calcAggregateSpecies("carbon", carbon_list)
    
        sim_dict[scenario].calcAggregateSpecies("oxygen", oxygen_list)
    
        sim_dict[scenario].calcAggregateSpecies("hydrogen", hydrogen_list)     
        
        sim_dict[scenario].calcAggregateSpecies("mass", mass_list)
        
        # Calculate radial correction for each element and mass    
        
        sim_dict[scenario].calcRadialCorrection("mass", reverse_axis=True)
        sim_dict[scenario].calcRadialCorrection("oxygen", reverse_axis=True)
        sim_dict[scenario].calcRadialCorrection("carbon", reverse_axis=True)
        sim_dict[scenario].calcRadialCorrection("hydrogen", reverse_axis=True)
        
        # Calculate radial correction for triacontane    
        
        sim_dict[scenario].calcRadialCorrection("Tri", reverse_axis=True)
        
        # Calculate mass of aerosol    
        
        sim_dict[scenario].calcAggregateSpecies("mass_r", mass_list_r)
        
        sim_dict[scenario].calcSpeciesRatio("O/C ratio", "oxygen_r", "carbon_r")
        sim_dict[scenario].calcSpeciesRatio("H/C ratio", "hydrogen_r", "carbon_r")
        
    return sim_dict
