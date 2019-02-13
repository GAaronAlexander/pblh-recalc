from wrf_variable_io import *
from wrf_basic_analysis_vars import *
from PBLH_recalc import *
from PBLH_plot import *
import numpy as np

# ~~~~~~~~~~~~~~~~ define important strings ~~~~~~~~~~~~~~~~~~~~~~~~
wrf_directory = './files' ##location of the wrf directory
file_name = 'wrfout_d02_2006-09-12_00:00:00' #wild card is supported if multiple wrf files are present

plot_richardson_direc = './richardson_plots/'
plot_temp_grad_direc = './temper_grad_plots/'
plot_real_wrf_pblh = '/wrf_output_plots/'

##note to change this string for SINGLE FILE if wild card is used to extract across multiple files above^^
single_netcdf_file = wrf_directory+'/'+file_name ##location of a single wrfout file (needed for plotting)

# ~~~~~~~~~~~~~~~~ define important lists ~~~~~~~~~~~~~~~~~~~~~~~~~~~

variables = ['theta','QVAPOR','ua','va','height','tv','PBLH']
static_variables = ['XLAT','XLONG']

# ~~~~~~~~~~~~~~~~~ extract variables ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

##these values are extracted and saved in directories as described by 
## wrf_variable_io

tensor_directory = wrf_extract_var_tensor(wrf_directory, file_name,variables)

static_directory = wrf_extract_var_constants(wrf_directory,file_name,static_variables)

# ~~~~~~~~~~~~~~~~~~ load in variables needed for PBLH analysis ~~~~~~~~~~~~~~~~~~~~~~~

##Tensor variables
theta   = np.load(tensor_directory+'theta.npy')      #K
qvapor  = np.load(tensor_directory+'QVAPOR.npy')     #unitless
uwind   = np.load(tensor_directory+'ua.npy')         #m/s
vwind   = np.load(tensor_directory+'va.npy')         #m/s
height  = np.load(tensor_directory+'height.npy')     #m
tv      = np.load(tensor_directory+'tv.npy')         #k
PBLH    = np.load(tensor_directory+'PBLH.npy')       #m

## static variables
lats = np.load(xy+'XLAT.npy')                        #degrees
lons = np.load(xy+'XLONG.npy')                       #degrees

# ~~~~~~~~~~~~~~~~ Recalculation of important Variables ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##full descriptions found in wrf_basic_analysis_vars

##virtual potential temperature
theta_v = virtual_potential_temp(theta,qvapor)        #K
 
##richardson number, and corresponding heights of richardson number

richardson_num,rich_num_height = richardson_number_surface(height,theta_v,uwind,vwind,tv,2)

##temperature gradients 
lapse_rate, lapse_rate_height = temperature_gradient(theta,height,2)

# ~~~~~~~~~~~~~~~ Rediagnosing PBLH ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## Full descriptions can be found in PBLH_recalc

PBLH_richardson_heights = PBLH_richardson(richardson_num, x, 0.2)
PBLH_temp_grad_heights = PBLH_temp_grad(lapse_rate, lapse_rate_height, 2)

wrf_save_var(PBLH_richardson_heights, './recalculated_vars','PBLH_richardson')
wrf_save_var(PBLH_temp_grad_heights, './recalculated_vars','PBLH_temp_grad')

# ~~~~~~~~~~~~~~~~ Plotting Software ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PBLH_plot(PBLH_ricardson_heights,lats,lons,single_netcdf_file,plot_richardson_direc)
PBLH_plot(PBLH_temp_grad_heights,lats,lons,single_netcdf_file,plot_temp_grad_direc)
PBLH_plot(PBLH,lats,lons,single_netcdf_file,plot_real_wrf_pblh)

