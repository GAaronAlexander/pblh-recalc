##This function plots rediagnosed PBLH files for comparsion. 

##Requires:

#numpy
#matplotlib.pyplot
#wrf
#netcdf4
#cartopy
#os

import numpy as np 
import matplotlib.pyplot as plt 
import netCDF4 
import cartopy.crs as crs
import wrf 
from matplotlib.cm import get_cmap
import cartopy
from cartopy.feature import NaturalEarthFeature
import os

def PBLH_plot(pblh_file,lats,lons,netcdffile,save_path):


	##recieves numpy files of pblh (3 dimension (time, lats, lons))
	##lats 
	##lons
	##path to a single pblh, lats, and lons were pulled from (need projection data)
	##save path

	##outputs len(time) number of plots in the save_path specified. 
	##save_path does not need to be present to work

	#create the save path (first check directory situation)
	if save_path.endswith('/'):
		save_path = save_path
	else:
		save_path = save_path + '/'
	
	try: 
		os.makedirs(save_path)
	except OSError:
		print('%s Directory Failed to Create. May be already present' %save_path)


	##load in the projection data set (only pull one time step, which should not add on too much time)
	##for standard wrf files XLAT should always be present
	data_file = netCDF4.Dataset(netcdffile)
	proj=wrf.getvar(data_file,'XLAT', timeidx=0)
	cart_proj = wrf.get_cartopy(proj)

	##read how many different files we will be making (one for each time)
	number_plots = pblh_file.shape[0]

	## PLOTTING STUFF
	## define useful fonts
	plt.rc('text', usetex=True)
	plt.rc('font', family='sans-serif')

	##Creation of plot loop

	for i in range(number_plots):

		##create save name
		save_name_loop = save_path + 'pblh_plot_' + str(i).zfill(6) + '.tiff'

		##general plot stuff
		fig = plt.figure('test_smois',figsize=(6,6), dpi=200)
		cmap='jet'

		##standard additions to the plot
		ax = plt.axes(projection=cart_proj)
		states = NaturalEarthFeature(category='cultural', scale='50m', facecolor='none',
	                             name='admin_1_states_provinces_lines')
		ax.add_feature(states, linewidth=.8)
		ax.add_feature(states, edgecolor='black')
		ax.add_feature(cartopy.feature.RIVERS)
		ax.add_feature(cartopy.feature.BORDERS)
		ax.coastlines('50m', linewidth=.8)
		

		actual_plot = plt.pcolormesh(lons, lats, pblh_file[i,:,:], cmap = cmap,transform=crs.PlateCarree())

		cax = fig.colorbar(actual_plot, orientation='vertical', label=r'PBLH $(m)$')
		plt.title('PBLH Heights',fontsize=28)
		plt.savefig(save_name_loop,figsize=(6, 6), dpi=400)
		plt.close()

	print('---Plots created in %s---' %save_path)







