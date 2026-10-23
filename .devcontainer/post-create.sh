#!/bin/bash
set -e  # Exit immediately if any command fails

echo "=== 1/3 Upgrading pip ==="
pip install --upgrade pip

echo "=== 2/3 Installing Python dependencies ==="
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
else
    echo "No requirements.txt found, skipping Python dependencies installation."
fi

echo "=== 3/3 Installing OpenCode 2.0 ==="
curl -fsSL https://opencode.ai/v2/install | bash

echo "=== Setup Complete ==="
