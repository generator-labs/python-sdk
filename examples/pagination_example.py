#!/usr/bin/env python3
"""
Example: Paginate through large result sets
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

    print("=== Fetching all hosts with pagination ===")

    all_hosts = []
    page = 1
    page_size = 50

    while True:
        print(f"Fetching page {page}...")

        response = client.rbl.hosts().get({
            'page': page,
            'page_size': page_size
        })

        hosts = response.get('hosts', [])
        all_hosts.extend(hosts)

        print(f"  Retrieved {len(hosts)} hosts")

        # Check if there are more pages
        has_more = response.get('has_more', False)
        if not has_more:
            break

        page += 1

    print(f"\nTotal hosts retrieved: {len(all_hosts)}")

    # Alternative: Use the built-in pagination helper
    print("\n=== Using pagination helper ===")

    all_hosts_helper = client.rbl.hosts().get_all(page_size=50)
    print(f"Total hosts via helper: {len(all_hosts_helper)}")

except Exception as e:
    print(f"API Error: {e}")
    sys.exit(1)
