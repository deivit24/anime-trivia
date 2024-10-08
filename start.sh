#!/bin/bash

# Check if an argument is provided
if [ -z "$1" ]; then
  echo "Usage: $0 {dev|prod}"
  exit 1
fi

# Determine which environment to use
if [ "$1" = "dev" ]; then
  docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
elif [ "$1" = "prod" ]; then
  docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
else
  echo "Invalid environment: $1. Use 'dev' or 'prod'."
  exit 1
fi

# Run the seed script
python seed.py

# End of script
