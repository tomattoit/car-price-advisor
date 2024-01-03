#!/bin/bash

kubectl apply -f postgres-pv.yaml
kubectl apply -f pv-claim.yaml
kubectl apply -f model-pv.yaml
kubectl apply -f model-claim.yaml
kubectl apply -f react-app.yaml
kubectl apply -f postgres.yaml
kubectl apply -f flask-api.yaml
kubectl apply -f otomoto-crawler-job.yaml
kubectl apply -f retrain-job.yaml

