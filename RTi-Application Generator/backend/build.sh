# Render Build Script for Backend
# This script handles Python setup and spaCy model download

#!/usr/bin/env bash
set -o errexit

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies (with no cache to avoid stale builds)
pip install --no-cache-dir -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

echo "Build completed successfully!"
