##this file outlines basic analysis of variables for general wrf outputs. 
##Please see each function for brief introduction to what each value is calculating

import numpy as np 


def virtual_potential_temp(theta,qvapor):
	assert (theta.shape == qvapor.shape), "Theta and Qvapor must be same size"
	assert (type(theta) is np.ndarray), "Theta must be an numpy.ndarray"
	assert (type(qvapor) is np.ndarray), "Qvapor must be an numpy.ndarray"
	
	#calculate the virtual potential temperature based on the assumption there is no 
	#liquid vapor in the air (good assumption for lower areas of the atmopshere with no precipitation)
	theta_v = theta*(1+0.61*qvapor)

	return theta_v


def richardson_number_profiles(height,theta_v,uwind,vwind,tv,surface_level):
	##richardson number profiles based off of surface level, this calcualtes a *local* richardson number 
	## based off of model grid boxes, but uses the surface as the reference

	## height  -----  height of model grid boxes  ---- meters
	## theta_v -----  virtual potential temperature -- kelvin
	## uwind   -----  u wind mass coordinates -------- meters per second
	## vwind   -----  v wind mass coordinates -------- meters per second
	## tv      -----  virtual temperature ------------ kelvin

	## surface_level is number of levels to skip from surface 

	##assertions
	assert (len(theta_v.shape) == 4), "arrays must be 4 dimensional (time, height, lat, lon)"
	assert (theta_v.shape == height.shape), "Theta_v and Height must be same size"
	assert (theta_v.shape == uwind.shape) , "Theta_v and Uwind must be same size"
	assert (theta_v.shape == vwind.shape),  "Theta_v and Vwind must be same size"

	assert (type(theta_v) is np.ndarray), "Theta_v must be a numpy.ndarray"
	assert (type(uwind) is np.ndarray), "Uwind must be a numpy.ndarray"
	assert (type(vwind) is np.ndarray), "Vwind must be a numpy.ndarray"
	assert (type(height) is np.ndarray),"Height must be a numpy.ndarray"


	#calculate the richardson number based off of dimensional analysis
	# of the buoyant term devided by the shear term of the N.S. Eqatuions

	## determine the reference virtual temperature
	base_level_tv = tv[:,surface_level,:,:]

	delta_thetav = theta_v[:,surface_level+1:,:,:] - theta_v[:,surface_level:-1,:,:]
	delta_u = uwind[:,surface_level+1:,:,:] - uwind[:,surface_level:-1,:,:]
	delta_v = vwind[:,surface_level+1:,:,:] - vwind[:,surface_level:-1,:,:]
	delta_h = height[:,surface_level+1:,:,:] - height[:,surface_level:-1,:,:]

	wind = delta_u**2 + delta_v**2

	richardson = ((9.81 * delta_h)/(base_level_tv[:,None,:,:])) * (delta_thetav/wind)
	
	return richardson,  height[:,surface_level:,:,:]


def richardson_number_surface(height,theta_v,uwind,vwind,tv,surface_level):
	##determines the richardson number based on surface level values
	## height  -----  height of model grid boxes  ---- meters
	## theta_v -----  virtual potential temperature -- kelvin
	## uwind   -----  u wind mass coordinates -------- meters per second
	## vwind   -----  v wind mass coordinates -------- meters per second
	## tv      -----  virtual temperature ------------ kelvin

	## surface_level is number of levels to skip from surface 

	##returns profiles of ridchardson numbers and the midpoint heights of each of the levels
	
	#calculate the richardson number based off of dimensional analysis
	# of the buoyant term devided by the shear term of the N.S. Eqatuions
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	##assertions
	assert (len(theta_v.shape) == 4), "arrays must be 4 dimensional (time, height, lat, lon)"
	assert (theta_v.shape == height.shape), "Theta_v and Height must be same size"
	assert (theta_v.shape == uwind.shape) , "Theta_v and Uwind must be same size"
	assert (theta_v.shape == vwind.shape),  "Theta_v and Vwind must be same size"

	assert (type(theta_v) is np.ndarray), "Theta_v must be a numpy.ndarray"
	assert (type(uwind) is np.ndarray), "Uwind must be a numpy.ndarray"
	assert (type(vwind) is np.ndarray), "Vwind must be a numpy.ndarray"
	assert (type(height) is np.ndarray),"Height must be a numpy.ndarray"
	assert (type(surface_level) is int), "Surface_level must be an int"

	##assume that the first two model levels are in the surface level, so create 'base level' variables
	base_level_thetav = theta_v[:,surface_level,:,:]
	base_level_tv = tv[:,surface_level,:,:]
	base_level_uwind = uwind[:,surface_level,:,:]
	base_level_vwind = vwind[:,surface_level,:,:]

	## start at 3rd model level, and subtract 3-d tensor from 4-d tensor by broadcasting
	delta_thetav = theta_v[:,surface_level:,:,:] - base_level_thetav[:,None,:,:]
	
	#absolute wind speed
	delta_u = uwind[:,surface_level:,:,:] - base_level_uwind[:,None,:,:]
	delta_v = vwind[:,surface_level:,:,:] - base_level_vwind[:,None,:,:]

	wind = delta_u**2 + delta_v**2

	#unitless richardshon bulk 
	richardson = ((9.81 * height[:,surface_level:,:,:])/(base_level_tv[:,None,:,:])) * (delta_thetav/wind)

	return richardson, height[:,surface_level:,:,:]

def temperature_gradient(theta,height,surface_level):

	##determines the temperature gradiensts throught the model domain (removes top of model)

	##determines the richardson number based on surface level values
	## height  -----  height of model grid boxes  ---- meters
	## theta   -----  potential temperature         -- kelvin

	##returns:
	## temperature gradients ----- kelvin/kilometer
	## midpoint heights ------ meters 
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	assert (len(theta.shape) == 4),"arrays must be 4 dimensional (time, height, lat, lon)"
	assert (theta.shape == height.shape),"Theta and Height must be the same shape"

	assert (type(theta) is np.ndarray),"Theta must be an numpy.ndarray"
	assert (type(height) is np.ndarray), "Height must be an numpy.ndarray"

	delta_theta = theta[:,surface_level+1:,:,:] - theta[:,surface_level:-1,:,:] #kelvin
	delta_z = height[:,surface_level+1:,:,:] - height[:,surface_level:-1,:,:] # always postive (m)

	lapse_rate = (delta_theta/delta_z) *1000 #kelvin per kilometer (adjusted so typical is atmospheric behavior is negative)

	return lapse_rate, height[:,surface_level:-1,:,:]




