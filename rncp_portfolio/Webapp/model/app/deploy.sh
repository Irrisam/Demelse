#!/bin/bash
cp app/.env app/tmp.env
gcloud kms decrypt --ciphertext-file=.env.prod.enc --plaintext-file=.env --location=europe-west3 --keyring=Medelse --key=encrypt-parameter
gcloud builds submit --tag eu.gcr.io/medelse-180512/medelse-random-forest:latest
gcloud beta run deploy medelse-random-forest --image eu.gcr.io/medelse-180512/medelse-random-forest:latest --region europe-west3 --platform managed
rm app/.env
mv app/tmp.env app/.env


gcloud kms encrypt --plaintext-file=.env.tmp --ciphertext-file=.env.preprod.enc --location=europe-west3 --keyring=Medelse --key=encrypt-parameter
gcloud kms decrypt --ciphertext-file=.env.preprod.enc --plaintext-file=.env.tmp --location=europe-west3 --keyring=Medelse --key=encrypt-parameter
gcloud kms decrypt --ciphertext-file=.env.prod.enc --plaintext-file=.env.tmp --location=europe-west3 --keyring=Medelse --key=encrypt-parameter