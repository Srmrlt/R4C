import json

from django.test import TestCase
from django.urls import reverse


class RobotCreateViewTests(TestCase):
    def test_create_robot_success(self):
        valid_data = {
            "model": "R2",
            "version": "D2",
            "created": "2022-12-31 23:59:59"
        }
        response = self.client.post(
            reverse("robots"),
            data=json.dumps(valid_data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertEqual(response_data["message"], "Robot created successfully")
        self.assertEqual(response_data["robot_id"], 1)

    def test_create_robot_invalid_data(self):
        invalid_data = {
            "model": "R2",
            "created": "2022-12-31 23:59:59"
        }
        response = self.client.post(
            reverse("robots"),
            data=json.dumps(invalid_data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertIn("Field 'version' is required.", response_data["error"])

    def test_create_robot_invalid_json(self):
        invalid_json = "not a json"
        response = self.client.post(
            reverse("robots"),
            data=invalid_json,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertEqual(response_data["error"], "Invalid JSON data")
