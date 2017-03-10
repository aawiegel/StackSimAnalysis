## Quick start

Use the Jupyter notebook Postprocessing.ipynb to see how the postprocessing data analysis works with graphs of each scenario.

## Files

### StackSim.py

Generic simulation and compartment classes used to represent the simulated data. The current implementation 
assumes a stack of compartments (see above), but could easily be extended for a full 3D treatment. The classes
contain generic methods for calculating average properties, species sums, and species ratios. For example,
a list of species associated with oxygen atoms and a list of species associated with carbon atoms can each be 
summed. Then, the ratio of oxygen to carbon atoms in the aerosol can be calculated to be compared to aerosol
mass spectometer data.

### Postprocessing.ipynb

This Jupyter notebook details the calculations used to process the data from the simulation XML files. Then, it graphs several relevant average properties from the simulation. Contour maps showing the internal distribution of the starting material, peroxy radicals, and O/C ratio are also found. Finally, the results are written to Excel files (not included in repository due to their size).

## Model scenario descriptions

Two main model scenarios considered are Scenario 1, Scenario 2, Scenario 1A, and Scenario 2A. Scenario 1 includes constant diffusion (derived from measurements of the bulk viscosity) and a gas phase OH + carboxyllic acid rate coefficient. Scenario 2 also has constant diffusion but an aqueous phase OH + carboxyllic acid rate coefficient. Model scenarios labeled with 'A' have the same chemistry, but a plasticization of the aerosol occurs when lower carbon number products (\<C16) form. More specifically, the diffusion coefficient increases by 5 orders of magnitude. 
