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

The script uses a `.env` file to manage configuration. Open the `.env` file in this directory and fill in the values for each variable as described below.

```
# Your Google Cloud Platform project ID. This is required for all commands.
PROJECT_ID=""

# The GCP location where your reasoning engine is deployed (e.g., us-central1). Required for 'list-engines'.
LOCATION="us-central1"

# The ID of your Agentspace application. Required for 'register' and 'view'.
# You can find this by running 'python deploy_to_agentspace.py list-apps'.
# You can provide the full resource name and the script will extract the ID.
APP_ID=""

# A display name for your new ADK agent. Required for 'register'.
DISPLAY_NAME=""

# A description for your new ADK agent. Required for 'register'.
DESCRIPTION=""

# The resource path of your deployed reasoning agent. Required for 'register'.
# You can find this by running 'python deploy_to_agentspace.py list-engines'.
AGENT_RESOURCE_PATH=""

# The full resource name of the agent you want to unregister. Required for 'unregister'.
# You can find this by running 'python deploy_to_agentspace.py view'.
AGENT_NAME=""
```

## Usage

You can run the script from your terminal using the following commands.

### List Agents in Agent Engine

To list the available Agents in Agent Engine and find your `AGENT_RESOURCE_PATH`:

```bash
python deploy_to_agentspace.py list-engines
```
> After running this command, copy the `Name` of the reasoning engine you want to use and paste it into the `AGENT_RESOURCE_PATH` field in your `.env` file.

### List Agentspace Apps

To list your Agentspace applications and find your `APP_ID`:

```bash
python deploy_to_agentspace.py list-apps
```
> After running this command, copy the `Name` of the Agentspace application you want to use and paste it into the `APP_ID` field in your `.env` file.

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
> After running this command, if you want to unregister an agent, copy the `Name` of the agent and paste it into the `AGENT_NAME` field in your `.env` file.

### Unregister an Agent

To remove an agent from Agentspace:

```bash
python deploy_to_agentspace.py unregister
```