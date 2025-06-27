"""
Test cases for the Recipe API endpoints.
"""

from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Recipe

from recipe.serializers import RecipeSerializer


RECIPE_URL = reverse("recipe:recipe-list")

def create_recipe(user, **params):
    """Create and return a sample recipe."""
    defaults = {
        "title": "Sample Recipe",
        "description": "Sample Description",
        "time_minutes": 22,
        "price": Decimal("5.25"),
        "link": "http://example.com/recipe.pdf",
    }
    defaults.update(params)

    recipe = Recipe.objects.create(user=user, **defaults)
    return recipe


## create a public recipe APITest class
class PublicRecipeAPITests(TestCase):
    """Test the publicly available recipe API."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required to access the recipe API."""
        res = self.client.get(reverse("recipe:recipe-list"))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


## create a private recipe APITest class
class PrivateRecipeAPITests(TestCase):
    """Test the authorized user recipe API."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user@example.com",
            password="testpass123"
        )
        self.client.force_authenticate(user=self.user)
    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes."""
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.all().order_by("-id")
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


    def test_retrieve_recipes_limited_to_user(self):
        """Test retrieving recipes for the authenticated user."""
        other_user = get_user_model().objects.create_user(
            email="other@example.com",
            password="testpass123"
        )
        create_recipe(user=other_user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.filter(user=self.user).order_by("-id")
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


# create recipe serializer test cases
class RecipeSerializerTests(TestCase):
    """Test the recipe serializer."""

    def test_recipe_serializer(self):
        """Test the recipe serializer with a sample recipe."""
        user = get_user_model().objects.create_user(
            email="user@example.com",
            password="testpass123"
        )
        recipe = create_recipe(user=user)

        serializer = RecipeSerializer(recipe)
        self.assertEqual(serializer.data, {
            "id": recipe.id,
            "title": recipe.title,
            "description": recipe.description,
            "time_minutes": recipe.time_minutes,
            "price": str(recipe.price),
            "link": recipe.link,
        })

# create recipe recipeViewSet test cases