import xarray as xr
import numpy as np
import metpy.calc as mp

import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from shapely.geometry.polygon import LinearRing

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.ticker as mticker
from matplotlib import cm
from matplotlib.colors import ListedColormap,LinearSegmentedColormap
import cmocean
import cmocean.cm as cmo
import colorcet as cc

#############################

def get_season(season='ann'):
    """
    This indexes which months to average over to derive an annual or seasonal mean
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
        mons = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    return mons

def get_xy_coords(var):
    """
    This extracts the lat and lon coordinates without having to know the specific coordinate names
    """
    if isinstance(var, xr.DataArray):
        x = var.metpy.x
        y = var.metpy.y
        return(x,y)
    if isinstance(var, xr.Dataset):
        print('This is a dataset. Please use an xarray DataArray')

def weighted_global_mean(var):
    """
    This weights var data to account for unequal grid cell areas that are a function of latitude,
    then calculates a global mean timeseries
    """
    # find latitude variable
    lons=var.metpy.x
    lats=var.metpy.y
    # determine weight based on latitude value
    weights = np.cos(np.deg2rad(lats))
    weights.name = 'weights'
    # calculate area-weighted values
    weighted_var = var.weighted(weights)
    # calculate global mean of weighted data
    weighted_global_mean = weighted_var.mean(dim=[lats.name,lons.name], keep_attrs=True)
    return(weighted_global_mean)
