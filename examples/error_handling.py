#!/usr/bin/env python3
"""
Example: Proper error handling and configuration
"""

import os
import sys
from generatorlabs import Client, Exception, Config

account_sid = os.getenv('GENERATOR_LABS_ACCOUNT_SID')
auth_token = os.getenv('GENERATOR_LABS_AUTH_TOKEN')

if not account_sid or not auth_token:
    print("Error: Set GENERATOR_LABS_ACCOUNT_SID and GENERATOR_LABS_AUTH_TOKEN environment variables")
    sys.exit(1)

try:
    # Initialize client with custom configuration
    config = Config(
        timeout=45,           # 45 second timeout
        connect_timeout=10,   # 10 second connection timeout
        max_retries=5,        # 5 retry attempts
        retry_backoff=2       # 2x backoff multiplier (2s, 4s, 8s, 16s, 32s)
    )
    client = Client(account_sid, auth_token, config)

    print("=== Example 1: Handling API errors ===")
    try:
        # Try to get a non-existent host
        client.rbl.hosts().get(999999)
    except Exception as e:
        print(f"Caught error: {e}")
        print("This is expected for a non-existent resource\n")

    print("=== Example 2: Invalid credentials ===")
    try:
        bad_client = Client('INVALID', auth_token)
    except Exception as e:
        print(f"Caught error: {e}")
        print("Credential validation works!\n")

    print("=== Example 3: Network resilience ===")
    # The SDK automatically retries on:
    # - Connection errors
    # - 5xx server errors
    # - 429 rate limit errors
    # With exponential backoff

    result = client.rbl.check('1.1.1.1')
    print("Request succeeded (with automatic retries if needed)")

    print("\n=== Example 4: Graceful degradation ===")
    try:
        hosts = client.rbl.hosts().get()
        print(f"Successfully retrieved {len(hosts.get('hosts', []))} hosts")
    except Exception as e:
        # Log error and continue with cached/default data
        print(f"API error: {e}")
        print("Using cached data due to API error")
        hosts = {'hosts': []}  # Fallback to empty array

except Exception as e:
    print(f"Fatal error: {e}")
    sys.exit(1)

print("\nAll examples completed!")
