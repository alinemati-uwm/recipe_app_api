"""
Django admin customization for the recipe app.

This module configures the Django admin interface for our custom models,
extending the default admin functionality to better match our application needs.
"""

from core import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _


class UserAdmin(BaseUserAdmin):
    """
    Custom admin configuration for our User model.

    Extends the default UserAdmin to work with our email-based authentication
    instead of the default username-based system.
    """

    # Basic display options
    ordering = ["id"]
    list_display = ["email", "name", "is_active", "is_staff"]
    list_filter = ["is_active", "is_staff", "is_superuser"]
    search_fields = ["email", "name"]

    # Detail view fieldsets
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("name",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )

    # Add user form fieldsets
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "name", "password1", "password2"),
            },
        ),
    )

    # Optimization for large databases
    readonly_fields = ["last_login"]


# Register models
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Recipe)
