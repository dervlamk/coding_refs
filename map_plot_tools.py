import xarray as xr
import numpy as np
import metpy.calc as mp

import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from shapely.geometry.polygon import LinearRing

import matplotlib as mpl
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.ticker as mticker
from matplotlib import cm
import matplotlib.colors as mcolors
from matplotlib.colors import ListedColormap,LinearSegmentedColormap
import cmocean
import cmocean.cm as cmo
import colorcet as cc

from colorbar_funcs import *


#############################


def get_season(season='ann'):
    """
    This indexes which months to average over to derive an annual or seasonal mean
        - can only be applied to monthly climatologies
    """
    mons = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    if season in ['ANNUAL', 'ANN', 'annual', 'ann']:
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

###


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

###

def quick_map(var, season='ann', field=None, diff=False, cbar=True, mask=None, mask_color='w', boundaries=None, label=None, ax=None):
    
    ### +++ GET VAR INFO +++ ###
    lons,lats = get_xy_coords(var) # get lat & lon coords without having to know coordinate names

    ## need to figure out how to write an if statement to only do this if there is a time/month variable
    if season!=None:
        mons = get_season(season=season) # index months to average over based on season var
        var_avg = var[mons].mean(dim='month', keep_attrs=True) # find seasonal or annual var mean
    else:
        var_avg=var

    ### +++ INITIALIZE FIGURE +++ ###
    trans = ccrs.PlateCarree()
    proj = ccrs.PlateCarree(central_longitude=180)
    # create a new figure if no axes are designated
    if ax==None:
        fig = plt.figure(figsize=(9, 6))
        ax = plt.subplot(111, projection=proj)

    ### +++ MAP & BOUNDARY INFO +++ ###
    # add optional masks
    if mask != None:
        if mask in ['land', 'Land']:
            ax.add_feature(cfeature.LAND, fc=mask_color, zorder=2) # masks continents
        if mask in ['ocean', 'Ocean']:
            ax.add_feature(cfeature.OCEAN, fc=mask_color, zorder=2) # masks oceans
    # map boundaries
    if boundaries != None:
        ax.set_extent(boundaries, crs=trans) # clips map extent according to designated boundaries
    else:
        ax.set_global() # make a global map
    # add coastlines
    ax.coastlines()
    # grid line specs
    gl = ax.gridlines(crs=trans, lw=.5, colors='black', alpha=1.0, linestyle='--', zorder=10, draw_labels=True)
    gl.top_labels=False
    gl.right_labels=False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.xlabel_style = {'color': 'black', 'weight': 'bold'}
    gl.ylabel_style = {'color': 'black', 'weight': 'bold'}

    ### +++ COLORMAP INFO +++ ###
    cmap, vmin, vmax, cf = get_settings(field=field, diff=diff)

    ### +++ PLOT CONTOURS +++ ###
    ax.pcolormesh(lons, lats, var_avg, cmap=cmap, vmin=vmin, vmax=vmax, transform=trans)

    ### +++ ADD FIG LABEL +++ ###
    if label==None:
        label=var_avg.name
    else:
        label=label
    t=ax.annotate(label,
                  xy=(0.015, 0.025), xycoords='axes fraction',
                  annotation_clip=False,
                  fontsize=12, fontweight='bold', ha='left', va='bottom')
    t.set_bbox(dict(facecolor='white', alpha=1, edgecolor='k'))

    ### +++ COLORBAR INFO +++ ###
    if cbar==True:
        cbar = plt.colorbar(cf,
                            extend='both',
                            orientation='vertical',
                            shrink=0.4,
                            location='right',
                            pad=0.01,
                            ax=ax
                            )
        if 'units' in var.attrs:
            clb = '['+var.attrs['units']+']'
            cbar.set_label(clb, labelpad=15, rotation=270, fontweight='bold', ha='center')
        cbar.ax.tick_params(labelsize=10)
        for tick in cbar.ax.yaxis.get_major_ticks():
            tick.label2.set_fontweight('bold')
    else:
        pass



###

def custom_map(var, season='ann', vmin=None, vmax=None, cmap=None, cbar=True, mask=None, mask_color='w', boundaries=None, ax=None):
    
    ### +++ GET VAR INFO +++ ###
    lons,lats = get_xy_coords(var) # get lat & lon coords without having to know coordinate names
    if season!=None:
        mons = get_season(season=season) # index months to average over based on season var
        var_avg = var[mons].mean(dim='month', keep_attrs=True) # find seasonal or annual var mean
    else:
        var_avg=var

    ### +++ INITIALIZE FIGURE +++ ###
    trans = ccrs.PlateCarree()
    proj = ccrs.PlateCarree()
    # create a new figure if no axes are designated
    if ax==None:
        fig = plt.figure(figsize=(9, 6))
        ax = plt.subplot(111, projection=proj)

    ### +++ MAP & BOUNDARY INFO +++ ###
    # add optional masks
    if mask != None:
        if mask in ['land', 'Land']:
            ax.add_feature(cfeature.LAND, fc=mask_color, zorder=2) # masks continents
        if mask in ['ocean', 'Ocean']:
            ax.add_feature(cfeature.OCEAN, fc=mask_color, zorder=2) # masks oceans
    # map boundaries
    if boundaries != None:
        ax.set_extent(boundaries, crs=trans) # clips map extent according to designated boundaries
    else:
        ax.set_global() # make a global map
    # add coastlines
    ax.coastlines()
    # grid line specs
    gl = ax.gridlines(crs=trans, lw=.5, colors='black', alpha=1.0, linestyle='--', zorder=10, draw_labels=True)
    gl.top_labels=False
    gl.right_labels=False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.xlabel_style = {'color': 'black', 'weight': 'bold'}
    gl.ylabel_style = {'color': 'black', 'weight': 'bold'}

    ### +++ COLORMAP INFO +++ ###
    if ((cmap==None) and (var_avg.min()<0)):
        cmap=plt.colormaps['RdBu']
    elif ((cmap==None) and (var_avg.min()>=0)):
        cmap=plt.colormaps['viridis_r']

    ### +++ PLOT CONTOURS +++ ###
    if ((vmin!=None) and (vmax!=None)):
        vn=vmin
        vx=vmax
        n_lvls = 2*(vx-vn)+1
        levels = np.linspace(vn, vx, n_lvls)
        norm = mpl.colors.BoundaryNorm(levels, cmap.N)
        cf = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)
        ax.pcolormesh(lons, lats, var_avg, cmap=cmap, vmin=vn, vmax=vx, transform=trans)
    else:
        if vmin==None:
            vn=var_avg.min()
        if vmax==None:
            vx=var_avg.max()
        cf = ax.pcolormesh(lons, lats, var_avg, cmap=cmap, vmin=vn, vmax=vx, transform=trans)
    t=ax.annotate(var_avg.name,
                  xy=(0.015, 0.025), xycoords='axes fraction',
                  annotation_clip=False,
                  fontsize=12, fontweight='bold', ha='left', va='bottom')
    t.set_bbox(dict(facecolor='white', alpha=1, edgecolor='k'))

    ## colorbar info
    if cbar==True:
        cbar = plt.colorbar(cf,
                            extend='both',
                            orientation='vertical',
                            shrink=0.4,
                            location='right',
                            pad=0.01,
                            ax=ax
                            )
        if 'units' in var.attrs:
            clb = '['+var.attrs['units']+']'
            cbar.set_label(clb, labelpad=15, rotation=270, fontweight='bold', ha='center')  
        cbar.ax.tick_params(labelsize=10)
        for tick in cbar.ax.yaxis.get_major_ticks():
            tick.label2.set_fontweight('bold')
    else:
        pass

    ###
    #plt.show()
    #return(ax)


###


def plot_field_diff(var1, var2, season='ann',
                    vmin_fld=None, vmax_fld=None, cmap_fld=None,
                    vmin_diff=None, vmax_diff=None, cmap_diff=None,
                    mask=None, boundaries=None, cl=None,
                    var1_name='', var2_name='',
                    save=False, ofile=None):
    
    ## initialize figure
    trans = ccrs.PlateCarree()
    if cl != None:
        proj = ccrs.PlateCarree(central_longitude=cl)
    else:
        proj = ccrs.PlateCarree()
    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(20,4), subplot_kw={'projection': proj})
    fig.subplots_adjust(bottom=0.05, top=0.95)
    # add figure title
    #plt.gcf().text(.5, .85, (var1.attrs['long_name']+' ('+season+')'), fontsize=16, fontweight='bold', ha='center', va='center')
    plt.suptitle((var1.attrs['long_name']+' ('+season+')'), fontsize=16, fontweight='bold', ha='center', va='center')

    ## get var info
    lons, lats = get_xy_coords(var1) # get lat & lon coords without having to know coordinate names
    mons = get_season(season=season) # index months to average over based on season var
    # find seasonal or annual var mean
    var_avg1 = var1[mons].mean(dim='month', keep_attrs=True) 
    var_avg2 = var2[mons].mean(dim='month', keep_attrs=True) 
    
    ## colormamp info
    if ((cmap_fld==None) and (var_avg1.min()<0)):
        cmap_fld=plt.colormaps['RdBu']
    if ((cmap_fld==None) and (var_avg1.min()>=0)):
        cmap_fld=plt.colormaps['viridis_r']
    if cmap_diff==None:
        cmap_diff=plt.colormaps['RdBu']
    
    ## plot contours for fields
    if ((vmin_fld!=None) and (vmax_fld!=None)):
        vn_fld=vmin_fld
        vx_fld=vmax_fld
        n_lvls_fld = 2*(vx_fld-vn_fld)+1
        levels_fld = np.linspace(vn_fld, vx_fld, n_lvls_fld)
        norm_fld = mpl.colors.BoundaryNorm(levels_fld, cmap_fld.N)
        cf_fld = mpl.cm.ScalarMappable(norm=norm_fld, cmap=cmap_fld)
        ax[0].pcolormesh(lons, lats, var_avg1, cmap=cmap_fld, vmin=vn_fld, vmax=vx_fld, transform=trans)
        t=ax[0].annotate(var1_name, xy=(0.015, 0.025), xycoords='axes fraction', annotation_clip=False, fontsize=10, fontweight='bold', ha='left', va='bottom')
        t.set_bbox(dict(facecolor='white', alpha=1, edgecolor='k'))
        ax[1].pcolormesh(lons, lats, var_avg2, cmap=cmap_fld, vmin=vn_fld, vmax=vx_fld, transform=trans)
        t=ax[1].annotate(var2_name, xy=(0.015, 0.025), xycoords='axes fraction', annotation_clip=False, fontsize=10, fontweight='bold', ha='left', va='bottom')
        t.set_bbox(dict(facecolor='white', alpha=1, edgecolor='k'))
    else:
        if vmin_fld==None:
            vn_fld=var_avg1.min()
        if vmax_fld==None:
            vx_fld=var_avg1.max()
        cf = ax[0].pcolormesh(lons, lats, var_avg1, cmap=cmap_fld, vmin=vn_fld, vmax=vx_fld, transform=trans)
        t=ax[0].annotate(var1_name, xy=(0.015, 0.025), xycoords='axes fraction', annotation_clip=False, fontsize=10, fontweight='bold', ha='left', va='bottom')
        t.set_bbox(dict(facecolor='white', alpha=1, edgecolor='k'))
        ax[1].pcolormesh(lons, lats, var_avg2, cmap=cmap_fld, vmin=vn_fld, vmax=vx_fld, transform=trans)
        t=ax[1].annotate(var2_name, xy=(0.015, 0.025), xycoords='axes fraction', annotation_clip=False, fontsize=10, fontweight='bold', ha='left', va='bottom')
        t.set_bbox(dict(facecolor='white', alpha=1, edgecolor='k'))
        
    ## plot contours for difference
    var_diff=var_avg2-var_avg1
    if ((vmin_diff!=None) and (vmax_diff!=None)):
        vn_diff=vmin_diff
        vx_diff=vmax_diff
        n_lvls_diff = 2*(vx_diff-vn_diff)+1
        levels_diff = np.linspace(vn_diff, vx_diff, n_lvls_diff)
        norm_diff = mpl.colors.BoundaryNorm(levels_diff, cmap_diff.N)
        cf_diff = mpl.cm.ScalarMappable(norm=norm_diff, cmap=cmap_diff)
        ax[2].pcolormesh(lons, lats, var_diff, cmap=cmap_diff, vmin=vn_diff, vmax=vx_diff, transform=trans)
        t=ax[2].annotate(f'{var2_name}$-${var1_name}', xy=(0.015, 0.025), xycoords='axes fraction', annotation_clip=False, fontsize=10, fontweight='bold', ha='left', va='bottom')
        t.set_bbox(dict(facecolor='white', alpha=1, edgecolor='k'))
    else:
        if vmin_diff==None:
            vn_diff=var_diff.min()
        if vmax_diff==None:
            vx_diff=var_diff.max()
        cf = ax[2].pcolormesh(lons, lats, var_diff, cmap=cmap_diff, vmin=vn_diff, vmax=vx_diff, transform=trans)
        t=ax[2].annotate(f'{var2_name}$-${var1_name}', xy=(0.015, 0.025), xycoords='axes fraction', annotation_clip=False, fontsize=10, fontweight='bold', ha='left', va='bottom')
        t.set_bbox(dict(facecolor='white', alpha=1, edgecolor='k'))
    
    for i in [0,1,2]:
        ## map & boundary info
        # add optional masks
        if mask != None:
            if mask in ['land', 'Land']:
                ax[i].add_feature(cfeature.LAND, fc=(1, 1, 1), zorder=2) # masks continents
            if mask in ['ocean', 'Ocean']:
                ax[i].add_feature(cfeature.OCEAN, fc=(1, 1, 1), zorder=2) # masks oceans
        # map boundaries
        if boundaries != None:
            ax[i].set_extent(boundaries, crs=trans) # clips map extent according to designated boundaries
        else:
            ax[i].set_global() # make a global map
        # add coastlines
        ax[i].coastlines()
        # grid line specs
        gl = ax[i].gridlines(crs=trans,
                             lw=.5,
                             colors='black',
                             alpha=1.0,
                             linestyle='--',
                             zorder=10,
                             draw_labels=True)
        gl.top_labels=False
        gl.right_labels=False
        gl.xformatter = LONGITUDE_FORMATTER
        gl.yformatter = LATITUDE_FORMATTER
        gl.xlabel_style = {'color': 'black', 'weight': 'bold'}
        gl.ylabel_style = {'color': 'black', 'weight': 'bold'}
    
        ## colorbar info
        if 'units' in var_avg1.attrs:
            clb = var_avg1.attrs['units']
        if i in [0,1]:
            cbar = plt.colorbar(cf_fld,
                                extend='both',
                                orientation='horizontal',
                                shrink=0.9,
                                location='bottom',
                                pad=0.075,
                                ax=ax[i])
            cbar.set_label(clb, labelpad=5, y=1, rotation=0, fontweight='bold')
            cbar.ax.tick_params(labelsize=10)
            for tick in cbar.ax.xaxis.get_major_ticks():
                tick.label1.set_fontweight('bold')
        else:
            cbar = plt.colorbar(cf_diff,
                                extend='both',
                                orientation='horizontal',
                                shrink=0.9,
                                location='bottom',
                                pad=0.075,
                                ax=ax[i])
            cbar.set_label(clb, labelpad=5, y=1, rotation=0, fontweight='bold')
            cbar.ax.tick_params(labelsize=10)
            for tick in cbar.ax.xaxis.get_major_ticks():
                tick.label1.set_fontweight('bold')

    ###
    plt.show()

    if save is True:
            plt.savefig('{}.pdf'.format(ofile),
                        dpi=None, facecolor='w', edgecolor='w',
                        orientation='portrait', papertype=None,
                        format=None, transparent=False,
                        bbox_inches='tight', pad_inches=0.1)