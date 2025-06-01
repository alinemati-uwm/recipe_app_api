"""
Sample test file for the app module.
"""
from django.test import SimpleTestCase

from app import calc


class ClacTests(SimpleTestCase):
    """Test the calc module."""

    def test_add(self):
        """Test the add function."""
        res = calc.add(5, 6)
        self.assertEqual(res, 11)
