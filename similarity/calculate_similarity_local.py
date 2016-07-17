#!/usr/bin/python

# We want a metric to calculate similarity between images based on package folders.txt and files.txt

from singularity.package import package, calculate_similarity
from singularity.utils import check_install
from singularity.cli import Singularity
import pandas
from glob import glob
import os
import sys

base = '/home/vanessa/Documents/Work/SINGULARITY'
image_directory = '%s/docker2singularity' %(base)
package_directory = '%s/packages' %(base)
analysis_directory = '%s/analysis' %(base)

# We might have some output...
if not os.path.exists(analysis_directory):
    os.mkdir(analysis_directory)


# Check for Singularity installation
if check_install() != True:
    print("You must have Singularity installed to use this script!")
    sys.exit(32)

os.chdir(analysis_directory)

# Create a command line client
S = Singularity()

packages = glob("%s/*.zip" %(package_directory))

# Let's compare similarity using just folders, just files, and both
files = pandas.DataFrame(index=packages,columns=packages)
folders = pandas.DataFrame(index=packages,columns=packages)
both = pandas.DataFrame(index=packages,columns=packages)

# This will run on a local machine (slow!)
count=0
for pkg1 in packages:
    print("Calculating similarity for %s, %s of %s..." %(pkg1,count,len(packages)))
    for pkg2 in packages:
        if pkg1 != pkg2:

            # Folder similarity
            sim = calculate_similarity(pkg1,pkg2) # default uses just folders
            folders.loc[pkg1,pkg2] = sim
            folders.loc[pkg2,pkg1] = sim

            # Files similarity
            sim = calculate_similarity(pkg1,pkg2,include_folders=False,include_files=True)
            files.loc[pkg1,pkg2] = sim
            files.loc[pkg2,pkg1] = sim

            # Both
            sim = calculate_similarity(pkg1,pkg2,include_files=True)
            both.loc[pkg1,pkg2] = sim
            both.loc[pkg2,pkg1] = sim
        else:
            folders.loc[pkg1,pkg2] = 1.0
            files.loc[pkg1,pkg2] = 1.0
            both.loc[pkg1,pkg2] = 1.0
    count+=1
