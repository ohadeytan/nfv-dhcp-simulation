# NFV DHCP Simulation
A project in Network Function Virtualization course at the Technion ([details](http://webcourse.cs.technion.ac.il/236635/Spring2017/ho_project.html))

## The Goal
Simulate replacement of consumer DHCP hardware with a virtual cloud based service residing on a commercial cloud, either Amazon cloud (AWS) or google Cloud Platform (GCP). 

## The Model
![Alt text](model.png?raw=true "Model")

## How To Run
* All should run with `python2.7`
* Client & Server VMs needed [`pydhcplib`](https://github.com/dgvncsz0f/pydhcplib) library installed
* On cloud Server VM run: `python Server/server.py`
* On local Nat VM run: `python Nat/nat.py` (change the ip of the cloud server in the script)
* On local Client VM run: `./Client/run.sh <number of homes>` (up to 300 homes)

# Animation
![Alt text](Server/animation.gif?raw=true "Animation")
