#!/bin/bash

# Check if .env file exists
if [ ! -f .env ]; then
  echo "Error: .env file not found."
  exit 1
fi

# Read and export variables from .env file
while IFS= read -r line || [[ -n "$line" ]]; do
  # Ignore comments and empty lines
  if [[ "$line" =~ ^[[:space:]]*# || -z "$line" ]]; then
    continue
  fi

  # Check if line contains '='
  if [[ "$line" == *"="* ]]; then
    # Split on first '=' and trim spaces
    key="${line%%=*}"
    value="${line#*=}"
    
    # Trim leading and trailing spaces
    key=$(echo "$key" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    value=$(echo "$value" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    
    # Remove surrounding quotes from the value if present
    if [[ "$value" =~ ^\".*\"$ ]]; then
      value="${value#\"}"
      value="${value%\"}"
    fi
    
    # Ensure the key is a valid identifier and not empty
    if [[ -n "$key" && "$key" =~ ^[a-zA-Z_][a-zA-Z0-9_]*$ ]]; then
      # Export the variable
      export "$key=$value"
      echo "Exported: $key"
    fi
  fi
done < .env

echo "Environment variables from .env have been exported."
