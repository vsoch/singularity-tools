# get_docker_container_id will return the id of a stopped Docker
# container. If the image is not on the local machine, it will 
# be downloaded via the run command.
#
# USAGE: ./get_docker_container_id.sh ubuntu:14.04
#

image=$1

# This will download the image if we don't have it
docker run $image

# Retrieve the full id of the image, looks like 
# sha256:d59bdb51bb5c4fb7b2c8d90ae445e0720c169c553bcf553f67cb9dd208a4ec15
fullid=`docker inspect --format="{{.Id}}" ubuntu:14.04`

# Split by : to get rid of sha256
IFS=':' read -a fullid <<< "$fullid"

# Take the first 12 characters to get id of container
container_id=`echo ${fullid[1]} | cut -c1-12`

echo $container_id
