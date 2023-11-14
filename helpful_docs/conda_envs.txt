## How to create a conda environment from a .yml file in terminal
# first create a new .yml file (I use visual studio code for this) and save it in your anaconda envs directory:
~/opt/anaconda3/envs

# cd to the directory where it is saved and issue the command:
conda env create --name <env_name> --file=<env_name>.yml

# activate the environment:
conda activate <env_name>

# create an ipykernel kernel so that you can load the env in Jupyter notebooks: 
python -m ipykernel install --user --name <env_name> --display-name "Python (<env_name>)"

# deactivate the environment:
conda deactivate <env_name>

# if you want to add packages to the environment after the fact, activate the environment then issue the command:
conda activate <env_name>
conda install -c conda-forge <package_name>

-----

## List all packages installed to an environment
conda activate <env_name>
conda list

-----

## List only the packages you explicitly installed to an environment
conda activate <env_name>
conda env export --from-history

-----

## Uninstall a package from an environment
conda remove -n <env_name> <package_name>
