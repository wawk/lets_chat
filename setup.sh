#!/bin/bash

# Activate venv (creates it if missing)
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install required packages
pip install \
    openai \
    python-dotenv \
    pytest \
    rich \
    tiktoken

