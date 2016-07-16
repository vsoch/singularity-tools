#! /bin/bash

# Let's make a crapton of singularity base images, so we can generate software lists for them :)

from singularity.utils import check_install
from singularity.cli import Singularity
from BeautifulSoup import BeautifulSoup
import requests
import re
import os

required_softwares = ['docker','singularity']
image_directory = '/home/vanessa/Documents/Work/SINGULARITY/docker2singularity'
os.chdir(image_directory)

print('Checking for required software...')
for required_software in required_softwares:
    if check_install(required_software) != True:
        print("You must have %s installed to use this script!" %(required_software.upper()))
        sys.exit(32)

# Create a command line client
S = Singularity()

# Here is out list of images (note -some of these couldn't be found)
# from https://github.com/docker/docker/wiki/Public-docker-images
docker_images = ["ubuntu:latest","ubuntu:12.10","ubuntu:12.04",
                 "opensuse:13.1","centos","busybox","base/arch",
                 "tianon/debian:wheezy","tianon/debian:7.1",
                 "tianon/debian:jessie","tianon/debian-roll:stable",
                 "tianon/debian-roll:7.1","johncosta/redis",
                 "shykes/couchdb","jpetazzo/pgsql","samalba/hipache",
                 "creack/firefox-vnc","jbarbier/memcached",
                 "shykes/znc","shykes/dockerbuilder","shykes/node-opencv",
                 "audreyt/ethercalc"]

# Let's get the list of official docker from a request
url = "https://github.com/docker-library/official-images/tree/master/library"
page = requests.get(url).text
soup = BeautifulSoup(page)
links = soup.findAll("a")
for link in links:
    if "attrs" in link.__dict__:
        title = [x for x in link.attrs if x[0] == 'title']
        if len(title) > 0:
            title = title[0][1]
            # Real image links have title same as text...
            if link.text == title:
                # and no white spaces!
                if not re.search(' ',link.text):
                    print('Adding image %s' %(title))
                    docker_images.append(title)

print("Generating %s images!" %(len(docker_images)))
for docker_image in docker_images:
    try:
        S.docker2singularity(docker_image)
    except:
        print("ERROR creating %s" %(docker_image))
