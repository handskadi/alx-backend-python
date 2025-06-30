#!/usr/bin/env python3
"""Unit tests for the GithubOrgClient."""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient
# Assuming this is the module containing the class


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for the GithubOrgClient class."""

    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"}),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, expected, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value."""
        # Configure the mock to return the expected value
        mock_get_json.return_value = expected

        # Instantiate the client and call the org method
        client = GithubOrgClient(org_name)
        result = client.org

        # Assertions
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, expected)

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the correct value."""
        expected_url = "https://api.github.com/orgs/google/repos"
        payload = {"repos_url": expected_url}

        # Patch the `org` property to return the mock payload
        with patch.object(GithubOrgClient, "org",
                          new_callable=PropertyMock, return_value=payload):
            client = GithubOrgClient("google")
            # Access the _public_repos_url property
            result = client._public_repos_url
            self.assertEqual(result, expected_url)

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns the correct list of repositories."""
        # Define mock data
        mock_repos_url = "https://api.github.com/orgs/google/repos"
        mock_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        expected_repos = ["repo1", "repo2", "repo3"]

        # Configure the mocks
        mock_get_json.return_value = mock_payload
        with patch.object(GithubOrgClient, "_public_repos_url",
                          new_callable=PropertyMock,
                          return_value=mock_repos_url):
            client = GithubOrgClient("google")

            # Call the public_repos method
            result = client.public_repos

            # Assertions
            # Check if the returned repos match the expected repos
            self.assertEqual(result, expected_repos)
            # Ensure get_json was called once with the correct URL
            mock_get_json.assert_called_once_with(mock_repos_url)
            client._public_repos_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license method for different repo license configs."""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
