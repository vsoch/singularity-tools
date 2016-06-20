# docker2singularity.sh will convert a docker image into a singularity
# Must be run with sudo to use docker commands (eg aufs)
# 
# container by running the image and exporting.
#
# USAGE: docker2singularity.sh ubuntu:14.04

image=$1
size=4096

# Run the image and obtain the ID, should DL if we don't have it
runningid=`docker run -d $image tail -f /dev/null`

# Get the container size (not done yet)
#fullid=`docker inspect --format="{{.Id}}" $image`
#IFS=':' read -a fullid <<< "$fullid"
#sudo du -d 2 -h /var/lib/docker/aufs | ${fullid[1]}
#size=`docker run --entrypoint=/bin/sh $image -c 'du -sh / 2>/dev/null | cut -f1'`
# 208M

# Full id looks like
# sha256:d59bdb51bb5c4fb7b2c8d90ae445e0720c169c553bcf553f67cb9dd208a4ec15

# Take the first 12 characters to get id of container
container_id=`echo ${runningid} | cut -c1-12`

# For Network Address
#docker inspect --format="{{.NetworkSettings.IPAddress}}" bodymap_web_1
image_name=`docker inspect --format="{{.Config.Image}}" $container_id`
creation_date=`docker inspect --format="{{.Created}}" $container_id`
creation_date=`echo ${creation_date} | cut -c1-10`
new_container_name=$image_name-$creation_date.img

# Create singularity image # STOPPED HERE - need to get container to run, and export
sudo singularity create -s $size $new_container_name
docker export $container_id | sudo singularity import $new_container_name 
