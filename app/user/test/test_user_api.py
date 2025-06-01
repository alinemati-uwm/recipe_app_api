"""
Test cases for the User API.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

# The URL for creating a user in the API
CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")
ME_USER_URL = reverse("user:me")


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """
    TestCase for public user API endpoints.
    This test class covers the following scenarios:
    - Successful creation of a new user via the public API.
    - Ensuring user passwords are securely hashed and not returned in API responses.
    - Preventing duplicate user creation with the same email and returning
    appropriate error messages.
    Each test simulates HTTP requests to the user API endpoints and verifies both
    the API response and the resulting database state.
    Annotations:
    -----------
    - Uses Django's TestCase for isolated test execution.
    - Utilizes DRF's APIClient for simulating API requests.
    - Ensures compliance with security best practices (e.g., password hashing,
    sensitive data exclusion).
    - Validates error handling for duplicate user registration.
    """

    """Test the public features of the user API."""

    def setUp(self):
        self.client = APIClient()  # Create an instance of the APIClient for making requests

    def test_create_user_success(self):
        """Test creating a user is successful."""
        payload = {
            "email": "test@example.com",
            "password": "testpass123",
            "name": "Test Name",
        }
        # Make a POST request to the user creation URL with the payload
        res = self.client.post(CREATE_USER_URL, payload)

        # assert the response status code is 201 (created)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # assert the user is created in the database
        user = get_user_model().objects.get(email=payload["email"])
        # assert the user password is hashed
        self.assertTrue(user.check_password(payload["password"]))
        # assert the user name is set correctly
        self.assertEqual(user.name, payload["name"])
        # assert the response contains the expected user data
        self.assertNotIn("password", res.data)

    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists."""
        payload = {
            "email": "test@example.com",
            "password": "pw",
            "name": "Test Name",
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["email"], ["user with this email already exists."])

    def test_create_token_for_user(self):
        """Test generates token for valid credentials."""
        user_details = {
            "email": "test@example.com",
            "password": "pw",
        }
        create_user(**user_details)
        res = self.client.post(TOKEN_URL, user_details)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("token", res.data)

    def test_create_user_invalid_email(self):
        payload = {"email": "notanemail", "password": "testpass123", "name": "Test"}
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_short_password(self):
        payload = {"email": "test2@example.com", "password": "123", "name": "Test"}
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", res.data)

    def test_create_token_missing_fields(self):
        res = self.client.post(TOKEN_URL, {"email": "test@example.com"})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", res.data)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users."""
        res = self.client.get(ME_USER_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """TestCase for private user API endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email="test@example.com", password="testpass123", name="Test Name")
        self.client = APIClient()

        # Authenticate the client with the user
        self.client.force_authenticate(user=self.user)

    # Test that the user profile is retrieved successfully
    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user."""
        res = self.client.get(ME_USER_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            res.data,
            {
                "name": self.user.name,
                "email": self.user.email,
            },
        )

    # Test that the user profile is not returned for unauthenticated users
    def test_post_me_not_allowed(self):
        """Test that POST is not allowed on the me url."""
        res = self.client.post(ME_USER_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # Test updating the user profile
    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user."""
        payload = {"name": "Updated Name", "password": "newpassword123"}
        res = self.client.patch(ME_USER_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload["name"])
        self.assertTrue(self.user.check_password(payload["password"]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
