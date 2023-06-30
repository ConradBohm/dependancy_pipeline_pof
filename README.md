# Dependancy Pipeline PoC

A self-hosted instance of RenovateBot.

Currently only produces log output of package dependencies, with a parser turning the logs into usable information.

This repo pulls an image from the internet, so will not run in air-gapped environments off the bat.

## Components
- Kubernetes single run job that houses the RenovateBot tool.
- A Kube Cronjob manifest to demonstrate an alternative to a single run job.
- Python script to parse and print the log output from the job.
- Bash script to run the job and the parsing script.

## Running the application
Ensure a Kubernetes cluster is running and available to create resources. This repo was made using Minikube.

Change the permissions of the `job_run.sh` bash file to allow it to be executed. Typically done with a `chmod 744` command.

