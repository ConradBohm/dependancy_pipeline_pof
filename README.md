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

In `kube/secrets.yml`, set 
- `RENOVATE_TOKEN` 
- `RENOVATE_PLATFORM` 
- `RENOVATE_ENDPOINT` 

for the platform you wish to scan. Select specific repositories to scan in the `RENOVATE_REPOSITORIES` env, or set `RENOVATE_AUTODISCOVER: true` for RenovateBot to scan all repositories that the given token has access to.

For a repository to be scanned, it needs a `renovate,json` config file in the root directory for it to be recognised by the 
tool. The minimum for the file to include is:
```
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json"
}
```
Fruther config options can be found under Configuration/Repository in the docs (link below).

Run the bash script via `./job_run.sh` and the script will run `kubectl` commands to create the job and it's resources. The
script will detect whether a job of the same name already exists before running, and deleting the existing one if so. 

In order to parse the logs, a file containing them will be created in the root directory of this project. This is for debugging 
purposes and the method will be changed when the parsing script is run as a part of the Kubernetes job.

## Expected Output
The file `logs_sample.txt` contains logs from scanning two dummy repos:
- https://github.com/ConradBohm/renovate_test_repo
- https://github.com/ConradBohm/renovate_second_test_repo

They are meant to have out-of-date dependencies, with dependency files differing in format. The parser takes those logs and produces this output:

<img width="386" alt="image" src="https://github.com/ConradBohm/dependancy_pipeline_pof/assets/37579805/0835d56c-d0b7-458a-bd95-07ddd0c5437c">
<img width="386" alt="image" src="https://github.com/ConradBohm/dependancy_pipeline_pof/assets/37579805/b7938d30-4725-427e-8907-fe4c6518dcc9">

Extra information can be garnered from the logs; look between lines `246-372`, and `571-904` in the sample log file for the scan of each repo respectively.

## Next Steps
- Run the parsing script as part of the Kubernetes job, or from a Kubernetes container using mounted volumes to get the log file from the scan.
- Create dummy payloads for RocketChat / Jira / etc alerting.
- ...

## Links
- https://docs.renovatebot.com
- https://minikube.sigs.k8s.io/docs/
