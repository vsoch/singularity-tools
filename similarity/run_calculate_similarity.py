#!/usr/bin/python

from singularity.package import calculate_similarity
from singularity.utils import check_install
from glob import glob
import pandas
import sys
import os

base = '/scratch/users/vsochat/DATA/SINGULARITY'
package_folder = '%s/packages' %(base)
analysis_folder = '%s/analysis' %(base)
output_folder = '%s/scores' %(base)

for folder in [analysis_folder,output_folder]:
    if not os.path.exists(folder):
        os.mkdir(folder)

# Check for Singularity installation
if check_install() != True:
    print("You must have Singularity installed to use this script!")
    sys.exit(32)

# if you are on a cluster and it should be installed, try adding 
# module load singularity to your .bash_profile or .modules file
# that is sourced

packages = glob("%s/*.zip" %(package_folder))
print("Found %s packages!" %(len(packages)))

for pkg1 in packages:
    print "Parsing %s" %(pkg1)
    pkg1_name = os.path.basename(pkg1)
    for pkg2 in packages:
        pkg2_name = os.path.basename(pkg2)
        if (pkg1 != pkg2) and (pkg1 < pkg2):
            output_file = "%s/%s_%s_score.pkl" %(output_folder,pkg1_name,pkg2_name)
            if not os.path.exists(output_file):
                job_id = "%s_%s" %(pkg1_name,pkg2_name)
                filey = ".job/%s.job" %(job_id)
                filey = open(filey,"w")
                filey.writelines("#!/bin/bash\n")
                filey.writelines("#SBATCH --job-name=%s\n" %(job_id))
                filey.writelines("#SBATCH --output=.out/%s.out\n" %(job_id))
                filey.writelines("#SBATCH --error=.out/%s.err\n" %(job_id))
                filey.writelines("#SBATCH --time=0-08:00\n")
                filey.writelines("#SBATCH --mem=6000\n")
                filey.writelines("python calculate_similarity.py %s %s %s" %(pkg1, pkg2, output_file))
                filey.close()
                os.system("sbatch -p russpold --qos russpold " + ".job/%s.job" %(job_id))
