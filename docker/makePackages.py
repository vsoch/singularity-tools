#! /bin/bash

# Let's turn our crapton of images into packages (to extract folders.txt and files.txt)

from singularity.utils import check_install
from singularity.cli import Singularity
from singularity.package import package
from glob import glob
import os
import sys

base = '/home/vanessa/Documents/Work/SINGULARITY'
image_directory = '%s/docker2singularity' %(base)
package_directory = '%s/packages' %(base)

# Check for Singularity installation
if check_install() != True:
    print("You must have Singularity installed to use this script!")
    sys.exit(32)

# Make output directory
if not os.path.exists(package_directory):
    os.mkdir(package_directory)
os.chdir(package_directory)


# Create a command line client
S = Singularity()

images = glob("%s/*.img" %(image_directory))

print("Generating packages for %s images!" %(len(images)))
for image in images:
    output_file = "%s/%s.zip" %(package_directory,os.path.basename(image))
    if not os.path.exists(output_file):
        package(image_path=image,
                output_folder=package_directory,
                runscript=False,
                software=True,
                S=S)
