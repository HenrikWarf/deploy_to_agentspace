"""
A script to manage ADK agents in Agentspace.

This script requires the following packages:
- python-dotenv
- requests

You can install them using pip:
pip install python-dotenv requests
"""

import os
import subprocess
import requests
import argparse
from dotenv import load_dotenv

def get_access_token():
    """Gets the gcloud access token."""
    try:
        token = subprocess.check_output(
            ["gcloud", "auth", "print-access-token"], text=True
        ).strip()
        return token
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Error getting access token: {e}")
        print("Please make sure you have the gcloud CLI installed and are authenticated.")
        exit(1)

def list_reasoning_engines(token, project_id, location):
    """Lists the available reasoning engines."""
    url = f"https://{location}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{location}/reasoningEngines"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    data = response.json()
    if "reasoningEngines" in data:
        for engine in data["reasoningEngines"]:
            print(f"Display Name: {engine.get('displayName')}")
            print(f"Name: {engine.get('name')}")
            print("-" * 20)
    else:
        print(data)

def list_agentspace_apps(token, project_id):
    """Lists the Agentspace apps."""
    url = f"https://discoveryengine.googleapis.com/v1alpha/projects/{project_id}/locations/global/collections/default_collection/engines"
    headers = {
        "Authorization": f"Bearer {token}",
        "x-goog-user-project": project_id,
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    if "engines" in data:
        for engine in data["engines"]:
            print(f"Display Name: {engine.get('displayName')}")
            print(f"Name: {engine.get('name')}")
            print("-" * 20)
    else:
        print(data)

def register_agent(token, project_id, app_id, display_name, description, agent_resource_path):
    """Registers an agent in Agentspace."""
    url = f"https://discoveryengine.googleapis.com/v1alpha/projects/{project_id}/locations/global/collections/default_collection/engines/{app_id}/assistants/default_assistant/agents"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "x-goog-user-project": project_id,
    }
    payload = {
        "displayName": display_name,
        "description": description,
        "adk_agent_definition": {
            "tool_settings": {"tool_description": "Tool Description"},
            "provisioned_reasoning_engine": {
                "reasoning_engine": agent_resource_path
            },
        },
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        try:
            print(response.json())
        except requests.exceptions.JSONDecodeError:
            print("Agent registered successfully, but no JSON response was returned.")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

def view_agents(token, project_id, app_id):
    """Views the registered agents in Agentspace."""
    url = f"https://discoveryengine.googleapis.com/v1alpha/projects/{project_id}/locations/global/collections/default_collection/engines/{app_id}/assistants/default_assistant/agents"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-Goog-User-Project": project_id,
    }
    response = requests.get(url, headers=headers)
    print(response.json())

def unregister_agent(token, project_id, agent_name):
    """Unregisters an agent from Agentspace."""
    url = f"https://discoveryengine.googleapis.com/v1alpha/{agent_name}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-Goog-User-Project": project_id,
    }
    response = requests.delete(url, headers=headers)
    if response.status_code == 200:
        print("Agent unregistered successfully.")
    else:
        print(response.json())

def main():
    """Main function to handle command-line arguments."""
    load_dotenv()

    parser = argparse.ArgumentParser(description="Manage ADK agents in Agentspace.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subparser for listing reasoning engines
    subparsers.add_parser("list-engines", help="List available reasoning engines.")

    # Subparser for listing Agentspace apps
    subparsers.add_parser("list-apps", help="List Agentspace apps.")

    # Subparser for registering an agent
    subparsers.add_parser("register", help="Register an agent in Agentspace.")

    # Subparser for viewing agents
    subparsers.add_parser("view", help="View registered agents.")

    # Subparser for unregistering an agent
    subparsers.add_parser("unregister", help="Unregister an agent.")

    args = parser.parse_args()

    # Get environment variables
    project_id = os.getenv("PROJECT_ID")
    location = os.getenv("LOCATION")
    app_id = os.getenv("APP_ID")
    display_name = os.getenv("DISPLAY_NAME")
    description = os.getenv("DESCRIPTION")
    agent_resource_path = os.getenv("AGENT_RESOURCE_PATH")
    agent_name = os.getenv("AGENT_NAME")

    # Check for required environment variables
    if not project_id:
        print("Error: PROJECT_ID environment variable not set.")
        exit(1)

    token = get_access_token()

    if args.command == "list-engines":
        if not location:
            print("Error: LOCATION environment variable not set.")
            exit(1)
        list_reasoning_engines(token, project_id, location)
    elif args.command == "list-apps":
        list_agentspace_apps(token, project_id)
    elif args.command == "register":
        if not all([app_id, display_name, description, agent_resource_path]):
            print("Error: One or more required environment variables for registering an agent are not set.")
            print("Please check APP_ID, DISPLAY_NAME, DESCRIPTION, and AGENT_RESOURCE_PATH.")
            exit(1)
        register_agent(token, project_id, app_id, display_name, description, agent_resource_path)
    elif args.command == "view":
        if not app_id:
            print("Error: APP_ID environment variable not set.")
            exit(1)
        view_agents(token, project_id, app_id)
    elif args.command == "unregister":
        if not agent_name:
            print("Error: AGENT_NAME environment variable not set.")
            exit(1)
        unregister_agent(token, project_id, agent_name)

if __name__ == "__main__":
    main()
