import sys
sys.dont_write_bytecode = True

import xarray as xr
import numpy as np

import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import cm
import matplotlib.colors as mcolors
from matplotlib.colors import ListedColormap,LinearSegmentedColormap
import cmocean


###

def clip_cmap(cmap, l_bnd, u_bnd):
    """
    Define a new colormap by clipping a standard matplotlib or cmocean colormap
    - be cautious when applying to divergent colormaps if clipping unequally from both ends
    """
    cmap_full = cmap
    cmap_clip = ListedColormap(cmap_full(np.linspace(l_bnd, u_bnd)))
    return(cmap_clip)

###

def combine_cmaps(cmap_low, cmap_up, range_low=[0,1], range_up=[0,1], n_low=128, n_up=128):
    """
    Stack two colormaps to form a new colormap
    """
    # use the range values to determine the fraction of the original cmap to clip off and sample n colors from new range
    lower_colors = cmap_low(np.linspace(range_low[0], range_low[1], n_low))
    upper_colors = cmap_up(np.linspace(range_up[0], range_up[1], n_up))
    # combine them and build a new colormap
    colors = np.vstack((lower_colors, upper_colors))
    new_cmap = mcolors.LinearSegmentedColormap.from_list('new_cmap', colors)
    return(new_cmap)

###

def get_settings(field=None, diff=False):
    """
    Determines bounds, levels, and colormap for various climate model fields
    """
    ################################
    #   +++ ATMOSPHERIC VARS +++   
    #### 
    if field in ['prec', 'precip', 'precipiation']:
        if diff==False:
            cmap=plt.colormaps['Blues']
            vmin=0
            vmax=10
            lvls=21
        if diff==True:
            cmap=combine_cmaps(plt.colormaps['BrBG'], plt.colormaps['Blues'], range_low=[0,.5], range_up=[0,.95], n_low=128, n_up=128)
            vmin=-6
            vmax=6
            lvls=25

    if field in ['ts', 'tsurf', 't', 'temp', 'temperature']:
        if diff==False:
            cmap=plt.colormaps['RdYlBu_r']
            vmin=-30
            vmax=30
            lvls=21
        if diff==True:
            cmap=plt.colormaps['RdBu_r']
            vmin=-10
            vmax=10
            lvls=21

    if field in ['u', 'U', 'uwind', 'usurf', 'v', 'V', 'vwind', 'vsurf']:
        if diff==False:
            cmap=combine_cmaps(plt.colormaps['YlOrBr_r'], plt.colormaps['BuPu'], range_low=[0,1], range_up=[0,1], n_low=128, n_up=128)
            vmin=-10
            vmax=10
            lvls=21
        if diff==True:
            cmap=plt.colormaps['RdBu_r']
            vmin=-5
            vmax=5
            lvls=11
    
    if field in ['sfc_wind_speed', 'sfcWind', 'sfcwind', 'sfc_wind', 'wsurf']:
        if diff==False:
            cmap=cmocean.cm.matter_r
            vmin=4
            vmax=11
            lvls=31
        if diff==True:
            cmap=plt.colormaps['RdBu_r']
            vmin=-10
            vmax=10
            lvls=21
    
    if field in ['mfc', 'moist_flux_convergence', 'mfcvg', 'mf_cvg', 'vimfc']:
        if diff==False:
            cmap=combine_cmaps(plt.colormaps['YlOrBr_r'], cmocean.cm.tempo_r, range_low=[0,1], range_up=[0,1], n_low=128, n_up=128) 
            vmin=-0.00006
            vmax=0.00006
            lvls=25
        if diff==True:
            cmap=combine_cmaps(plt.colormaps['YlOrBr_r'], cmocean.cm.tempo_r, range_low=[0,1], range_up=[0,1], n_low=128, n_up=128)
            vmin=-0.00004
            vmax=0.00004
            lvls=17
    
    if field in ['rh', 'rel_hum', 'relative_humidity']:
        if diff==False:
            cmap=clip_cmap(cmocean.cm.delta_r, 0.5, 1.0)
            vmin=0
            vmax=100
            lvls=21
        if diff==True:
            cmap=combine_cmaps(plt.colormaps['BrBG'], cmocean.cm.delta_r, range_low=[0,0.45], range_up=[0.52,1.0], n_low=128, n_up=128)
            vmin=-50
            vmax=50
            lvls=21
    
    if field in ['sh', 'qv', 'q', 'Q', 'QV', 'specific_humidity']:
        if diff==False:
            cmap=clip_cmap(cmocean.cm.delta_r, 0.5, 1.0)
            vmin=0
            vmax=100
            lvls=21
        if diff==True:
            cmap=combine_cmaps(plt.colormaps['BrBG'], cmocean.cm.delta_r, range_low=[0,0.45], range_up=[0.52,1.0], n_low=128, n_up=128)
            vmin=-50
            vmax=50
            lvls=21
    
    if field in ['cvg', 'convergence']:
        if diff==False:
            cmap=['RdBu']
            vmin=-5e-05
            vmax=5e-05
            lvls=21
        if diff==True:
            cmap=['RdBu']
            vmin=-5e-06
            vmax=5e-06
            lvls=21
    
    if field in ['div', 'dvg', 'divergence']:
        if diff==False:
            cmap=['RdBu_r']
            vmin=-5e-05
            vmax=5e-05
            lvls=21
        if diff==True:
            cmap=['RdBu_r']
            vmin=-5e-05
            vmax=5e-05
            lvls=21
    
    if field in ['omega', 'w']:
        if diff==False:
            cmap=cmocean.cm.curl
            vmin=-0.1
            vmax=0.1
            lvls=21
        if diff==True:
            cmap=cmocean.cm.curl
            vmin=-0.05
            vmax=0.05
            lvls=21
    
    if field in ['lh_flux', 'LH', 'lhf']:
        if diff==False:
            cmap=cmocean.cm.amp
            vmin=0
            vmax=300
            lvls=16
        if diff==True:
            cmap=plt.colormaps['RdBu_r']
            vmin=-100
            vmax=100
            lvls=21
    
    if field in ['sh_flux', 'SH', 'shf']:
        if diff==False:
            cmap=plt.colormaps['RdBu_r']
            vmin=-100
            vmax=100
            lvls=21
        if diff==True:
            cmap=plt.colormaps['RdBu_r']
            vmin=-20
            vmax=20
            lvls=21
    
    if field in ['cloud', 'cloud_frac', 'fcloud', 'pcldl', 'pcldm', 'pcldh', 'pcldt']:
        if diff==False:
            cmap=cmocean.cm.ice
            vmin=0
            vmax=100
            lvls=21
        if diff==True:
            cmap=cmocean.cm.diff
            vmin=-20
            vmax=20
            lvls=21
    
    if field in ['sw_flux', 'sw_toa', 'swcrf']:
        if diff==False:
            cmap=cmocean.cm.thermal_r
            vmin=-100
            vmax=0
            lvls=21
        if diff==True:
            cmap=combine_cmaps(cmocean.cm.gray, cmocean.cm.amp, range_low=[.1,.95], range_up=[0,.95], n_low=128, n_up=128)
            vmin=-50
            vmax=50
            lvls=21
    
    if field in ['lw_flux', 'lw_toa', 'lwcrf']:
        if diff==False:
            cmap=cmocean.cm.thermal
            vmin=0
            vmax=100
            lvls=21
        if diff==True:
            cmap=combine_cmaps(plt.colormaps['bone'], cmocean.cm.amp, range_low=[.1,.95], range_up=[0,.95], n_low=128, n_up=128)
            vmin=-50
            vmax=50
            lvls=21

    if field in ['slp', 'pressure']:
        if diff==False:
            cmap=plt.colormaps['RdBu']
            vmin=975
            vmax=1025
            lvls=11
        if diff==True:
            cmap=plt.colormaps['RdBu']
            vmin=-10
            vmax=10
            lvls=11
    
    if field in ['z200', 'z700', 'z_200', 'z_700', 'stationary_wave']:
        if diff==False:
            cmap=plt.colormaps['seismic']
            vmin=-150
            vmax=150
            lvls=31
        if diff==True:
            cmap=plt.colormaps['seismic']
            vmin=-30
            vmax=30
            lvls=21
    
    ##########################
    #   +++ OCEAN VARS +++   
    ####                        
    if field in ['sst', 'SST', 'sea_surface_temperature', 'sea_surface_temp']:
        if diff==False:
            cmap=plt.colormaps['RdYlBu_r']
            vmin=-5
            vmax=30
            lvls=36
        if diff==True:
            cmap=plt.colormaps['RdBu_r']
            vmin=-10
            vmax=10
            lvls=21
    
    if field in ['ice', 'seaice', 'seaIce', 'oicefr']:
        if diff==False:
            cmap=cmocean.cm.ice
            vmin=0
            vmax=100
            lvls=26
        if diff==True:
            cmap=plt.colormaps['RdBu']
            vmin=-50
            vmax=50
            lvls=26
    
    if field in ['ocean_streamfunction', 'sf_Atl', 'sf_atl', 'sf_pac', 'sf_ind', 'sf_Pac', 'sf_Ind', 'sf_ocn']:
        if diff==False:
            cmap=plt.colormaps['YlGnBu']
            vmin=-10
            vmax=30
            lvls=21
        if diff==True:
            cmap=cmocean.cm.delta_r
            vmin=-20
            vmax=20
            lvls=21

    ##########################
    #   +++ OTHER VARS +++   
    #### 
    if field in ['topo_real', 'topo', 'topography', 'surface_height', 'zatmo', 'zsurf']:
        if diff==False:
            cmap=clip_cmap(cmocean.cm.topo, 0.5, 1.0)
            vmin=0
            vmax=5000
            lvls=26
        if diff==True:
            cmap=combine_cmaps(plt.colormaps['twilight_shifted'], plt.colormaps['afmhot_r'], range_low=[0,0.5], range_up=[0,1.0], n_low=128, n_up=128)
            vmin=-2000
            vmax=2000
            lvls=21

    if field in ['bathymetry', 'bathy', 'depth']:
        if diff==False:
            cmap=cmocean.cm.deep_r
            vmin=-4000
            vmax=0
            lvls=21
        if diff==True:
            cmap=cmocean.cm.diff
            vmin=-1000
            vmax=1000
            lvls=21
    
    else:
        print('Field not recognized')
    
    # save output
    levels = np.linspace(vmin, vmax, lvls)
    norm = mpl.colors.BoundaryNorm(levels, cmap.N)
    cf = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)
    return(cmap, vmin, vmax, cf)
    