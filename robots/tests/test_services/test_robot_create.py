from datetime import datetime

from django.test import TestCase

from robots.models import Robot
from robots.services import RobotCreate


class RobotCreateTests(TestCase):
    def test_create_robot_success(self):
        validated_data = {
            "model": "R2",
            "version": "D2",
            "created": datetime(2022, 12, 31, 23, 59, 59)
        }
        robot = RobotCreate.create_robot(validated_data)

        self.assertEqual(Robot.objects.count(), 1)
        self.assertEqual(robot.serial, "R2-D2")
        self.assertEqual(robot.model, "R2")
        self.assertEqual(robot.version, "D2")
        self.assertEqual(robot.created.strftime('%Y-%m-%d %H:%M:%S'), "2022-12-31 23:59:59")

    def test_generate_serial(self):
        data = {"model": "X1", "version": "LT"}
        generated_data = RobotCreate._generate_serial(data)
        self.assertEqual(generated_data["serial"], "X1-LT")

    def test_save_robot_success(self):
        """
        Test that the _save_robot method creates a robot in the database.
        """
        data = {
            "serial": "X1-LT",
            "model": "X1",
            "version": "LT",
            "created": datetime(2022, 12, 31, 23, 59, 59)
        }
        robot = RobotCreate._save_robot(data)
        self.assertEqual(Robot.objects.count(), 1)
        self.assertEqual(robot.serial, "X1-LT")
        self.assertEqual(robot.model, "X1")
        self.assertEqual(robot.version, "LT")
        self.assertEqual(robot.created.strftime('%Y-%m-%d %H:%M:%S'), "2022-12-31 23:59:59")

    def test_create_robot_missing_field(self):
        validated_data = {
            "model": "R2",
            "created": datetime(2022, 12, 31, 23, 59, 59)
        }
        with self.assertRaises(Exception):
            RobotCreate.create_robot(validated_data)
