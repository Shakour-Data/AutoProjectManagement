# User Guide

## Overview
This guide provides comprehensive instructions for using the AutoProjectManagement system. It covers installation, configuration, and usage of all system features.

## Table of Contents
- [Installation](#installation)
- [Configuration](#configuration)
- [API Usage](#api-usage)
- [Dashboard Features](#dashboard-features)
- [Real-time Updates](#real-time-updates)
- [Troubleshooting](#troubleshooting)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (for source installation)

### Installation Methods

#### Method 1: From Source
```bash
# Clone the repository
git clone https://github.com/AutoProjectManagement/AutoProjectManagement.git
cd AutoProjectManagement

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Method 2: Using Docker
```bash
# Build the Docker image
docker build -t autoprojectmanagement .

# Run the container
docker run -p 8000:8000 autoprojectmanagement
```

#### Method 3: Using pip
```bash
pip install fastapi uvicorn python-multipart
```

### Starting the Server

```bash
# Start the development server
uvicorn autoprojectmanagement.api.app:app --host 0.0.0.0 --port 8000 --reload

# Start production server
uvicorn autoprojectmanagement.api.app:app --host 0.0.0.0 --port 8000 --workers 4
```

## Configuration

### Environment Variables
Set the following environment variables for configuration:

```bash
export API_KEY=your-api-key
export DATABASE_URL=sqlite:///./autoprojectmanagement.db
export LOG_LEVEL=INFO
export CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

### Configuration File
Create a `config.json` file in the project root:

```json
{
  "api": {
    "host": "0.0.0.0",
    "port": 8000,
    "debug": false
  },
  "database": {
    "url": "sqlite:///./autoprojectmanagement.db",
    "echo": false
  },
  "security": {
    "api_key": "development-key",
## 7. Dashboards and Reporting

- Access dashboards displaying:
  - Progress reports.
  - Priority and urgency visualizations.
  - Cost management summaries.
  - Resource allocation details.
  - Risk management insights.
- Reports are updated dynamically and support filtering and sorting.

## 8. User Interaction Flow Summary

1. Launch frontend → Setup Wizard starts.
2. Complete project initialization.
3. Upload required JSON inputs.
4. Complete project planning inputs.
5. System performs calculations and scheduling.
6. Access dashboards and reports.
7. Use monitoring and control features during project execution.

## 9. Support and Troubleshooting

- Ensure all JSON inputs comply with standards.
- Use the interactive setup wizard for guidance.
- Check logs for errors.
- Contact support via project repository issues.

---
 
This guide helps users effectively interact with the ProjectManagement system through its intuitive frontend and automated backend processes.
