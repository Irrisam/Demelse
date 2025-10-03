#!/bin/bash
docker build -t recommander .
docker run -p 8000:8000 recommander