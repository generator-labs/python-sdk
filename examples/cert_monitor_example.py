#!/usr/bin/env python3
"""
Example: Certificate monitoring - list errors, manage monitors and profiles
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

    # ===================================================================
    # Certificate Errors
    # ===================================================================
    print("=== Listing Certificate Errors ===")
    errors = client.cert.errors.get()
    print(f"Total errors: {len(errors.get('errors', []))}\n")

    for error in errors.get('errors', []):
        print(f"Error ID: {error['id']}")
        print(f"  Monitor: {error['monitor_name']}")
        print(f"  Type: {error['error_type']}")
        print(f"  Message: {error['message']}\n")

    # ===================================================================
    # Certificate Profiles
    # ===================================================================
    print("=== Managing Certificate Profiles ===")

    # List all profiles
    profiles = client.cert.profiles.get()
    print(f"Total profiles: {len(profiles.get('profiles', []))}")

    # Create a new profile
    print("\n=== Creating a new certificate profile ===")
    new_profile = client.cert.profiles.create({
        'name': 'Example Certificate Profile',
        'expiration_warning_days': 30,
        'expiration_critical_days': 7,
        'check_self_signed': True,
        'check_hostname_mismatch': True
    })
    print(f"Created profile ID: {new_profile['profile']['id']}")
    profile_id = new_profile['profile']['id']

    # Get specific profile
    print("\n=== Getting specific profile ===")
    profile = client.cert.profiles.get(profile_id)
    print(f"Profile name: {profile['profile']['name']}")
    print(f"Expiration warning days: {profile['profile']['expiration_warning_days']}")

    # Update profile
    print("\n=== Updating profile ===")
    updated_profile = client.cert.profiles.update(profile_id, {
        'expiration_warning_days': 45
    })
    print("Updated profile warning days to 45")

    # ===================================================================
    # Certificate Monitors
    # ===================================================================
    print("\n=== Managing Certificate Monitors ===")

    # List all monitors
    monitors = client.cert.monitors.get()
    print(f"Total monitors: {len(monitors.get('monitors', []))}")

    # Create a new HTTPS monitor
    print("\n=== Creating HTTPS certificate monitor ===")
    https_monitor = client.cert.monitors.create({
        'name': 'Example HTTPS Monitor',
        'hostname': 'example.com',
        'port': 443,
        'protocol': 'https',
        'cert_profile': profile_id,
        'contact_group': 'CG37106c6baa1ec90a2b3f5c8ec54afe9d'  # Use your contact group ID
    })
    print(f"Created HTTPS monitor ID: {https_monitor['monitor']['id']}")
    https_monitor_id = https_monitor['monitor']['id']

    # Create a mail server monitor (SMTPS)
    print("\n=== Creating SMTPS certificate monitor ===")
    smtps_monitor = client.cert.monitors.create({
        'name': 'Example Mail Server Monitor',
        'hostname': 'mail.example.com',
        'port': 465,
        'protocol': 'smtps',
        'cert_profile': profile_id,
        'contact_group': 'CG37106c6baa1ec90a2b3f5c8ec54afe9d'
    })
    print(f"Created SMTPS monitor ID: {smtps_monitor['monitor']['id']}")
    smtps_monitor_id = smtps_monitor['monitor']['id']

    # Get specific monitor
    print("\n=== Getting specific monitor ===")
    monitor = client.cert.monitors.get(https_monitor_id)
    print(f"Monitor name: {monitor['monitor']['name']}")
    print(f"Hostname: {monitor['monitor']['hostname']}")
    print(f"Protocol: {monitor['monitor']['protocol']}")
    print(f"Status: {monitor['monitor']['status']}")

    # Update monitor
    print("\n=== Updating monitor ===")
    updated_monitor = client.cert.monitors.update(https_monitor_id, {
        'name': 'Updated HTTPS Monitor Name'
    })
    print("Updated monitor name")

    # Pause monitoring
    print("\n=== Pausing monitor ===")
    client.cert.monitors.pause(https_monitor_id)
    print(f"Paused monitor ID: {https_monitor_id}")

    # Resume monitoring
    print("\n=== Resuming monitor ===")
    client.cert.monitors.resume(https_monitor_id)
    print(f"Resumed monitor ID: {https_monitor_id}")

    # ===================================================================
    # Cleanup
    # ===================================================================
    print("\n=== Cleaning up - Deleting created resources ===")

    # Delete monitors
    client.cert.monitors.delete(https_monitor_id)
    print(f"Deleted HTTPS monitor ID: {https_monitor_id}")

    client.cert.monitors.delete(smtps_monitor_id)
    print(f"Deleted SMTPS monitor ID: {smtps_monitor_id}")

    # Delete profile
    client.cert.profiles.delete(profile_id)
    print(f"Deleted profile ID: {profile_id}")

    print("\n=== Certificate Monitoring Example Complete ===")

except Exception as e:
    print(f"API Error: {e}")
    sys.exit(1)
