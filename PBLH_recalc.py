import numpy as np

##this script recalculates the PBLH heights given temperature gradients and richardson numbers in 
##two seperate routines

def PBLH_richardson(rich_num, height, critical_richard):
	##inefficent way of recalculating the PBLH height(needs to loop through time, and 2-d space)

	##likely going to take about ~3 minutes for one week of wrf runs
	##rediagnoses the PBLH heights through the use of the richardson number
	assert (len(rich_num.shape) ==4), "Richardson Number must be 4-D array (time, vertical, lat, lon)"
	assert (rich_num.shape == height.shape), "Heights and Richardson Numbers must be same size"

	##save shape files as 
	time_loop = rich_num.shape[0]
	vert_levels = rich_num.shape[1]
	lats_size = rich_num.shape[2]
	lon_size = rich_num.shape[3]

	##begin by allocating 
	PBLH_heights = np.zeros((time_loop,lats_size,lon_size))

	##create vertical boolean of richardson numbers that meet the criteria for stability defined 
	## by user. Anything above critical richardson is now True
	richardson_bool = rich_num > critical_richard

	##break the 4_d tensor of richardson boolians into a time loop, 
	##two space loops (lats and lons,)
	##and vertical profiles

	##on every vertical profile search for the first true value,
	##make the first true value location true in a filtering boolean for 
	##the PBLH heights from the height tensor that was passed by user
	for time in range(time_loop):

		heights_loop = height[time,:,:,:]
		##filter out unstable richardson numbers ()
		bool_filter = np.zeros((vert_levels,lats_size,lon_size),dtype=bool)

		for i in range(lats_size):
			for j in range(lon_size):
				for vert in range(vert_levels):

					if richardson_bool[time,vert,i,j] == True:

						##improve estimate by checking the model level below this to see if it is 
						##closer to crticial richardson number, and then flag for saving later

						# if np.abs(rich_num[time,vert,i,j] - critical_richard) > np.abs(rich_num[time,vert-1,i,j] - critical_richard):
						# 	bool_filter[vert-1,i,j] = True
						# 	break
						
						# else:
						bool_filter[vert,i,j] = True
						break
		##reshape to original lats and lons dimesions
		heights_save = heights_loop[bool_filter].reshape((lats_size,lon_size))

		PBLH_heights[time,:,:] = heights_save



	return PBLH_heights


def PBLH_temp_grad(lapse_rate, height, delta_required):
	##similar inefficient recalculation of the PBLH based off of lapse rates
	##looks for a change in the lapse rate from the surface that will indicate the top of the mixed layer
	##The delta_required acts as the trigger for the recalculation of the PBLH

	## if there is no PBLH height found via this method during a time period below the first 5km of the atmosphere
	## a value of -999 is placed in. This is likely to 
	## occur due to nocturnal boundary layer depth treatment in numerical models

	##this method is only valid during the afternoon, so ensure that any further analysis that 
	##uses only afternoon values

	##asertions
	assert (len(lapse_rate.shape) ==4), "Lapse Rates must be 4-D array (time, vertical, lat, lon)"
	assert (lapse_rate.shape == height.shape), "Heights and Lapse Rates must be same size"

	##create loop counters
	time_loop = lapse_rate.shape[0]
	lats_size = lapse_rate.shape[2]
	lon_size = lapse_rate.shape[3]

	PBLH_heights = np.zeros((time_loop,lats_size,lon_size)) 

	##calculation is based on the change in the lapse rates, so we need to adjust our loop in the vertical length
	lapse_rate_delta = lapse_rate[:,1: :,:] - lapse_rate[:,:-1,:,:]

	##create the delta bool needed for analysis
	lapse_rate_delta_bool = lapse_rate_delta > delta_required

	#define the vertical levesl
	vert_levels = lapse_rate_delta_bool.shape[1]


	##break into 4 for loops, looping throught time, lats, lons, and vertical levels
	##check if the delta_required condition has been met below the first 5km in the vertical of the model simulation
	##if it has not been satisfied in the first 5km, determine that this method does not work for that grid box and fill 
	##with a value of -999
	for time in range(time_loop):

		PBLH_loop = np.zeros((lats_size,lon_size))

		for i in range(lats_size):
			for j in range(lon_size):

				for vert in range(vert_levels):

					
					if height[time,vert,i,j] >= 5000:

						PBLH_loop[i,j] = -999 #erronous loop error
						break

					if lapse_rate_delta_bool[time,vert,i,j] == True:

						PBLH_loop[i,j] = height[time,vert,i,j]
						break

		PBLH_heights[time,:,:] = PBLH_loop


	return PBLH_heights


def PBLH_HOROW(theta,height,surface_level):

	##This method calculates the PBLH heights in WRF data sets through the use of the horowortz method, as outlined in 
	##Horowortz 1964

	##this is outlined to be the point at which the vertical profile of theta is 1.5 that of the surface level ()

	## if there is no PBLH height found via this method during a time period, a value of -999 is placed in. This is likely to 
	## occur due to nocturnal boundary layer depth treatment in numerical models 

	## this method is only valid during the afternoon, so ensure that any further analysis that 
	## uses only afternoon values

	assert(len(theta.shape) == 4), "Theta Variable must be 4-D array (time,vertical,lat,lon)"
	assert(theta.shape == height.shape), "Theta and height must be the same size"

	##adjust the theta and height to account for surface level provided

	theta_adj = theta[:,surface_level:,:,:]
	height_adj = height[:,surface_level:,:,:]

	##create loop counters
	time_loop = theta_adj.shape[0]
	vert_levels = theta_adj.shape[1]
	lats_size = theta_adj.shape[2]
	lon_size = theta_adj.shape[3]

	##allocate PBLH

	PBLH_heights = np.zeros((time_loop,lats_size,lon_size))

	for time in range(time_loop):
		## create PBLH loop
		PBLH_loop = np.zeros((lats_size,lon_size))

		##remove the surface level
		surface_level_loop = theta_adj[time,0,:,:]

		##add 1.5 to surface level, and create bool vertical space

		surface_bool = theta_adj[time,1:,:,:] > surface_level_loop + 1.5

		##we now test for the first true in the surface bool on each vertical level

		for i in range(lats_size):

			for j in range(lon_size):

				for vert in range(1,vert_levels): #start at one because we are basing this calculation on the surface level

					if height[time,vert,i,j] >= 5000:

						PBLH_loop[i,j] = -999 #erronous loop error
						break


					if surface_bool[vert-1,i,j] == True:

						PBLH_loop[i,j] = height[time,vert,i,j]
						break

		PBLH_heights[time,:,:] = PBLH_loop

	return PBLH_heights








