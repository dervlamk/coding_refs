# Submitting batch jobs to the NASA GISS Discover HPC

## Creating and submitting batch jobs
Example batch job script that runs a python script:
```
#!/bin/bash
#SBATCH --job-name=<JOB_NAME>
#SBATCH --ntasks-per-node=1
#SBATCH --ntasks=46
#SBATCH --time=00:30:00
#SBATCH --error=<JOB_NAME>_err
#SBATCH --qos=allnccs
#SBATCH --account=s2689

source /usr/share/modules/init/bash

module load anaconda
source activate <ENV_NAME>
python <SCRIPT_NAME>.py
```

to run: `sbatch ./<RUN_BATCH_JOB_SCRIPT_NAME>.sh`


## Checking on jobs

see status of jobs: `qstat -u dmkumar`
<br>
get information about a job: `qrsf <JOB_ID>`
<br>
delete a job: `qdel <JOB_ID_NUMBER>`
<br>
see all jobs currently in queue: `qb`
