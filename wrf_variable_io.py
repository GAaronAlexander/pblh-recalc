##This file was created to extract files from WRF output files and save them 
##to a directory that is specified by the user.

##dependent upon netCDF4
##dependend upon WRF-python
##dependent upon numpy
##dependent on os

from netCDF4 import Dataset
import numpy as np 
import os
import wrf
import glob 

##
def wrf_extract_var_tensor(path_to_file,filename,variables):
	##path_to_file is a string that either leads to one file or leads to directory that contains many netcdf files
	##variables is a list of strings that are variables within the netcdf files. These are case sensitive
	
	##this will delete files that are of the same name in the path_to_save directory
	##creates a directory that is called exctracted_vars in the local directory

	##returns the location of the new directory where our files are saved
	##sets current directory
	directory_path = os.path.dirname(os.path.realpath(__file__))
	print(directory_path)

	new_directory = directory_path+'/exctracted_vars/'

	##attempts to create the new directory
	try: 
		os.makedirs(new_directory)
	except OSError:
		print('%s Directory Failed to Create. May be already present' %new_directory)

	####list files in path provided, and append as a dataset (netcdf data set class)
	file_names = glob.glob(path_to_file+'/' + filename)
	file_list= []

	for name in file_names:
		file_list.append(Dataset(name))

	#loop over variables desired
	for i,var in enumerate(variables):
		##print variable extraction
		print('------Extracting Variable %s------ '%var)

		variable = wrf.getvar(file_list,var,timeidx=wrf.ALL_TIMES,method="cat")
		variable_np = wrf.to_np(variable)

		#create variable save name
		savefile_loop = new_directory + var 

		np.save(savefile_loop,variable_np)


	print('-----Extract Variables Finished----')

	return new_directory

def wrf_extract_var_constants(path_to_file,filename,variables):
	##path_to_file is a string that either leads to one file or leads to directory that contains many netcdf files
	##variables is a list of strings that are variables within the netcdf files. These are case sensitive, and are assumed to be 
					##constants within the netcdf file (i.e. these do not change throughout the simulation)
	##save_label is the hanging label that will be used to save variables:
					##variables will be saved as VARNAME_savelabel

	##this will delete files that are of the same name in the path_to_save directory
	##creates a directory that is called exctracted_vars in the local directory

	##returns the location of the new directory where our files are saved
	##sets current directory
	directory_path = os.path.dirname(os.path.realpath(__file__))
	print(directory_path)

	new_directory = directory_path+'/exctracted_vars/'

	##attempts to create the new directory
	try: 
		os.makedirs(new_directory)
	except OSError:
		print('%s Directory Failed to Create. May be already present' %new_directory)

	####list files in path provided, and append as a dataset (netcdf data set class)
	file_names = glob.glob(path_to_file+'/' + filename)
	file_list= []

	
	file_list.append(Dataset(file_names[0]))

	#loop over variables desired
	for i,var in enumerate(variables):
		##print variable extraction
		print('------Extracting Variable %s------ '%var)

		variable = wrf.getvar(file_list,var,timeidx=0,method="cat")
		variable_np = wrf.to_np(variable)

		#create variable save name
		savefile_loop = new_directory + var 

		np.save(savefile_loop,variable_np)


	print('-----Extract Variables Finished----')

	return new_directory

def wrf_save_var(variable,directory_path,variable_name):

	##saves variables to a directory that you specify. saves the variables as
	##.npy files

	##note that the directory must be present

	if directory_path.endswith('/'):
		save_me = directory_path + variable_name
	else:
		save_me = directory_path + '/' + variable_name

	np.save(save_me,variable)
	print('----%s saved to %s -----'%(variable_name ,directory_path))


