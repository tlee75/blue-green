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

### Workflow Disaptch menu:  
![workflow-dispatch](https://private-user-images.githubusercontent.com/103002386/363773390-0c2aaade-6c83-452a-b5d7-78f19395c867.jpg?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MjUzMTIzNzQsIm5iZiI6MTcyNTMxMjA3NCwicGF0aCI6Ii8xMDMwMDIzODYvMzYzNzczMzkwLTBjMmFhYWRlLTZjODMtNDUyYS1iNWQ3LTc4ZjE5Mzk1Yzg2Ny5qcGc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQwOTAyJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MDkwMlQyMTIxMTRaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT01YjBhOTE4OWUyZTlkOTVjNDY0NjcwNjgyOTRiMjlmYmVhOGEyODRmYzBjOGE0MGI2YzMyNzEwOTVlZDFmODY5JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZhY3Rvcl9pZD0wJmtleV9pZD0wJnJlcG9faWQ9MCJ9.VIVzMVRYVsFFpAjuNWqdohx6L83xnCiHOJtaC3bb_8w)    

**Image Tag**: Wll be dynamically introduced as an environment variable inside the container and returned with the JSON response  
**Deploy Color**: Will deploy this version of the application to the corresponding colored deployment  
**Deploy Only**: If you have no intention of switching the traffic, e.g. refreshing the build  
**Github Environment**: Which set of environmental variables to use for mapping to different development environments  

### Pipeline after deploying and waiting for traffic switch:  
![waiting-for-approval](https://private-user-images.githubusercontent.com/103002386/363773275-d1ac4a9e-62d8-4efe-823b-d0468822404f.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MjUzMTIzNzQsIm5iZiI6MTcyNTMxMjA3NCwicGF0aCI6Ii8xMDMwMDIzODYvMzYzNzczMjc1LWQxYWM0YTllLTYyZDgtNGVmZS04MjNiLWQwNDY4ODIyNDA0Zi5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQwOTAyJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MDkwMlQyMTIxMTRaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT05ZWRhNDQzZmFhNDQyOWQ1YTg0YjM4NTc0NmVjYTZiMDA1MGRjZDhiOTgyMTM2YzA5ZjBkNGJkNWQ1YWM0YWQ2JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZhY3Rvcl9pZD0wJmtleV9pZD0wJnJlcG9faWQ9MCJ9.eRlZ-lb0G0kyYNeXWX-x92QTOS4TDb_qskzh-kYeUQA)  

Instead of automatically switching traffic after a deployment, a manual approval gate was setup to allow teams to perform
testing prior to switching.

### Manual approval menu:  
![approval-confirmation](https://private-user-images.githubusercontent.com/103002386/363773691-a2e83e84-cd2e-4eae-aca7-77e98e75a5b9.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MjUzMTIzNzQsIm5iZiI6MTcyNTMxMjA3NCwicGF0aCI6Ii8xMDMwMDIzODYvMzYzNzczNjkxLWEyZTgzZTg0LWNkMmUtNGVhZS1hY2E3LTc3ZTk4ZTc1YTViOS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQwOTAyJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MDkwMlQyMTIxMTRaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT0yN2M5MzI1NGE1ZWU2OWU4ZjUwM2ZhMGQ4YjhiM2M3M2ZjN2Q2MWM5NmMzZDc3ZTM4YzgxNWViNGEwZjc1NGY1JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZhY3Rvcl9pZD0wJmtleV9pZD0wJnJlcG9faWQ9MCJ9.WoNiKDbfrEjdTmtNHfMJPLD5u9yavX303iOIF6LA2yI)  

### Pipeline after traffic switch:  
![traffic-switched](https://private-user-images.githubusercontent.com/103002386/363773515-fcff9070-8ece-43d6-92d6-7b3673f807e9.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MjUzMTIzNzQsIm5iZiI6MTcyNTMxMjA3NCwicGF0aCI6Ii8xMDMwMDIzODYvMzYzNzczNTE1LWZjZmY5MDcwLThlY2UtNDNkNi05MmQ2LTdiMzY3M2Y4MDdlOS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQwOTAyJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MDkwMlQyMTIxMTRaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1jZDNlN2MzNDQyOGMxZWE1ZmYwZGUwNzE4NjIxNzVlMTkyM2U2YjE0OGNlNDc4NDJiODJiZTUwZmQ0ZDAxNDkwJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZhY3Rvcl9pZD0wJmtleV9pZD0wJnJlcG9faWQ9MCJ9.qt4hMVz8rDkCeVe8lw52E4ZWQbpIECsxHHBtVKNTDT4)  

### Rollback switched traffic:  
![rollback](https://private-user-images.githubusercontent.com/103002386/363773469-743bdee9-af3a-4f7d-9f64-1563f14e4b11.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MjUzMTIzNzQsIm5iZiI6MTcyNTMxMjA3NCwicGF0aCI6Ii8xMDMwMDIzODYvMzYzNzczNDY5LTc0M2JkZWU5LWFmM2EtNGY3ZC05ZjY0LTE1NjNmMTRlNGIxMS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQwOTAyJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MDkwMlQyMTIxMTRaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1mOGVlYjAyODYxMjYyMDI0YjgwODE5NWI5NTc3OGIwNWY2NWExOGY4YTIzODc1OGQ0MmI3MmUxMDY0NzU5MWQ2JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZhY3Rvcl9pZD0wJmtleV9pZD0wJnJlcG9faWQ9MCJ9.QPCZXrTdGS6Cjyaui2lPe-CEiwIXOdvakt0qbti1nGY)  

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
