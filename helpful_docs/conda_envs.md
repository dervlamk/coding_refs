# How to create a conda environment from a .yml file in terminal
first create a new .yml file (I use visual studio code for this) and save it in your anaconda envs directory: `~/opt/anaconda3/envs`
<br>
**Example .yml file:**
```
name: climate
channels:
  - conda-forge
  - defaults
dependencies:
  - numpy
  - xarray
  - netcdf4
  - cartopy
  - ncview
  - nco
  - cdo
  - bottleneck
  - ipykernel
  - matplotlib
  - cmocean
  - seaborn
  - metpy
```

cd to `~/opt/anaconda3/envs` and generate the environment:
```
conda env create --name <env_name> --file=<env_name>.yml
```

activate the environment:
```
conda activate <env_name>
```

create an ipykernel kernel so that you can load the env in Jupyter notebooks: 
```
python -m ipykernel install --user --name <env_name> --display-name "Python (<env_name>)"
```

deactivate the environment:
```
conda deactivate <env_name>
```
<br>

# Modifying an environment
add packages to an environment:
```
conda activate <env_name>
conda install -c conda-forge <package_name>
```

Uninstall a package from an environment
```
conda remove -n <env_name> <package_name>
```

<br>

# See what's installed to an environment
List all packages installed to an environment
```
conda activate <env_name>
conda list
```

List only the packages you explicitly installed to an environment
```
conda activate <env_name>
conda env export --from-history
```