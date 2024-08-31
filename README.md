# Blue Green Deployment Example

This project demonstrates a very basic implementation of a Blue-Green deployment to Kubernetes, including a script for 
detecting the traffic switch-over. The Github Actions automation is presented as a bare-bones build/deploy workflow and 
has an idempotent traffic switching job that can be initiated multiple times to switch the traffic back and forth between
Blue and Green as needed.  

The traffic switching is automated but must be approved and triggered manually to ensure time is given to properly test
the environment before transferring the workload.  

# Usage


#### Debug

Install requirements into virtual environment:  
`python3 -m pip install -r requirements.txt`  

Start the server:  
`python3 th3-server/th3-server.py`  

#### Docker

Build the image:  
`IMAGE_VERSION=0.0.1 ./build-client.sh`

Start the server:  
`sudo docker run --name th3-server -p 8080:8080 --rm -it docker.io/tlee75/th3-server:0.0.1`  

# Testing

To observe the connectivity to the deployment, install the required package and edit the script for the correct server 
port and url before running the script. The script primarily outputs to a file on disk and will run 
indefinitely or until a version change has been detected.  

`python3 -m pip install requests==2.32.3`
`python3 get_version.py`  

# CI/CD

