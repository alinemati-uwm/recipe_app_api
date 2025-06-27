"""
Serializer for recipe objects API.
"""

from rest_framework import serializers
from core.models import Recipe

class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipe objects."""
    class Meta:
        model = Recipe
        fields = ["id", "title", "description", "time_minutes", "price", "link"]
        read_only_fields = ["id"]
        