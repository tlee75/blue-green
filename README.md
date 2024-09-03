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
`IMAGE_TAG=0.0.1 ./build-client.sh`

Start the server:  
`sudo docker run --name th3-server -p 8080:8080 --rm -it docker.io/tlee75/th3-server:0.0.1`  

# Testing

To observe the connectivity to the deployment, install the required package and edit the script for the correct server 
port and url before running the script. The script primarily outputs to a file on disk and will run 
indefinitely or until a version change has been detected.  

The color agnostic endpoint can be reached at:  
https://th3-server.tylerlee.dev/version

To test a specific color:  
Blue: https://blue-th3-server.tylerlee.dev/version  
Green: https://green-th3-server.tylerlee.dev/version

The deployment can be switched between the colors by running the idempotent "Switch Traffic" job at the end of the workflow.  

```
python3 -m pip install requests==2.32.3  
python3 get_version.py  
```
# Automation

This automation assumes there is an available Kubernetes installation running on a remote server accessible via SSH.
Multiple variables and secrets are required:

**Repository Secrets**:  
DOCKERHUB_USERNAME  
DOCKERHUB_TOKEN  
SSH_PRIVATE_KEY  

**Repository Variables**:  
DOCKERHUB_ACCOUNT  
SSH_SERVER_URL  
SERVER_USERNAME  

## Build and Deploy

You may initiate a deployment via Github Actions using the [Blue Green Deployment](https://github.com/tlee75/blue-green/actions/workflows/blue-green-deploy.yml)
workflow.

### Workflow Dispatch menu:  
![workflow-dispatch](https://github.com/tlee75/blue-green/blob/feature/1-create-blue-green-deployment/images/workflow-dispatch.jpg?raw=true)    

**Image Tag**: Will be dynamically introduced as an environment variable inside the container and returned with the JSON response  
**Deploy Color**: Will deploy this version of the application to the corresponding colored deployment  
**Deploy Only**: If you have no intention of switching the traffic, e.g. refreshing the build  
**Github Environment**: Which set of environmental variables to use for mapping to different development environments  

### Pipeline after deploying and waiting for traffic switch:  
![waiting-for-approval](https://github.com/tlee75/blue-green/blob/feature/1-create-blue-green-deployment/images/waiting-pipeline.png?raw=true)  

Instead of automatically switching traffic after a deployment, a manual approval gate was setup to allow teams to perform
testing prior to switching.

### Manual approval menu:  
![approval-confirmation](https://github.com/tlee75/blue-green/blob/feature/1-create-blue-green-deployment/images/approval-dialog.png?raw=true)  

### Pipeline after traffic switch:  
![traffic-switched](https://github.com/tlee75/blue-green/blob/feature/1-create-blue-green-deployment/images/automated-traffic-switch.png?raw=true)  

### Rollback switched traffic:  
![rollback](https://github.com/tlee75/blue-green/blob/feature/1-create-blue-green-deployment/images/rollback.png?raw=true)  

By re-running the traffic switch job, it will invert the Kubernetes service selectors and effectively revert traffic to 
the previous deployment.  

# Notes

This project has a lot of room for growth, here are some thoughts:  

- Consider a weight based canary deployment strategy
- Explore using a service mesh, cloud based load balancer, Argo Rollouts
- If this application were more complex that would make storing all the resources for two versions of the application
within the same namespace more difficult, leading to file duplication, naming collisions, templating complexity, helm 
deployment collisions, etc. In that case using separate namespaces might make more sense but that complicates some aspects 
such as using cluster wide resources like persistent volumes and would need to be considered as part of the design.  
