#!/usr/bin/env python3
"""
Example: Verifying webhook signatures

This example shows how to verify incoming webhook requests from Generator Labs
using the SDK's built-in signature verification helper.
"""

import os
import sys
from generatorlabs import Webhook, Exception

# Your webhook's signing secret, available in the Edit Webhook panel of the Portal.
# Store this securely (e.g., environment variable), never hard-code it.
signing_secret = os.getenv('GENERATOR_LABS_WEBHOOK_SECRET')

if not signing_secret:
    print("Error: Set GENERATOR_LABS_WEBHOOK_SECRET environment variable")
    sys.exit(1)


def example_basic_verification(body: str, header: str) -> None:
    """
    Example 1: Basic verification

    Verify the signature with the default 5-minute tolerance window.
    On success, returns the decoded JSON payload as a dictionary.
    Raises an Exception if verification fails.
    """
    try:
        payload = Webhook.verify(body, header, signing_secret)

        print("Webhook verified successfully!")
        print(f"Event: {payload.get('event', 'unknown')}")

    except Exception as e:
        print(f"Verification failed: {e}")


def example_custom_tolerance(body: str, header: str) -> None:
    """
    Example 2: Custom tolerance

    Set a custom tolerance window (in seconds) for timestamp validation.
    Use 0 to disable timestamp checking entirely.
    """
    try:
        # 10-minute tolerance
        payload = Webhook.verify(body, header, signing_secret, 600)
        print(f"Verified with custom tolerance: {payload}")

    except Exception as e:
        print(f"Verification failed: {e}")


def example_flask_endpoint():
    """
    Example 3: Usage with Flask

    A typical Flask webhook endpoint using the SDK verification helper.
    """
    from flask import Flask, request, jsonify

    app = Flask(__name__)

    @app.route('/webhook', methods=['POST'])
    def webhook():
        header = request.headers.get('X-Webhook-Signature', '')
        body = request.get_data(as_text=True)

        try:
            payload = Webhook.verify(body, header, signing_secret)
        except Exception:
            return jsonify({'error': 'Invalid signature'}), 403

        # Process the event
        event = payload.get('event', '')

        if event == 'rbl.host.listed':
            # Handle host listed event
            pass
        elif event == 'rbl.host.delisted':
            # Handle host delisted event
            pass
        elif event == 'billing.balance.alert':
            # Handle low balance alert
            pass

        return jsonify({'status': 'ok'}), 200

    return app
