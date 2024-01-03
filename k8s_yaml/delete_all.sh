#!/bin/bash

kubectl delete -f postgres-pv.yaml
kubectl delete -f pv-claim.yaml
kubectl delete -f model-pv.yaml
kubectl delete -f model-claim.yaml
kubectl delete -f react-app.yaml
kubectl delete -f postgres.yaml
kubectl delete -f flask-api.yaml
kubectl delete -f otomoto-crawler-job.yaml
kubectl delete -f retrain-job.yaml
