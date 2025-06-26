"""Tests for the models."""

from decimal import Decimal

from core import models
from django.contrib.auth import get_user_model
from django.test import TestCase


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = "test@example.com"
        password = "testpassword123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized."""
        sample_emails = [
            ("test1@EXAMPLE.COM", "test1@example.com"),
            ("Test2@Example.COM", "test2@example.com"),
            ("TEST3@EXAMPLE.COM", "test3@example.com"),
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email=email, password="sample123")
            self.assertEqual(user.email, expected)

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email=None, password="sample123")

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            email="test@example.com", password="testpassword123"
        )
        self.assertEqual(user.is_superuser, True)
        self.assertEqual(user.is_staff, True)

    def test_create_recipe(self):
        """Test creating a recipe is successful."""
        user = get_user_model().objects.create_user(
            email="test@example.com",
            password="testpassword123",
        )
        recipe = models.Recipe.objects.create(
            user=user,
            title="Test Recipe name",
            time_minutes=5,
            price=Decimal("5.50"),
            description="Sample recipe description",
        )
        # self.assertEqual(recipe.user, user)
        self.assertEqual(str(recipe), recipe.title)
        # self.assertEqual(recipe.time_minutes, 5)
        # self.assertEqual(recipe.price, Decimal("5.99"))
        # self.assertEqual(recipe.description, "Test Description")
