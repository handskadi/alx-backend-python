from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos
import unittest

# ------------------------ INTEGRATION TESTS ------------------------ #

@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration tests for GithubOrgClient.public_repos.
    Only external requests are mocked (requests.get).
    """

    @classmethod
    def setUpClass(cls):
        """
        Patch requests.get and set side_effect so that requests.get(url).json()
        returns the appropriate fixture payload depending on the URL.
        """
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        def _mocked_get(url, *args, **kwargs):
            m = Mock()
            # org endpoint like: https://api.github.com/orgs/<org>
            if url.endswith("/orgs/google") or url.endswith("/orgs/abc"):
                m.json.return_value = cls.org_payload
            # repos endpoint: prefer exact repos_url from the org payload
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
