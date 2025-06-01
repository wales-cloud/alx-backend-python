#!/usr/bin/env python3
"""Unit tests for GithubOrgClient.org and related properties"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
import fixtures
import requests

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


class TestGithubOrgClient(unittest.TestCase):
    """Tests for the GithubOrgClient class"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that org property calls get_json once with expected URL"""
        payload = {"login": org_name, "id": 1234}
        mock_get_json.return_value = payload

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, payload)

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    @patch.object(GithubOrgClient, 'org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test that _public_repos_url returns expected value from org payload"""
        mock_org.return_value = {
            "repos_url": "https://api.github.com/orgs/test/repos"
        }
        client = GithubOrgClient("test")
        self.assertEqual(
            client._public_repos_url,
            "https://api.github.com/orgs/test/repos"
        )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns expected names and mocks were called"""
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
        ]
        mock_get_json.return_value = test_payload

        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new=PropertyMock(
                return_value=(
                    "https://api.github.com/orgs/test/repos"
                )
            )
        ) as mock_url:
            client = GithubOrgClient("test")
            result = client.public_repos()
            self.assertEqual(result, ["repo1", "repo2"])
            mock_get_json.assert_called_once()
            mock_url.assert_called_once()

    @parameterized.expand([
        (
            {"license": {"key": "my_license"}},
            "my_license",
            True
        ),
        (
            {"license": {"key": "other_license"}},
            "my_license",
            False
        ),
        (
            {},
            "my_license",
            False
        ),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns expected boolean based on repo license"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": fixtures.TEST_PAYLOAD[0][0],
        "repos_payload": fixtures.TEST_PAYLOAD[0][1],
        "expected_repos": fixtures.TEST_PAYLOAD[0][2],
        "apache2_repos": fixtures.TEST_PAYLOAD[0][3],
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Set up mock for requests.get().json() using fixture data"""
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        def side_effect(url):
            if url.endswith("/orgs/google"):
                return MockResponse(cls.org_payload)
            if url.endswith("/orgs/google/repos"):
                return MockResponse(cls.repos_payload)
            return MockResponse(None)

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher after all tests run"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected repo list from fixture"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos filters repos by apache-2.0 license"""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )


class MockResponse:
    """Mock response object that returns provided JSON payload"""

    def __init__(self, payload):
        self._payload = payload

    def json(self):
        """Return the JSON payload"""
        return self._payload


if __name__ == "__main__":
    unittest.main()
