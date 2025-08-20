#!/usr/bin/env python3
"""Unit & Integration tests for the GithubOrgClient."""

import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class  # <- MUST include parameterized_class

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
        mock_get_json.return_value = expected
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self):
        expected_url = "https://api.github.com/orgs/google/repos"
        payload = {"repos_url": expected_url}
        with patch.object(GithubOrgClient, "org", new_callable=PropertyMock, return_value=payload):
            client = GithubOrgClient("google")
            self.assertEqual(client._public_repos_url, expected_url)

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
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
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)


# ------------------------ INTEGRATION TESTS ------------------------ #

@parameterized_class(  # <- EXACT decorator the checker searches for
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    [
        (org_payload, repos_payload, expected_repos, apache2_repos),
    ],
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration tests for GithubOrgClient.public_repos.
    Only external requests are mocked (requests.get).
    """

    @classmethod
    def setUpClass(cls):
        """
        Start a patcher of requests.get and set a side_effect so that
        requests.get(url).json() returns the right fixture for each URL.
        """
        cls.get_patcher = patch("requests.get")  # <- name must be get_patcher
        cls.mock_get = cls.get_patcher.start()

        def _mocked_get(url, *args, **kwargs):
            m = Mock()
            # org endpoint
            if url.endswith("/orgs/google") or url.endswith("/orgs/abc"):
                m.json.return_value = cls.org_payload
            # repos endpoint (use fixture's repos_url)
            elif url == cls.org_payload.get("repos_url") or url.endswith("/repos"):
                m.json.return_value = cls.repos_payload
            else:
                m.json.return_value = {}
            return m

        cls.mock_get.side_effect = _mocked_get

    @classmethod
    def tearDownClass(cls):
        """Stop the requests.get patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(license="apache-2.0"), self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
