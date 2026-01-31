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
    host = client.rbl.hosts.get("HTee06c4fa7c23aa8a3a4e8d66922b0834")
    print(host)
except generatorlabs.Exception as e:
    print(f"Error: {e}")

# Create a new host
try:
    result = client.rbl.hosts.create({
        "name": "My Mail Server",
        "host": "192.168.1.100",
        "type": "rbl",
        "rbl_profile": "RP15d4e891d784977cacbfcbb00c48f133",
        "contact_group": "CG37106c6baa1ec90a2b3f5c8ec54afe9d"
    })
    print(result)
except generatorlabs.Exception as e:
    print(f"Error: {e}")

# Update a host
try:
    result = client.rbl.hosts.update("HTee06c4fa7c23aa8a3a4e8d66922b0834", {
        "name": "Updated Mail Server Name"
    })
    print(result)
except generatorlabs.Exception as e:
    print(f"Error: {e}")

# Delete a host
try:
    result = client.rbl.hosts.delete("HTee06c4fa7c23aa8a3a4e8d66922b0834")
    print(result)
except generatorlabs.Exception as e:
    print(f"Error: {e}")

# Pause/Resume a host
try:
    client.rbl.hosts.pause("HTee06c4fa7c23aa8a3a4e8d66922b0834")
    client.rbl.hosts.resume("HTee06c4fa7c23aa8a3a4e8d66922b0834")
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
    client.contact.contacts.update("CT1234567890abcdef", {
        "email": "updated@example.com"
    })

    # Confirm a contact
    client.contact.contacts.confirm("CT1234567890abcdef", {
        "authcode": "123456"
    })

    # Delete a contact
    client.contact.contacts.delete("CT1234567890abcdef")
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
    client.contact.groups.update("CG1234567890abcdef", {
        "name": "Updated Group Name"
    })

    # Delete a contact group
    client.contact.groups.delete("CG1234567890abcdef")
except generatorlabs.Exception as e:
    print(f"Error: {e}")
