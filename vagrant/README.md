# Vagrant

This is a simple Vagrantfile to run Ubuntu Trusty (14.04) LTS installed with Docker and Singularity, for a quick development environment if you might be using a *cough cough* Mac.

## Usage

To obtain the base image (if you don't have it) and start the VM, do:

      vagrant up

You can then connect to the box via:

      vagrant ssh

Once inside, you should test your Docker installation with:

      docker run hello-world

If there is an error about the Docker daemon, a restart will resolve it:

      sudo reboot now
