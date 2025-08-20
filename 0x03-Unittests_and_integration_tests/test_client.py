#!/usr/bin/env python3
"""Unit & Integration tests for the GithubOrgClient."""

import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class

from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient methods that only mock local helpers."""

    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"}),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, expected, mock_get_json):
        """GithubOrgClient.org returns the payload from get_json."""
        mock_get_json.return_value = expected
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self):
        """_public_repos_url reads from org['repos_url']."""
        expected_url = "https://api.github.com/orgs/google/repos"
        payload = {"repos_url": expected_url}
        with patch.object(GithubOrgClient, "org", new_callable=PropertyMock, return_value=payload):
            client = GithubOrgClient("google")
            self.assertEqual(client._public_repos_url, expected_url)

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """public_repos returns repo names from get_json list of dicts."""
        mock_repos_url = "https://api.github.com/orgs/google/repos"
        mock_payload = [{"name": "repo1"}, {"name": "repo2"}, {"name": "repo3"}]
        mock_get_json.return_value = mock_payload
        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=PropertyMock, return_value=mock_repos_url):
            client = GithubOrgClient("google")
            self.assertEqual(client.public_repos(), ["repo1", "repo2", "repo3"])
            mock_get_json.assert_called_once_with(mock_repos_url)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """has_license identifies license matches."""
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)


# ------------------------ INTEGRATION TESTS ------------------------ #

@parameterized_class(  # parameterize with fixtures from fixtures.py
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    [
        (org_payload, repos_payload, expected_repos, apache2_repos),
    ],
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration tests for GithubOrgClient.public_repos.

    Only external requests are mocked (requests.get). We verify that:
    - public_repos() returns expected repo names
    - public_repos(license="apache-2.0") filters correctly
    """

    @classmethod
    def setUpClass(cls):
        """
        Start a patcher of requests.get and set a side_effect so that
        requests.get(url).json() returns the right fixture for each URL.
        """
        # must be named get_patcher per checker
        cls.get_patcher = patch("requests.get")

        def _mocked_get(url, *args, **kwargs):
            m = Mock()
            # URLs we anticipate:
            # 1) org endpoint: https://api.github.com/orgs/<org>
            # 2) repos endpoint: value of org_payload["repos_url"] OR /orgs/<org>/repos
            if url.endswith("/orgs/google") or url.endswith("/orgs/abc"):
                m.json.return_value = cls.org_payload
            elif url == cls.org_payload.get("repos_url"):
                m.json.return_value = cls.repos_payload
            # Fallback: if tests hit org repos path directly
            elif url.endswith("/repos"):
                m.json.return_value = cls.repos_payload
            else:
                m.json.return_value = {}
            return m

        cls.mock_get = cls.get_patcher.start()
        cls.mock_get.side_effect = _mocked_get

    @classmethod
    def tearDownClass(cls):
        """Stop the requests.get patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """public_repos returns all repo names as expected by fixture."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """public_repos filters by apache-2.0 license correctly."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(license="apache-2.0"), self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
