#!/usr/bin/env python3
"""
Example: Check if an IP address is listed on any RBLs
"""

import os
import sys
from generatorlabs import Client, Exception

# Get credentials from environment variables
account_sid = os.getenv('GENERATOR_LABS_ACCOUNT_SID')
auth_token = os.getenv('GENERATOR_LABS_AUTH_TOKEN')

if not account_sid or not auth_token:
    print("Error: Set GENERATOR_LABS_ACCOUNT_SID and GENERATOR_LABS_AUTH_TOKEN environment variables")
    sys.exit(1)

try:
    # Initialize client
    client = Client(account_sid, auth_token)

    # Check a single IP address
    ip = '8.8.8.8'
    print(f"Checking IP: {ip}")

    result = client.rbl.check(ip)

    print("Results:")
    print(result)

    # Check if IP is listed
    if result.get('listed'):
        print(f"\nWARNING: IP {ip} is listed on one or more RBLs!")
        if 'listings' in result:
            print(f"Listed on: {len(result['listings'])} RBL(s)")
    else:
        print(f"\nIP {ip} is clean - not listed on any RBLs")

except Exception as e:
    print(f"API Error: {e}")
    sys.exit(1)
