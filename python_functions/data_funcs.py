import os
import sys
import xarray as xr
import netCDF4 as nc
import numpy as np
import metpy.calc as mp
from datetime import datetime


#############################

def get_xy_coords(var):
    """
    Get lon and lat arrays without knowing coordinate names
    """
    if isinstance(var, xr.DataArray):
        x,y=var.metpy.coordinates('x','y')
        return(x,y)
    if isinstance(var, xr.Dataset):
        print('This is a dataset. Please use an xarray DataArray')

def get_season(season='ann'):
    """
    Index months to average over to derive an annual or seasonal mean
        - can only be applied to monthly climatologies
    """
    mons = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    if season in ['ANNUAL', 'ANN', 'ann']:
        mons = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    if season in ['DJF', 'djf']:
        mons = [0, 1, 11]
    if season in ['JJA', 'jja']:
        mons = [5, 6, 7]
    if season in ['JJAS', 'jjas']:
        mons = [5, 6, 7, 8]
    if season in ['JFM', 'jfm']:
        mons = [0, 1, 2]
    if season in ['JAS', 'jas']:
        mons = [6, 7, 8]
    if season==None:
        pass
    return mons

def longitude_flip(var,how):
    """
    Convert longitude values from the -180:180 to 0:360 convention or vice versa.
        
    Notes
    ----------
    Only works for global data. Do not apply to data with a clipped longitude range
        
    Parameters
    ----------
    var : Data Array
    how : 180 or 360
            how==180 will convert 0:360 longitudes to -180:180 longitudes
            how==360 will convert -180:180 longitudes to 0:360 longitudes 
    """    
    # get var info
    x,_=get_xy_coords(var)
    lon_name=x.name
    # FLIP LONGITUDES FROM 0:360 to -180:180
    if how==180:
        # if negative longitudes already exist, no need to flip them
        if min(x)<0:
            print('Longitudes are likely already in -180:180 format.\n', x)
        # otherwise flip longitudes
        elif min(x)>=0:
            # determine the number of values in the original longitude coord
            nx=len(x)
            # shift the data by 180°
            nshift=nx//2
            var=var.roll({lon_name: nshift}, roll_coords=False)
            # create an array of longitudes spanning -180:180 with the same length as original longitude coord 
            new_lons=np.linspace((min(x)-180), (max(x)-180), nx)
            # update longitude coord with new values
            var=var.assign_coords({lon_name: new_lons})
            # add attributes documenting change
            timestamp=datetime.now().strftime("%B %d, %Y, %r")
            var.attrs['history']=f'{timestamp} flipped longitude convention from 0°:360° to -180°:180°'
            var.attrs['original_lons']=x.values
            return(var)
    # FLIP LONGITUDES FROM -180:180 to 0:360
    if how==360:
        # if all longitudes are already greater than 0, no need to flip them
        if min(x)>=0:
            print('Longitudes are likely already in 0:360 format. Double check your input:\n', x)
        # otherwise flip longitudes
        elif min(x)<0:
            # determine the number of values in the original longitude coord
            nx=len(x)
            # shift the data by 180° of longitude
            nshift=nx//2
            var=var.roll({lon_name: nshift}, roll_coords=False)
            # create an array of longitudes spanning 0:360 with the same length as original longitude coord 
            new_lons=np.linspace((min(x)+180), (max(x)+180), nx)
            # update longitude coord with new values
            var=var.assign_coords({lon_name: new_lons})
            # add attributes documenting change
            timestamp=datetime.now().strftime("%B %d, %Y, %r")
            var.attrs['history']=f'{timestamp} flipped longitude convention from -180°:180° to 0°:360°'
            var.attrs['original_lons']=x.values
            return(var)

def latitude_weighted_mean(var):
    """
    Calculate the mean of geospatial data taking into account unequal grid cell area
    """
    # get x and y coordinate data
    lons,lats = get_xy_coords(var)
    # determine weight based on latitude value
    weights = np.cos(np.deg2rad(lats))
    weights.name = 'weights'
    # calculate area-weighted values
    weighted_var = var.weighted(weights)
    # calculate global mean of weighted data
    weighted_mean = weighted_var.mean(dim=[lats.name,lons.name], keep_attrs=True)
    return(weighted_mean)
