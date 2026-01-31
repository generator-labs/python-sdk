# Generator Labs Python SDK

[![Tests](https://github.com/generator-labs/python-sdk/actions/workflows/tests.yml/badge.svg)](https://github.com/generator-labs/python-sdk/actions/workflows/tests.yml)
[![MyPy](https://img.shields.io/badge/mypy-strict-blue.svg)](http://mypy-lang.org/)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

The official Python SDK for the [Generator Labs](https://generatorlabs.com) API v4.0.

## Features

- Full support for Generator Labs API v4.0
- RESTful endpoint design with proper HTTP verbs (GET, POST, PUT, DELETE)
- RBL and DNSBL monitoring
- Contact and contact group management
- Manual RBL checks
- Monitoring profiles and sources
- Type-safe with Python 3.8+ type hints
- Async support (coming soon)

## Prerequisites

Before using this library, you must have:

* A Generator Labs account - [Sign up](https://portal.generatorlabs.com/signup/) or [Login](https://portal.generatorlabs.com/login/)
* Valid API credentials (Account SID and Auth Token) from the [Portal](https://portal.generatorlabs.com/login/)
* Python >= 3.8

## Installation

Install via pip:

```bash
pip install generatorlabs
```

## Quick Start

### Initialize the Client

```python
import generatorlabs

client = generatorlabs.Client("your_account_sid", "your_auth_token")
```

### List Hosts

```python
try:
    hosts = client.rbl.hosts.get({"page_size": 10, "page": 1})
    print(hosts)
except generatorlabs.Exception as e:
    print(e)
```

### Get a Single Host

```python
try:
    host = client.rbl.hosts.get("HTee06c4fa7c23aa8a3a4e8d66922b0834")
    print(host)
except generatorlabs.Exception as e:
    print(e)
```

### Create a New Host

```python
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
    print(e)
```

### Update a Host

```python
try:
    result = client.rbl.hosts.update("HTee06c4fa7c23aa8a3a4e8d66922b0834", {
        "name": "Updated Mail Server Name"
    })
    print(result)
except generatorlabs.Exception as e:
    print(e)
```

### Delete a Host

```python
try:
    result = client.rbl.hosts.delete("HTee06c4fa7c23aa8a3a4e8d66922b0834")
    print(result)
except generatorlabs.Exception as e:
    print(e)
```

### Pause/Resume a Host

```python
try:
    # Pause monitoring
    client.rbl.hosts.pause("HTee06c4fa7c23aa8a3a4e8d66922b0834")

    # Resume monitoring
    client.rbl.hosts.resume("HTee06c4fa7c23aa8a3a4e8d66922b0834")
except generatorlabs.Exception as e:
    print(e)
```

### Start a Manual RBL Check

```python
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
    print(e)
```

### Manage Contacts

```python
try:
    # List contacts
    contacts = client.contact.contacts.get()

    # Create a contact
    result = client.contact.contacts.create({
        "email": "admin@example.com",
        "type": "email"
    })

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
    print(e)
```

### Manage Contact Groups

```python
try:
    # List contact groups
    groups = client.contact.groups.get()

    # Create a contact group
    result = client.contact.groups.create({
        "name": "Primary Contacts",
        "contacts": "CT123...,CT456..."
    })

    # Update a contact group
    client.contact.groups.update("CG1234567890abcdef", {
        "name": "Updated Group Name"
    })

    # Delete a contact group
    client.contact.groups.delete("CG1234567890abcdef")
except generatorlabs.Exception as e:
    print(e)
```

## API Documentation

Full API documentation is available at the [Generator Labs Developer Site](https://docs.generatorlabs.com/api/v4/).

## API Structure

The v4.0 API follows a RESTful design with two main resource namespaces:

### RBL Namespace (`client.rbl`)

- **hosts** - List, get, create, update, delete, pause, and resume hosts
- **listings** - Get currently listed hosts
- **check** - Start manual checks and get status
- **profiles** - List, get, create, update, and delete monitoring profiles
- **sources** - List, get, create, update, delete, pause, and resume RBL sources

### Contact Namespace (`client.contact`)

- **contacts** - List, get, create, update, delete, pause, resume, confirm, and resend contacts
- **groups** - List, get, create, update, and delete contact groups

## Development

### Running Tests

```bash
pytest
```

### Running Type Checking

```bash
mypy generatorlabs
```

### Running Tests with Coverage

```bash
pytest --cov=generatorlabs --cov-report=term-missing
```

## Release History

### v2.0.0 (2026-01-31)
* Complete rewrite for Generator Labs API v4.0
* RESTful endpoint design with proper HTTP verbs
* Updated to use Generator Labs branding (formerly RBLTracker)
* Minimum Python version bumped to 3.8
* Added full pytest test coverage
* Added mypy strict type checking
* Added GitHub Actions CI/CD workflow
* Organized endpoints under `/rbl/` and `/contact/` namespaces
* Added support for PUT and DELETE methods
* Improved error handling for v4.0 response format
* Full type hints throughout the codebase

### v1.1.0
* Updated to use the new API endpoint URL
* Added support for Monitoring Profiles
* Added support for the ACLs endpoint

### v1.0.0
* Initial release

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For questions, issues, or feature requests:

- GitHub Issues: https://github.com/generator-labs/python-sdk/issues
- Email: support@generatorlabs.com
- Documentation: https://docs.generatorlabs.com

## License

This library is released under the MIT License. See [LICENSE](LICENSE) for details.

## Links

- [Generator Labs Website](https://generatorlabs.com/)
- [API Documentation](https://docs.generatorlabs.com/api/v4/)
- [Sign Up](https://portal.generatorlabs.com/signup/)
- [Portal Login](https://portal.generatorlabs.com/login/)
