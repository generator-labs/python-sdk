#
# This file is part of the Generator Labs Python SDK package.
#
# (c) Generator Labs <support@generatorlabs.com>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#

"""Webhook signature verification utility."""

import hashlib
import hmac
import json
import time
from typing import Any, Dict

from .exception import Exception

#: Default tolerance in seconds for timestamp validation (5 minutes).
DEFAULT_TOLERANCE = 300


class Webhook:
    """Webhook signature verification utility.

    Verifies that incoming webhook requests were sent by Generator Labs
    using HMAC-SHA256 signatures.

    Example::

        from generatorlabs import Webhook

        payload = Webhook.verify(body, header, signing_secret)
    """

    @staticmethod
    def verify(
        body: str,
        header: str,
        secret: str,
        tolerance: int = DEFAULT_TOLERANCE,
    ) -> Dict[str, Any]:
        """Verify a webhook signature and return the decoded payload.

        Args:
            body: The raw request body string
            header: The X-Webhook-Signature header value
            secret: Your webhook's signing secret
            tolerance: Maximum age in seconds (0 to disable, default: 300)

        Returns:
            The decoded JSON payload as a dictionary

        Raises:
            Exception: If verification fails
        """
        if not header:
            raise Exception("Missing X-Webhook-Signature header.")

        # Parse the header: t=timestamp,v1=signature
        parts: Dict[str, str] = {}
        for part in header.split(","):
            key_value = part.split("=", 1)
            if len(key_value) == 2:
                parts[key_value[0]] = key_value[1]

        if "t" not in parts or "v1" not in parts:
            raise Exception("Invalid X-Webhook-Signature header format.")

        # Check timestamp tolerance
        if tolerance > 0 and abs(int(time.time()) - int(parts["t"])) > tolerance:
            raise Exception("Webhook timestamp is outside the tolerance window.")

        # Compute and compare the signature
        expected = hmac.new(
            secret.encode("utf-8"),
            f"{parts['t']}.{body}".encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

        if not hmac.compare_digest(expected, parts["v1"]):
            raise Exception("Webhook signature verification failed.")

        # Decode and return the payload
        return json.loads(body)
