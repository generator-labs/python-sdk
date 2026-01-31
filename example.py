#!/usr/bin/env python3
#
# This file is part of the Generator Labs Python SDK package.
#
# (c) Generator Labs <support@generatorlabs.com>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#

"""Example usage of the Generator Labs Python SDK."""

import generatorlabs

# Initialize the client
client = generatorlabs.Client("your_account_sid", "your_auth_token")

# List hosts
try:
    hosts = client.rbl.hosts.get({"page_size": 10, "page": 1})
    print(hosts)
except generatorlabs.Exception as e:
    print(f"Error: {e}")

# Get a single host
try:
    host = client.rbl.hosts.get("HT1a2b3c4d5e6f7890abcdef1234567890")
    print(host)
except generatorlabs.Exception as e:
    print(f"Error: {e}")

# Create a new host
try:
    result = client.rbl.hosts.create({
        "name": "My Mail Server",
        "host": "192.168.1.100",
        "type": "rbl",
        "rbl_profile": "RP9f8e7d6c5b4a3210fedcba0987654321",
        "contact_group": "CG4f3e2d1c0b9a8776655443322110fed"
    })
    print(result)
except generatorlabs.Exception as e:
    print(f"Error: {e}")

# Update a host
try:
    result = client.rbl.hosts.update("HT1a2b3c4d5e6f7890abcdef1234567890", {
        "name": "Updated Mail Server Name"
    })
    print(result)
except generatorlabs.Exception as e:
    print(f"Error: {e}")

# Delete a host
try:
    result = client.rbl.hosts.delete("HT1a2b3c4d5e6f7890abcdef1234567890")
    print(result)
except generatorlabs.Exception as e:
    print(f"Error: {e}")

# Pause/Resume a host
try:
    client.rbl.hosts.pause("HT1a2b3c4d5e6f7890abcdef1234567890")
    client.rbl.hosts.resume("HT1a2b3c4d5e6f7890abcdef1234567890")
except generatorlabs.Exception as e:
    print(f"Error: {e}")

# Start a manual RBL check
try:
    result = client.rbl.check.start({
        "host": "192.168.1.100",
        "callback": "https://myserver.com/callback",
        "details": 1
    })
    check_id = result["data"]["id"]

    # Get check status
    status = client.rbl.check.status(check_id, {"details": 1})
    print(status)
except generatorlabs.Exception as e:
    print(f"Error: {e}")

# Manage contacts
try:
    # List contacts
    contacts = client.contact.contacts.get()
    print(contacts)

    # Create a contact
    result = client.contact.contacts.create({
        "email": "admin@example.com",
        "type": "email"
    })
    print(result)

    # Update a contact
    client.contact.contacts.update("COabcdef1234567890abcdef1234567890", {
        "email": "updated@example.com"
    })

    # Confirm a contact
    client.contact.contacts.confirm("COabcdef1234567890abcdef1234567890", {
        "authcode": "123456"
    })

    # Delete a contact
    client.contact.contacts.delete("COabcdef1234567890abcdef1234567890")
except generatorlabs.Exception as e:
    print(f"Error: {e}")

# Manage contact groups
try:
    # List contact groups
    groups = client.contact.groups.get()
    print(groups)

    # Create a contact group
    result = client.contact.groups.create({
        "name": "Primary Contacts",
        "contacts": "CT123...,CT456..."
    })
    print(result)

    # Update a contact group
    client.contact.groups.update("CG4f3e2d1c0b9a8776655443322110fed", {
        "name": "Updated Group Name"
    })

    # Delete a contact group
    client.contact.groups.delete("CG4f3e2d1c0b9a8776655443322110fed")
except generatorlabs.Exception as e:
    print(f"Error: {e}")
