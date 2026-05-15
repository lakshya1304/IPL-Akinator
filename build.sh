#!/bin/bash
set -e

# Upgrade pip and install wheel
pip install --upgrade pip wheel

# Install from backend requirements
# Try with prebuilt wheels only first, then fall back to normal install
cd backend && pip install --no-cache-dir -r requirements.txt
