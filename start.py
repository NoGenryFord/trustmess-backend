#!/usr/bin/env python3
"""Startup script that reads PORT from environment and starts uvicorn"""
import os
import sys

# Get port from environment variable (Cloud Run sets this)
port = int(os.environ.get("PORT", 8000))

print(f"Starting server on port {port}...")

# Start uvicorn
os.execvp("uvicorn", ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", str(port)])
