#!/usr/bin/python

from singularity.package import calculate_similarity
from singularity.utils import check_install
import pickle
import sys
import os

pkg1 = sys.argv[1]
pkg2 = sys.argv[2]
output_file = sys.argv[3]

# Check for Singularity installation
if check_install() != True:
    print("You must have Singularity installed to use this script!")
    sys.exit(32)

print("Calculating similarity for %s, %s of %s..." %(pkg1,count,len(packages)))

sims = dict()

# Calculate similarities
sims["folder"] = calculate_similarity(pkg1,pkg2) # default uses just folders
sims["files"] = calculate_similarity(pkg1,pkg2,include_folders=False,include_files=True)
sims["both"] = calculate_similarity(pkg1,pkg2,include_files=True)

# Save to output file
pickle.dump(sims,open(output_file,"wb"))
