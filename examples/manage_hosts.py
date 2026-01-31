#!/usr/bin/env python3
"""
Example: Manage monitored hosts (create, list, update, delete)
"""

import os
import sys
from generatorlabs import Client, Exception

account_sid = os.getenv('GENERATOR_LABS_ACCOUNT_SID')
auth_token = os.getenv('GENERATOR_LABS_AUTH_TOKEN')

if not account_sid or not auth_token:
    print("Error: Set GENERATOR_LABS_ACCOUNT_SID and GENERATOR_LABS_AUTH_TOKEN environment variables")
    sys.exit(1)

try:
    client = Client(account_sid, auth_token)

    # List all hosts
    print("=== Listing all monitored hosts ===")
    hosts = client.rbl.hosts().get()
    print(f"Total hosts: {len(hosts.get('hosts', []))}\n")

    for host in hosts.get('hosts', []):
        print(f"ID: {host['id']}, IP: {host['ip']}, Description: {host.get('description', 'N/A')}")

    # Create a new host
    print("\n=== Creating a new host ===")
    new_host = client.rbl.hosts().create({
        'ip': '203.0.113.10',
        'description': 'Example host from Python SDK',
        'profile_id': 1  # Use your profile ID
    })
    print(f"Created host ID: {new_host['host']['id']}")
    host_id = new_host['host']['id']

    # Get specific host
    print("\n=== Getting specific host ===")
    host = client.rbl.hosts().get(host_id)
    print("Host details:")
    print(host)

    # Update host
    print("\n=== Updating host ===")
    updated_host = client.rbl.hosts().update(host_id, {
        'description': 'Updated description from Python SDK'
    })
    print("Updated host description")

    # Delete host
    print("\n=== Deleting host ===")
    client.rbl.hosts().delete(host_id)
    print(f"Deleted host ID: {host_id}")

except Exception as e:
    print(f"API Error: {e}")
    sys.exit(1)
