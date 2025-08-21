# Registering an ADK Agent in Agentspace

This guide provides step-by-step instructions on how to register, view, and unregister an ADK (Agent Development Kit) agent in Agentspace.

## Prerequisites

Before you begin, ensure you have completed the following setup steps:

1.  **Enable the Discovery Engine API:** Make sure the Discovery Engine API is enabled for your Google Cloud Platform (GCP) project.
2.  **Assign IAM Roles:** Grant the `Vertex AI User` and `Vertex AI Viewer` roles to your Discovery Engine service account. This is necessary for Agentspace to call your ADK agent.
    *   To do this, navigate to the IAM page in the Google Cloud Console.
    *   Search for the "discoveryengine" service account.
    *   **Important:** You may need to check the "Include Google-provided role grants" option to see the service account.
    *   Add the required `Vertex AI User` and `Vertex AI Viewer` permissions to the service account.

## Configuration

You'll need to define several environment variables to run the commands in this guide.

```bash
# Your Google Cloud Platform project ID
export PROJECT_ID=""

# Your Google Cloud Platform project number
export ProjectNumber=""

# The ID of your Agentspace application
export APP_ID=""

# A display name for your ADK agent
export DISPLAY_NAME=""

# A description for your ADK agent
export DESCRIPTION=""

# The resource path of your deployed reasoning agent
export AGENT_RESOURCE_PATH=""

# The GCP location where your reasoning engine is deployed (e.g., us-central1)
export LOCATION="us-central1"
```

## Instructions

Follow these steps to manage your ADK agent in Agentspace.

### 1. Obtain Your Access Token

You will need an access token to authenticate with the GCP APIs. You can get one using the gcloud CLI:

```bash
TOKEN=$(gcloud auth print-access-token)
```

### 2. List Available Reasoning Engines

This command helps you find the `AGENT_RESOURCE_PATH` for your deployed reasoning engine.

```bash
curl -X GET \
  -H "Authorization: Bearer $TOKEN" \
  "https://us-central1-aiplatform.googleapis.com/v1/projects/$PROJECT_ID/locations/$LOCATION/reasoningEngines"
```

### 3. List Agentspace Apps

This command helps you find the `APP_ID` for your Agentspace application.

```bash
curl -X GET \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: $PROJECT_ID" \
  "https://discoveryengine.googleapis.com/v1alpha/projects/$PROJECT_ID/locations/global/collections/default_collection/engines"
```

### 4. Register the ADK Agent

This command registers your ADK agent with Agentspace.

```bash
# Create the JSON payload for the registration request
JSON_PAYLOAD=$(printf 
    {
        "displayName": "%s",
        "description": "%s",
        "adk_agent_definition": {
          "tool_settings": {
            "tool_description": "Tool Description"
          },
          "provisioned_reasoning_engine": {
            "reasoning_engine": "%s"
          }
        }
    }
, "$DISPLAY_NAME", "$DESCRIPTION", "$AGENT_RESOURCE_PATH")

# Send the registration request
curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "x-goog-user-project: $PROJECT_ID" \
  "https://discoveryengine.googleapis.com/v1alpha/projects/$PROJECT_ID/locations/global/collections/default_collection/engines/$APP_ID/assistants/default_assistant/agents" \
  -d "$JSON_PAYLOAD"
```

### 5. View Registered Agents

After registering your agent, you can use this command to view all the agents registered in your Agentspace application.

```bash
curl -X GET \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "X-Goog-User-Project: $PROJECT_ID" \
  "https://discoveryengine.googleapis.com/v1alpha/projects/$PROJECT_ID/locations/global/collections/default_collection/engines/$APP_ID/assistants/default_assistant/agents"
```

### 6. Unregister an Agent

If you need to remove an agent from Agentspace, you can use this command.

```bash
# The full name of the agent to unregister
export AGENT_NAME="projects/your-project-id/locations/global/collections/default_collection/engines/your-app-id/assistants/default_assistant/agents/your-agent-id"

# Send the delete request
curl -X DELETE \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "X-Goog-User-Project: $PROJECT_ID" \
  "https://discoveryengine.googleapis.com/v1alpha/$AGENT_NAME"
```