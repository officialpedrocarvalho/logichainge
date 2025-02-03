# Validator for the title field
from rest_framework.exceptions import ValidationError

from app.models import Task


def validate_title(title, user):
    if not title:
        raise ValidationError("Title cannot be empty.")
    if Task.objects.filter(title=title, user=user).exists():
        raise ValidationError("A task with this title already exists.")


def validate_description(description):
    if not description:
        raise ValidationError("Description cannot be empty.")
    if len(description) > 1000:
        raise ValidationError("This field must be less than 1000 characters.")
