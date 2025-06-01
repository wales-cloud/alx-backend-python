#!/usr/bin/env python3
"""Unit tests for GithubOrgClient.org and related properties"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


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
        mock_org.return_value = {"repos_url": "https://api.github.com/orgs/test/repos"}
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
            new=PropertyMock(return_value="https://api.github.com/orgs/test/repos")
        ) as mock_repos_url:
            client = GithubOrgClient("test")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2"])
            mock_get_json.assert_called_once()
            mock_repos_url.assert_called_once()


if __name__ == "__main__":
    unittest.main()
