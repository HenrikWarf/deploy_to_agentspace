# ADK Agent Deployment Script

This guide explains how to use the `deploy_to_agentspace.py` script to manage your ADK (Agent Development Kit) agents in Agentspace.

## Prerequisites

Before you begin, ensure you have completed the following setup steps:

1.  **Enable the Discovery Engine API:** Make sure the Discovery Engine API is enabled for your Google Cloud Platform (GCP) project.
2.  **Assign IAM Roles:** Grant the `Vertex AI User` and `Vertex AI Viewer` roles to your Discovery Engine service account. This is necessary for Agentspace to call your ADK agent.
    *   To do this, navigate to the IAM page in the Google Cloud Console.
    *   Search for the "discoveryengine" service account.
    *   **Important:** You may need to check the "Include Google-provided role grants" option to see the service account.
    *   Add the required `Vertex AI User` and `Vertex AI Viewer` permissions to the service account.

## Setup

Follow these steps to set up your environment to run the script.

### 1. Create a Virtual Environment

It is recommended to use a virtual environment to manage the dependencies for this script. 

**On macOS and Linux:**

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

**On Windows:**

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
.\venv\Scripts\activate
```

### 2. Install Dependencies

Once your virtual environment is activated, you can install the required Python libraries:

```bash
pip install python-dotenv requests
```

### 3. Configure Environment Variables

The script uses a `.env` file to manage configuration. 

1.  A `.env` file should already be present in this directory. 
2.  Open the `.env` file and fill in the values for each variable. 

```
PROJECT_ID=""
ProjectNumber=""
APP_ID=""
DISPLAY_NAME=""
DESCRIPTION=""
AGENT_RESOURCE_PATH=""
LOCATION="us-central1"
AGENT_NAME=""
```

## Usage

You can run the script from your terminal using the following commands.

### List Reasoning Engines

To list the available reasoning engines and find your `AGENT_RESOURCE_PATH`:

```bash
python deploy_to_agentspace.py list-engines
```

### List Agentspace Apps

To list your Agentspace applications and find your `APP_ID`:

```bash
python deploy_to_agentspace.py list-apps
```

### Register an Agent

To register your ADK agent with Agentspace:

```bash
python deploy_to_agentspace.py register
```

### View Registered Agents

To see the agents that are currently registered in your Agentspace application:

```bash
python deploy_to_agentspace.py view
```

### Unregister an Agent

To remove an agent from Agentspace:

```bash
python deploy_to_agentspace.py unregister
```