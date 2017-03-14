# StackSimAnalysis
Code exports and analyzes simulation data to XML from the simulation program [Kinetiscope](http://www.hinsberg.net/kinetiscope/). The directory /cpp/ contains C++ code for export of simulation data into XML format. The /python/ directory contains scripts for postprocessing of the simulation data. The Jupyter notebook /python/Postprocessing.ipynb demonstrates how the data analysis scripts are used to process data from the simulations. 

## Code for data analysis

These scripts have been developed to analyze data from Kinetiscope simulations exported as XML. 
The simulations are a stack of rectangular prisms used to represent a radial core of a spherical aerosol nanoparticle.
The code can pull out average properties of the aerosol or provide contour maps of the internal distribution. The following graphic gives an overview of the simulation. ![](/python/overview graphic.png) Additional details about the model simulations can be found in [this publication](http://pubs.rsc.org/en/content/articlelanding/2017/cp/c7cp00696a#!divAbstract).
