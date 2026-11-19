# Generator Labs Python SDK

[![Tests](https://github.com/generator-labs/python-sdk/actions/workflows/tests.yml/badge.svg)](https://github.com/generator-labs/python-sdk/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/generator-labs/python-sdk/branch/master/graph/badge.svg)](https://codecov.io/gh/generator-labs/python-sdk)
[![MyPy](https://img.shields.io/badge/mypy-strict-blue.svg)](http://mypy-lang.org/)
[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

The official Python SDK for the [Generator Labs](https://generatorlabs.com) API v4.0.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [RBL Monitoring](#rbl-monitoring)
  - [List Hosts](#list-hosts)
  - [Get a Single Host](#get-a-single-host)
  - [Create a New Host](#create-a-new-host)
  - [Update a Host](#update-a-host)
  - [Delete a Host](#delete-a-host)
  - [Pause/Resume a Host](#pauseresume-a-host)
  - [Start a Manual RBL Check](#start-a-manual-rbl-check)
  - [Manage RBL Profiles](#manage-rbl-profiles)
  - [Manage RBL Sources](#manage-rbl-sources)
- [Contact Management](#contact-management)
  - [Manage Contacts](#manage-contacts)
  - [Manage Contact Groups](#manage-contact-groups)
- [Certificate Monitoring](#certificate-monitoring)
  - [List Certificate Errors](#list-certificate-errors)
  - [Manage Certificate Monitors](#manage-certificate-monitors)
  - [Manage Certificate Profiles](#manage-certificate-profiles)
  - [Check a Certificate Monitor Now](#check-a-certificate-monitor-now)
  - [Certificate Findings](#certificate-findings)
  - [Count Certificate Errors](#count-certificate-errors)
- [Account](#account)
- [Pagination](#pagination)
- [Request Options](#request-options)
  - [Idempotency Keys](#idempotency-keys)
  - [Request IDs](#request-ids)
  - [Conditional Requests](#conditional-requests)
  - [Field Selection](#field-selection)
- [Webhook Verification](#webhook-verification)
- [Rate Limiting](#rate-limiting)
- [API Structure](#api-structure)
- [Development](#development)
- [Release History](#release-history)
- [Contributing](#contributing)
- [Support](#support)
- [License](#license)

## Features

- Full support for Generator Labs API v4.0
- Automatic retry logic with exponential backoff and `Retry-After` header support
- Configurable timeouts and retry behavior
- Automatic pagination support for large result sets
- RESTful endpoint design with proper HTTP verbs (GET, POST, PUT, DELETE)
- RBL and DNSBL monitoring
- Contact and contact group management
- Manual RBL checks
- Monitoring profiles and sources
- Type-safe with Python 3.11+ type hints and mypy strict mode
- requests.Session with connection pooling
- Async support (coming soon)

## Prerequisites

Before using this library, you must have:

* A Generator Labs account - [Sign up](https://portal.generatorlabs.com/signup/) or [Login](https://portal.generatorlabs.com/login/)
* Valid API credentials (Account SID and Auth Token) from the [Portal](https://portal.generatorlabs.com/login/)
* Python >= 3.11

## Installation

Install via pip:

```bash
pip install generatorlabs
```

## Quick Start

### Initialize the Client

```python
import generatorlabs

# Basic initialization
client = generatorlabs.Client("your_account_sid", "your_auth_token")

# With custom configuration
config = generatorlabs.Config(
    timeout=45,           # Request timeout in seconds
    connect_timeout=10,   # Connection timeout in seconds
    max_retries=5,        # Maximum retry attempts
    retry_backoff=2       # Backoff multiplier (2x: 1s, 2s, 4s, 8s, 16s)
)
client = generatorlabs.Client("your_account_sid", "your_auth_token", config)
```

## RBL Monitoring

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
    host = client.rbl.hosts.get("HT1a2b3c4d5e6f7890abcdef1234567890")
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
        "profile": "RP9f8e7d6c5b4a3210fedcba0987654321",
        "contact_group": [
            "CG4f3e2d1c0b9a8776655443322110fedc",
            "CG5a6b7c8d9e0f1234567890abcdef1234"
        ],
        "tags": ["production", "web"]
    })
    print(result)
except generatorlabs.Exception as e:
    print(e)
```

### Update a Host

```python
try:
    result = client.rbl.hosts.update("HT1a2b3c4d5e6f7890abcdef1234567890", {
        "name": "Updated Mail Server Name",
        "tags": ["production", "web"]
    })
    print(result)
except generatorlabs.Exception as e:
    print(e)
```

### Delete a Host

```python
try:
    result = client.rbl.hosts.delete("HT1a2b3c4d5e6f7890abcdef1234567890")
    print(result)
except generatorlabs.Exception as e:
    print(e)
```

### Pause/Resume a Host

```python
try:
    # Pause monitoring
    client.rbl.hosts.pause("HT1a2b3c4d5e6f7890abcdef1234567890")

    # Resume monitoring
    client.rbl.hosts.resume("HT1a2b3c4d5e6f7890abcdef1234567890")
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

### Manage RBL Profiles

```python
try:
    # List all profiles
    profiles = client.rbl.profiles.get()

    # Get a specific profile
    profile = client.rbl.profiles.get("RP9f8e7d6c5b4a3210fedcba0987654321")

    # Create a new profile
    result = client.rbl.profiles.create({
        "name": "My Custom Profile",
        "entries": [
            "RB1234567890abcdef1234567890abcdef",
            "RB0987654321fedcba0987654321fedcba"
        ]
    })

    # Update a profile
    client.rbl.profiles.update("RP9f8e7d6c5b4a3210fedcba0987654321", {
        "name": "Updated Profile Name",
        "entries": [
            "RB1234567890abcdef1234567890abcdef",
            "RB0987654321fedcba0987654321fedcba"
        ]
    })

    # Delete a profile
    client.rbl.profiles.delete("RP9f8e7d6c5b4a3210fedcba0987654321")
except generatorlabs.Exception as e:
    print(e)
```

### Manage RBL Sources

```python
try:
    # List all sources
    sources = client.rbl.sources.get()

    # Get a specific source
    source = client.rbl.sources.get("RB18c470cc518a09678bb280960dbdd524")

    # Create a custom source
    result = client.rbl.sources.create({
        "host": "custom.rbl.example.com",
        "type": "rbl",
        "custom_codes": ["127.0.0.2", "127.0.0.3"]
    })

    # Update a source
    client.rbl.sources.update("RB18c470cc518a09678bb280960dbdd524", {
        "host": "updated.rbl.example.com",
        "custom_codes": ["127.0.0.2", "127.0.0.3"]
    })

    # Delete a source
    client.rbl.sources.delete("RB18c470cc518a09678bb280960dbdd524")
except generatorlabs.Exception as e:
    print(e)
```

## Contact Management

### Manage Contacts

```python
try:
    # List contacts
    contacts = client.contact.contacts.get()

    # Create a contact
    result = client.contact.contacts.create({
        "contact": "admin@example.com",
        "type": "email",
        "schedule": "every_check",
        "contact_group": [
            "CG4f3e2d1c0b9a8776655443322110fedc",
            "CG5a6b7c8d9e0f1234567890abcdef1234"
        ]
    })

    # Update a contact
    client.contact.contacts.update("COabcdef1234567890abcdef1234567890", {
        "contact": "updated@example.com",
        "contact_group": [
            "CG4f3e2d1c0b9a8776655443322110fedc",
            "CG5a6b7c8d9e0f1234567890abcdef1234"
        ]
    })

    # Confirm a contact
    client.contact.contacts.confirm("COabcdef1234567890abcdef1234567890", {
        "authcode": "123456"
    })

    # Delete a contact
    client.contact.contacts.delete("COabcdef1234567890abcdef1234567890")
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
        "name": "Primary Contacts"
    })

    # Update a contact group
    client.contact.groups.update("CG4f3e2d1c0b9a8776655443322110fed", {
        "name": "Updated Group Name"
    })

    # Delete a contact group
    client.contact.groups.delete("CG4f3e2d1c0b9a8776655443322110fed")
except generatorlabs.Exception as e:
    print(e)
```

## Certificate Monitoring

Certificate monitoring allows you to monitor SSL/TLS certificates for expiration, validity, and configuration issues across HTTPS, SMTPS, IMAPS, and other TLS-enabled services.

### List Certificate Errors

```python
try:
    # List all certificate errors
    errors = client.cert.errors.get()

    # Get a specific error by ID
    error = client.cert.errors.get("CE5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a")

    print(errors)
except generatorlabs.Exception as e:
    print(e)
```

### Manage Certificate Monitors

```python
try:
    # List all certificate monitors
    monitors = client.cert.monitors.get()

    # Get a specific monitor
    monitor = client.cert.monitors.get("CM62944aeeee2b46d7a28221164f38976a")

    # Create a new certificate monitor
    monitor = client.cert.monitors.create({
        "name": "Production Web Server",
        "hostname": "example.com",
        "protocol": "https",
        "profile": "CP79b597e61a984a35b5eb7dcdbc3de53c",
        "contact_group": [
            "CG4f3e2d1c0b9a8776655443322110fedc",
            "CG5a6b7c8d9e0f1234567890abcdef1234"
        ],
        "tags": ["production", "web", "ssl"]
    })

    # Update a monitor
    monitor = client.cert.monitors.update("CM62944aeeee2b46d7a28221164f38976a", {
        "name": "Updated Server Name",
        "tags": ["production", "web", "ssl"]
    })

    # Delete a monitor
    client.cert.monitors.delete("CM62944aeeee2b46d7a28221164f38976a")

    # Pause monitoring
    client.cert.monitors.pause("CM62944aeeee2b46d7a28221164f38976a")

    # Resume monitoring
    client.cert.monitors.resume("CM62944aeeee2b46d7a28221164f38976a")
except generatorlabs.Exception as e:
    print(e)
```

### Manage Certificate Profiles

```python
try:
    # List all certificate profiles
    profiles = client.cert.profiles.get()

    # Get a specific profile
    profile = client.cert.profiles.get("CP79b597e61a984a35b5eb7dcdbc3de53c")

    # Create a new profile
    profile = client.cert.profiles.create({
        "name": "Standard Certificate Profile",
        "expiration_thresholds": [30, 14, 7],
        "alert_on_expiration": True,
        "alert_on_name_mismatch": True,
        "alert_on_misconfigurations": True,
        "alert_on_changes": True
    })

    # Update a profile
    profile = client.cert.profiles.update("CP79b597e61a984a35b5eb7dcdbc3de53c", {
        "expiration_thresholds": [45, 14, 7],
        "alert_on_misconfigurations": True,
        "alert_on_changes": True
    })

    # Delete a profile
    client.cert.profiles.delete("CP79b597e61a984a35b5eb7dcdbc3de53c")
except generatorlabs.Exception as e:
    print(e)
```

### Check a Certificate Monitor Now

```python
try:
    # Queue a check of a monitor now, instead of waiting for its next scheduled check
    check = client.cert.monitors.check("CM62944aeeee2b46d7a28221164f38976a")

    print(check["data"]["status"])
except generatorlabs.Exception as e:
    print(e)
```

### Certificate Findings

Findings are everything the last check of each active monitor found: errors, warnings and notices, whatever the profile's alert settings. Some findings can be dismissed, and restored later.

```python
try:
    # List the current findings, one entry per monitor
    findings = client.cert.findings.get()

    # Include the findings dismissed from each monitor
    findings = client.cert.findings.get({"dismissed": 1})

    # Dismiss findings on named monitors (leave "monitors" out for every monitor that has them)
    client.cert.findings.dismiss({
        "finding_id": ["CERT_CAA01", "CERT_CAA02"],
        "monitors": ["CM62944aeeee2b46d7a28221164f38976a"]
    })

    # Restore dismissed findings
    client.cert.findings.restore({"finding_id": "CERT_CAA01"})
except generatorlabs.Exception as e:
    print(e)
```

### Count Certificate Errors

```python
try:
    # The number of current certificate warnings and errors, as an int
    count = client.cert.errors.count()

    print(count)
except generatorlabs.Exception as e:
    print(e)
```

## Account

```python
try:
    # The account: balance, whether scheduled checks are running, and plan usage
    account = client.account.get()

    # The account balance, as a float
    balance = client.account.balance()

    # Usage by month, for the last 3 months
    usage = client.account.usage({"months": 3})

    # Pause and resume the account's scheduled checks
    client.account.pause_checks()
    client.account.resume_checks()
except generatorlabs.Exception as e:
    print(e)
```

## Pagination

List endpoints return paginated results. You can manually pass `page` and `page_size` parameters, or use the `get_all()` helper to automatically fetch every page and return a flat list of all items:

```python
try:
    # Get all hosts across all pages (default page_size: 100)
    all_hosts = client.rbl.hosts.get_all()

    for host in all_hosts:
        print(f"{host['name']} - {host['host']}")

    # With a custom page size
    all_hosts = client.rbl.hosts.get_all(page_size=50)

except generatorlabs.Exception as e:
    print(e)
```

The `get_all()` method is available on all list endpoints:

- `client.rbl.hosts.get_all()`
- `client.rbl.profiles.get_all()`
- `client.rbl.sources.get_all()`
- `client.rbl.listings.get_all()`
- `client.contact.contacts.get_all()`
- `client.contact.groups.get_all()`
- `client.cert.monitors.get_all()`
- `client.cert.profiles.get_all()`
- `client.cert.errors.get_all()`

## Request Options

Every resource method takes these keyword arguments after its own: `idempotency_key`, `request_id`, `if_none_match` and `fields`.

### Idempotency Keys

Requests that create something (`create`), a contact `resend` or `confirm`, the certificate monitor `delete`, and the two check requests (`rbl.check.start`, `cert.monitors.check`) are sent with an `Idempotency-Key` header. The SDK generates one key per call and sends the same key on every automatic retry of that call, so a retry after a timeout never creates, sends, bills or deletes anything twice. Pass your own key to make a repeat of the call from your code safe as well:

```python
host = client.rbl.hosts.create({
    "name": "My Mail Server",
    "host": "192.168.1.100",
    "profile": "RP9f8e7d6c5b4a3210fedcba9876543210",
    "contact_group": ["CG4f3e2d1c0b9a8776655443322110fedc"]
}, idempotency_key="b0e1f6a2-4d7c-4b43-9d3c-3f1c5a9f2e11")

# True when the API answered with the result of an earlier request with the same key
print(host.replayed)
```

The same key with a different request is refused with a 422.

### Request IDs

Every response carries an `X-Request-Id`, available as `request_id` on the response and on `generatorlabs.Exception`. Quote it when you contact support about a request. You can also send your own (1 to 64 letters, digits, `-`, `_`, `.` or `:`):

```python
try:
    hosts = client.rbl.hosts.get(request_id="my-request-1")
    print(hosts.request_id)
except generatorlabs.Exception as e:
    print(e.status_code, e.request_id)
```

### Conditional Requests

Every `GET` response carries an `ETag`. Send it back as `if_none_match`: when nothing has changed the API answers `304 Not Modified`, and the response has `not_modified` set and no data.

```python
hosts = client.rbl.hosts.get()

later = client.rbl.hosts.get(if_none_match=hosts.etag)
if not later.not_modified:
    hosts = later
```

### Field Selection

Any `GET` takes `fields` (a list, or a comma-separated string) to keep only those keys in each object of `data`. A nested key is written with a dot. A field no object has is refused with a 422.

```python
host = client.rbl.hosts.get("HT1a2b3c4d5e6f7890abcdef1234567890", fields=["id", "host", "listed"])

hosts = client.rbl.hosts.get({"page_size": 50}, fields="id,host")
```

## Webhook Verification

The SDK includes a helper for verifying incoming webhook signatures. Each webhook is assigned a signing secret (available in the Portal), which is used to compute an HMAC-SHA256 signature sent with every request in the `X-Webhook-Signature` header.

```python
from generatorlabs import Webhook, Exception

header = request.headers.get('X-Webhook-Signature', '')
body = request.get_data(as_text=True)
secret = os.getenv('GENERATOR_LABS_WEBHOOK_SECRET')

try:
    payload = Webhook.verify(body, header, secret)

    # payload is the decoded event data
    print(payload['event'])

except Exception as e:
    # Signature verification failed
    return jsonify({'error': 'Invalid signature'}), 403
```

The default timestamp tolerance is 5 minutes. You can customize it (in seconds), or pass `0` to disable:

```python
payload = Webhook.verify(body, header, secret, 600)  # 10-minute tolerance
payload = Webhook.verify(body, header, secret, 0)    # disable timestamp check
```

See `examples/webhook_verification.py` for a complete example.

## API Documentation

Full API documentation is available at the [Generator Labs Developer Site](https://docs.generatorlabs.com/api/v4/).

## Rate Limiting

The API enforces two layers of rate limiting:

- **Hourly limit**: 1,000 requests per hour per application
- **Per-second limit**: varies by endpoint — 100 RPS for read operations, 50 RPS for write operations, and 20 RPS for manual check start

When a rate limit is exceeded, the API returns HTTP 429 with a `Retry-After` header indicating how many seconds to wait. The SDK automatically respects this header during retries, falling back to exponential backoff for other retryable errors. A `Retry-After` longer than 60 seconds is not waited out: the 429 is raised as the error instead.

All API responses include IETF draft rate limit headers, accessible via the `rate_limit_info` attribute on every response:

| Header | Description | Example |
|--------|-------------|---------|
| `RateLimit-Limit` | Active rate limit policies | `1000;w=3600, 100;w=1` |
| `RateLimit-Remaining` | Requests remaining in the most restrictive window | `95` |
| `RateLimit-Reset` | Seconds until the most restrictive window resets | `1` |

```python
response = client.rbl.hosts.get()

# Access response data (bracket notation works as before)
hosts = response['data']

# Access rate limit info
if response.rate_limit_info is not None:
    print(f"Remaining: {response.rate_limit_info.remaining}")
    print(f"Reset: {response.rate_limit_info.reset}s")
```

## API Structure

The v4.0 API follows a RESTful design with four main resource namespaces:

### Account Namespace (`client.account`)

- **get** - The account, its balance and plan usage
- **balance** - The account balance
- **usage** - Usage by month
- **pause_checks** / **resume_checks** - Pause and resume the account's scheduled checks

### RBL Namespace (`client.rbl`)

- **hosts** - List, get, create, update, delete, pause, and resume hosts
- **listings** - Get currently listed hosts
- **check** - Start manual checks and get status
- **profiles** - List, get, create, update, and delete monitoring profiles
- **sources** - List, get, create, update, delete, pause, and resume RBL sources

### Contact Namespace (`client.contact`)

- **contacts** - List, get, create, update, delete, pause, resume, confirm, and resend contacts
- **groups** - List, get, create, update, and delete contact groups

### Certificate Namespace (`client.cert`)

- **errors** - List and count certificate errors
- **findings** - List, dismiss, and restore certificate findings
- **monitors** - List, get, create, update, delete, pause, resume, and check certificate monitors
- **profiles** - List, get, create, update, and delete certificate monitoring profiles

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

### v2.1.0 (2026-11-19)
* Minimum Python version bumped to 3.11
* Added `client.account` (account, balance, usage, pause and resume scheduled checks)
* Added `client.cert.findings` (list, dismiss, restore), `client.cert.monitors.check()` and `client.cert.errors.count()`
* Added request options: `idempotency_key`, `request_id`, `if_none_match` and `fields`
* Automatic `Idempotency-Key` on requests that create something or start a check, reused on every retry
* `Response` exposes `request_id`, `etag`, `replayed` and `not_modified`; `Exception` carries the `request_id`
* A `Retry-After` longer than 60 seconds is raised as the error, not waited out
* `generatorlabs.Exception` now extends the built-in `Exception`, so `except Exception:` catches SDK errors

### v2.0.1 (2026-06-19)
* Error detection now reads the API `status_code` and `status_message`; any `status_code` (or HTTP status) of 400 or greater raises `Exception` with the API message
* `Exception` now carries a `status_code` attribute
* The response body is parsed before the status is evaluated, preserving the API error message

### v2.0.0 (2026-01-31)
* Complete rewrite for Generator Labs API v4.0
* RESTful endpoint design with proper HTTP verbs
* Updated to use Generator Labs branding (formerly RBLTracker)
* Minimum Python version bumped to 3.8
* Added full pytest test coverage
* Added mypy strict type checking
* Added GitHub Actions CI/CD workflow
* Organized endpoints under `/rbl/`, `/contact/`, and `/cert/` namespaces
* Added support for PUT and DELETE methods
* Improved error handling for v4.0 response format
* Full type hints throughout the codebase
* Automatic `Retry-After` header support on 429 rate limit responses
* `Response` wrapper (dict-like) exposes per-request rate limit info (`rate_limit_info`)
* Added `RateLimitInfo` class with `limit`, `remaining`, and `reset` attributes
* Webhook signature verification with HMAC-SHA256 and constant-time comparison
* Automatic pagination via `get_all()` for large result sets

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
