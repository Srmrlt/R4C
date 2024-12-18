from datetime import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase

from robots.validators import RobotDataValidator


class RobotDataValidatorTests(TestCase):
    def test_validate_valid_data(self):
        data = {
            "model": "R2",
            "version": "D2",
            "created": "2022-12-31 23:59:59"
        }
        validated = RobotDataValidator.validate(data)
        self.assertEqual(validated["model"], "R2")
        self.assertEqual(validated["version"], "D2")
        self.assertIsInstance(validated["created"], datetime)

    def test_missing_fields(self):
        data = {
            "model": "R2",
            "created": "2022-12-31 23:59:59"
        }
        with self.assertRaisesRegex(
                ValidationError,
                "Field 'version' is required."
        ):
            RobotDataValidator.validate_required_fields(data)

    def test_invalid_model_format(self):
        data = "R22"
        with self.assertRaisesRegex(
                ValidationError,
                "Model must be exactly 2 characters long"
        ):
            RobotDataValidator.validate_model(data)

    def test_invalid_version_format(self):
        data = "D2222"
        with self.assertRaisesRegex(
                ValidationError,
                "Version must be 2-3 characters long"
        ):
            RobotDataValidator.validate_version(data)

    def test_invalid_date_format(self):
        data = "not a date"
        with self.assertRaisesRegex(
                ValidationError,
                "Invalid date format"
        ):
            RobotDataValidator.validate_created_date(data)
