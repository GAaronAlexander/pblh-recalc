# pblh-recalc
## Brief Description:
Uses WRF outputs to recalculate the PBLH heights based off of different methods found throughout literature
## Currently a work in progress

**Dependendencies:** numpy, matplotlib, cartopy, os, netCDF4, wrf-python, glob

Instructions for installation of wrf-python can be found: https://wrf-python.readthedocs.io/en/latest/installation.html

**Full Description:**
The Weather Research and Forecasting Model outputs many different meteorlogical variables that can be used to 're-diagnose' the planetary boundary layer height. This repository uses python to provide the structure to recalculate this variable to allow for comparison between model outputs of `PBLH` and standard literature methods of `PBLH`. Currently, two different methods have been implemented. 

## Richardson Number:
Using the richardson number calculation of field variables, the python program obtains the model level at which the richardson number falls above a critical value. This critical value can be defined by the user. 

## Temperature Gradient:
The temperature gradient method is looks at the Lapse Rates and determines the change in the Lapse Rate between levels is sufficient for a well mixed PBL. This method should only be used during afternoon model runs


## How to Run:

Instructions for a full run can be found in the main.py, and full descriptions of what different functions are doing can be found in related python files. 

## Files Created:

This repository will create 6 different directories:

### extracted_vars:

This directory contains raw WRF variables that are 3-D or 4-D tensors. They are saved as .npy files.

### extracted_vars_static:

This directory contains raw static WRF variables, meaning they are 2-D in nature. They are saved as .npy files.

### recalculated_vars:

Contains recalculated PBLH heights. 

### richardson_plots

Field plots of PBLH recalculated using the richardson number method

### temp_grad_plots

Field plots of PBLH recalculated using the temperature gradient method

### wrf_output_plots

Field plots of PBLH from raw WRF outputs



