#!/usr/bin/python

# Combine similarity calculations for 109 images for files, folders, and both

from glob import glob
import pandas
import pickle
import os

base = '/scratch/users/vsochat/DATA/SINGULARITY'
scores_folder = '%s/scores' %(base)
packages_folder = '%s/packages' %(base)
results_folder = '%s/results' %(base)
scores = glob("%s/*.pkl" %(scores_folder))
packages = [os.path.basename(x) for x in glob("%s/*.zip" %(packages_folder))]

if not os.path.exists(results_folder):
    os.mkdir(results_folder)

# compared similarity using just folders, just files, and both
files = pandas.DataFrame(index=packages,columns=packages)
folders = pandas.DataFrame(index=packages,columns=packages)
both = pandas.DataFrame(index=packages,columns=packages)

for s in range(len(scores)):
    print("Parsing %s of %s" %(s,len(scores)))
    score = scores[s]
    result = pickle.load(open(score,'rb'))
    pkg1,pkg2 = os.path.basename(score).replace("_score.pkl","").split("_")
    files.loc[pkg1,pkg2] = result["files"]
    files.loc[pkg2,pkg1] = result["files"]
    folders.loc[pkg1,pkg2] = result["folder"]
    folders.loc[pkg2,pkg1] = result["folder"]
    both.loc[pkg1,pkg2] = result["both"]
    both.loc[pkg2,pkg1] = result["both"]

# The remaining not calculated (NaN) are with values == 1 on the diagonal
files[files.isnull()] = 1.0
folders[folders.isnull()] = 1.0
both[both.isnull()] = 1.0

# Save data frames to file for other stuffs
files.to_csv("%s/files_sims.tsv" %(results_folder),sep="\t")
folders.to_csv("%s/folders_sims.tsv" %(results_folder),sep="\t")
both.to_csv("%s/files_and_folders_sims.tsv" %(results_folder),sep="\t")
