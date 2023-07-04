#!/bin/bash

KUBE_JOB_NAME='renovate-job'
PROJECT_PATH='/Users/admin/dependancy_pipeline_pof'

echo 'building parser image to local registry'
docker build -f ./Dockerfile -t parser:latest .

echo 'deleting existing job..'
if kubectl get jobs | grep ${KUBE_JOB_NAME}; then
    echo 'deleting'
    kubectl delete job ${KUBE_JOB_NAME}
else
    echo 'job does not exist, continuing..'
fi

echo 'applying secrets file'
kubectl apply -f "${PROJECT_PATH}/kube/secret.yml"

echo 'starting job'
kubectl apply -f "${PROJECT_PATH}/kube/renovate_job.yml" > /dev/null &

sleep 20
echo 'waiting for job to finish'
kubectl wait --for=condition=complete --timeout=90s job/${KUBE_JOB_NAME} && echo 'job complete'
