#
# This file is part of the Generator Labs Python SDK package.
#
# (c) Generator Labs <support@generatorlabs.com>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#

"""Tests for the Generator Labs Client."""

import pytest
from generatorlabs import Client, Exception
from generatorlabs.api.rbl import RBL
from generatorlabs.api.contact import Contact
from generatorlabs.api.cert import Cert


class TestClient:
    """Test the Client class."""

    def test_valid_credentials(self) -> None:
        """Test client initialization with valid credentials."""
        client = Client("AC" + "a" * 32, "b" * 64)
        assert client.account_sid == "AC" + "a" * 32
        assert client.auth_token == "b" * 64
        assert client.api_url == "https://api.generatorlabs.com/4.0/"

    def test_invalid_account_sid(self) -> None:
        """Test client initialization with invalid account SID."""
        with pytest.raises(Exception, match="Invalid account SID format"):
            Client("invalid", "b" * 64)

    def test_invalid_auth_token(self) -> None:
        """Test client initialization with invalid auth token."""
        with pytest.raises(Exception, match="Invalid auth token format"):
            Client("AC" + "a" * 32, "invalid")

    def test_rbl_namespace(self) -> None:
        """Test access to RBL namespace."""
        client = Client("AC" + "a" * 32, "b" * 64)
        assert isinstance(client.rbl, RBL)
        # Test lazy loading - should return same instance
        assert client.rbl is client.rbl

    def test_contact_namespace(self) -> None:
        """Test access to Contact namespace."""
        client = Client("AC" + "a" * 32, "b" * 64)
        assert isinstance(client.contact, Contact)
        # Test lazy loading - should return same instance
        assert client.contact is client.contact

    def test_cert_namespace(self) -> None:
        """Test access to Cert namespace."""
        client = Client("AC" + "a" * 32, "b" * 64)
        assert isinstance(client.cert, Cert)
        # Test lazy loading - should return same instance
        assert client.cert is client.cert

    def test_cert_errors_endpoint(self) -> None:
        """Test access to Cert errors endpoint."""
        client = Client("AC" + "a" * 32, "b" * 64)
        # Just verify the endpoint is accessible
        assert hasattr(client.cert, 'errors')
        assert client.cert.errors is not None

    def test_cert_monitors_endpoint(self) -> None:
        """Test access to Cert monitors endpoint."""
        client = Client("AC" + "a" * 32, "b" * 64)
        # Just verify the endpoint is accessible
        assert hasattr(client.cert, 'monitors')
        assert client.cert.monitors is not None

    def test_cert_profiles_endpoint(self) -> None:
        """Test access to Cert profiles endpoint."""
        client = Client("AC" + "a" * 32, "b" * 64)
        # Just verify the endpoint is accessible
        assert hasattr(client.cert, 'profiles')
        assert client.cert.profiles is not None

    def test_version(self) -> None:
        """Test SDK version."""
        assert Client.VERSION == "2.0.0"
