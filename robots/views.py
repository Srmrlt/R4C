import json

from django.core.exceptions import ValidationError
from django.http import FileResponse, JsonResponse
from django.utils.timezone import now
from django.views import View

from robots.services import ProductionSummaryService, RobotCreate
from robots.validators import RobotDataValidator


class RobotCreateView(View):
    """
    A view to create new robots.
    This view handles POST requests with JSON data to add a new robot to the database.
    """
    @staticmethod
    def post(request):
        """
        Process POST requests to create a robot.
        It reads JSON data from the request, validates it, and creates a new robot.
        :return: JsonResponse: A message indicating success or error with a status code.
        """
        try:
            data = json.loads(request.body.decode('utf-8'))
            validated_data = RobotDataValidator.validate(data)
            robot = RobotCreate.create_robot(validated_data)

            return JsonResponse({
                "message": "Robot created successfully",
                "robot_id": robot.id
            }, status=201)

        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)


class ProductionSummaryView(View):
    """
    A view to generate and return the production summary Excel file.
    """
    @staticmethod
    def get():
        file = ProductionSummaryService.generate_production_summary_excel()
        filename = f"production_summary_{now().date()}.xlsx"
        return FileResponse(
            file,
            as_attachment=True,
            filename=filename,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
