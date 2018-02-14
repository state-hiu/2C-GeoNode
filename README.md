State_2c_Geonode
========================

This repo contains the static and template files for the 2C GeoNode as well as the configuration files needed to install GeoNode using the [ansible-geonode scripts](https://github.com/GeoNode/ansible-geonode).

## Steps for Installing GeoNode on Amazon AWS

- clone this repo locally

The playbook.yml file in this repo has the settings used when installing GeoNode using ansible-geonode.

On Amazon AWS:

- create a new M5 large instance, download the pem key

On your local machine:

- make sure Ansible is installed. These are the commands to [install Ansible via Apt](http://docs.ansible.com/ansible/intro_installation.html#latest-releases-via-apt-ubuntu):

```
sudo apt-get update
sudo apt-get install software-properties-common -y
sudo apt-add-repository ppa:ansible/ansible -y
sudo apt-get update -y
sudo apt-get install ansible -y
```

Only tested with Ansible version 2.2.1.0, to find out which version of Ansible you have type ```ansible --version```. To install version 2.2.1.0, intead of the previous commands, run the following:

```
sudo apt-get update
sudo apt-get install software-properties-common -y
sudo apt-get install python-pip
sudo pip install 'ansible==2.2.1.0'
```

- Install the GeoNode.geonode role on Ansible Galaxy:
```$ sudo ansible-galaxy install GeoNode.geonode```

- After you've installed Ansible, then you'll want Ansible to know which servers to connect to and manage. Ansible's inventory hosts file is used to list and group your servers. Its default location is /etc/ansible/hosts. Edit this file and add two lines that specify the location of your host, this should match your playbook.yml file. Example:

```
[amazon2]
dev.secondarycities.geonode.state.gov
```

- run the ansible-playbook command. Ex:
```
$ ansible-playbook -v --private-key ~/keys/geonode_dev.pem playbook.yml
```

**if you are having permission problems connecting with ssh, use sudo before the ansible-playbook command

**if you are deploying on AWS and want to use a domain name from Route53 first create a new ec2 instance, then associate that instance to a static ip. Then in route53 create an A record with that elastic ip. Then within your /etc/ansible/hosts file and within the server_name of your playbook.yml file write in that domain name
