import datetime
import re

from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_datetime


class RobotDataValidator:
    """
    Validator for robot data.
    """
    REQUIRED_FIELDS = ['model', 'version', 'created']
    MODEL_PATTERN = r'^[A-Z0-9]{2}$'
    VERSION_PATTERN = r'^[A-Z0-9]{2,3}$'

    @classmethod
    def validate(cls, data: dict) -> dict:
        """
        Main method to validate input data.
        """
        cls.validate_required_fields(data)
        model = cls.validate_model(data.get('model'))
        version = cls.validate_version(data.get('version'))
        created = cls.validate_created_date(data.get('created'))

        return {
            "model": model,
            "version": version,
            "created": created
        }

    @classmethod
    def validate_required_fields(cls, data: dict):
        for field in cls.REQUIRED_FIELDS:
            if not data.get(field):
                raise ValidationError(f"Field '{field}' is required.")

    @classmethod
    def validate_model(cls, model: str) -> str:
        if not re.match(cls.MODEL_PATTERN, model):
            raise ValidationError("Model must be exactly 2 characters long and contain only letters and digits.")
        return model

    @classmethod
    def validate_version(cls, version: str) -> str:
        if not re.match(cls.VERSION_PATTERN, version):
            raise ValidationError("Version must be 2-3 characters long and contain only letters and digits.")
        return version

    @classmethod
    def validate_created_date(cls, created: str) -> datetime:
        created_date = parse_datetime(created)
        if created_date is None:
            raise ValidationError("Invalid date format. Use: YYYY-MM-DD HH:MM:SS.")
        return created_date
