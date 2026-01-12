# Using NCO to manipulate nc files

## Editing a file
add a variable:
```
ncks -A -v <var_name> infile.nc outfile.nc
```

delete a variable:
```
ncks -O -x -v <var> in.nc out.nc
```

## Resampling data
Resample daily data to monthly with cdo
```
cdo monmean in_daily.nc out_monthly.nc
```
Extract a hyperslab of the data specifying coordinate values using nco 
```
ncks -d <coordinate_to_slice_along>,<coord_val_min>,<coord_val_max> input.nc output_for_coord_val.nc
# then remove singleton dimension
ncwa -a <singleton_coordinate_name> output_for_coord_val.nc output_for_coord_val_squeezed.nc
```

## Manipulating variables
Calculating Monthly Climatologies with nco
```
ncra -F -d time,1,-1,12 prec_2650-2999.E2pt1_PIctrl_restart.nc prec_mean_JAN.nc
ncra -F -d time,2,-1,12 prec_2650-2999.E2pt1_PIctrl_restart.nc prec_mean_FEB.nc
ncra -F -d time,3,-1,12 prec_2650-2999.E2pt1_PIctrl_restart.nc prec_mean_MAR.nc
```

remove a singleton dimension (i.e. dimension length = 1):
```
ncwa -a <dim_name> in.nc out.nc
```

## Attributes
delete global attributes:
```
ncatted -h -a history,global,d,, flor.ctrl.precip.nc
```
add global attributes:
```
ncatted -O -h -a <new_attr_name>,global,o,c,"<new_attr_content>" file.nc
```

renaming/adding variable attributes
```
ncatted -O -a long_name,toa_lw_all_clim,o,c,"NORTHWARD WIND VELOCITY" satellite_obs.monthly_climatologies.E2.1_grid.Mar2023.nc

ncatted -O -a long_name,level,a,c,"PRESSURE LEVEL" vwind.envelope_e2.1_amip.monthly.nc

ncatted -O -a units,level,a,c,"mb" vwind.envelope_e2.1_amip.monthly.nc

ncatted -O -a axis,level,a,c,"Z" vwind.envelope_e2.1_amip.monthly.nc

ncatted -O -a long_name,month,o,c,”MONTH” satellite_obs.monthly_climatologies.E2.1_grid.Mar2023.nc

ncatted -O -a comment,month,o,c,"JAN, FEB, MAR, APR, MAY, JUN, JUL, AUG, SEP, OCT, NOV, DEC" satellite_obs.monthly_climatologies.E2.1_grid.Mar2023.nc
```
