#!/usr/bin/env python3
""" 
parameterizing a unit tests
"""
import unittest
from parameterized import parameterized
from unittest.mock import patch
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """testing the function access_nested_map"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected_result):
        """test access_nested_map"""
        self.assertEqual(access_nested_map(nested_map, path), expected_result)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_result):
        """test access_nested_map_exception"""
        self.assertRaises(expected_result)


class TestGetJson(unittest.TestCase):
    """testing the function get_json"""
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    
    @patch('utils.requests.get')
    def test_get_json(self, test_url, test_payload, mock_requests_get):
        # Mock the requests.get method to return a Mock object with json method
        mock_response = unittest.mock.Mock()
        mock_response.json.return_value = test_payload
        mock_requests_get.return_value = mock_response

        # Call the get_json function and check if it returns the expected result
        result = get_json(test_url)
        self.assertEqual(result, test_payload)

        # Check if requests.get was called exactly once with the test_url argument
        mock_requests_get.assert_called_once_with(test_url)


class TestClass:
    def a_method(self):
        return 42

    @memoize
    def a_property(self):
        return self.a_method()

class TestMemoize(unittest.TestCase):

    def test_memoize(self):
        test_instance = TestClass()

        # Mock the a_method of TestClass
        with patch.object(TestClass, 'a_method') as mock_a_method:
            # Set the return value of the mocked a_method
            mock_a_method.return_value = 42

            # Call the a_property method twice
            result1 = test_instance.a_property()
            result2 = test_instance.a_property()

            # Check that a_method was only called once
            mock_a_method.assert_called_once()

            # Check that the results are equal
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

if __name__ == "__main__":
    unittest.main()