#!/bin/bash

# Check if virtual environment directory "venv" exists in project root
if [ ! -d "venv" ]; then
  echo "Virtual environment not found in project root. Creating one..."
  python3 -m venv venv
  if [ $? -ne 0 ]; then
    echo "Failed to create virtual environment. Please ensure python3-venv is installed."
    exit 1
  fi
else
  echo "Virtual environment found in project root."
fi

# Activate the virtual environment from project root
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install required packages
pip install -r requirements.txt
if [ $? -ne 0 ]; then
  echo "Failed to install Python packages from requirements.txt."
  exit 1
else
  echo "Python packages installed successfully."
fi

# Verify Node.js and npm installation
if ! command -v node &> /dev/null
then
    echo "Node.js could not be found. Please install Node.js."
    exit 1
else
    echo "Node.js is installed."
fi

if ! command -v npm &> /dev/null
then
    echo "npm could not be found. Please install npm."
    exit 1
else
    echo "npm is installed."
fi

# Install npm packages and build frontend assets
frontend_dir="frontend"
if [ -d "$frontend_dir" ]; then
  echo "Installing npm packages in $frontend_dir..."
  npm install --prefix "$frontend_dir"
  if [ $? -ne 0 ]; then
    echo "Failed to install npm packages."
    exit 1
  else
    echo "npm packages installed successfully."
  fi

  echo "Building frontend assets..."
  npm run build --prefix "$frontend_dir"
  if [ $? -ne 0 ]; then
    echo "Failed to build frontend assets."
    exit 1
  else
    echo "Frontend assets built successfully."
  fi
else
  echo "Frontend directory $frontend_dir not found."
  exit 1
fi

echo "Setup complete. Virtual environment is ready, Python packages installed, and frontend built successfully."
