from robots.models import Robot


class RobotCreate:
    """
    Business logic for creating a robot.
    """
    @classmethod
    def create_robot(cls, validated_data: dict) -> Robot:
        """
        Generate serial and creates a record in the database.
        :param validated_data: A dictionary with valid robot data.
        :return: Created Robot object.
        """
        generated_data = cls._generate_serial(validated_data)
        return cls._save_robot(generated_data)

    @classmethod
    def _generate_serial(cls, data: dict) -> dict:
        data["serial"] = f'{data["model"]}-{data["version"]}'
        return data

    @classmethod
    def _save_robot(cls, data: dict) -> Robot:
        return Robot.objects.create(**data)
