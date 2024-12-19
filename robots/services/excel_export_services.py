from io import BytesIO

import openpyxl
from django.db import models
from django.utils.timezone import now, timedelta
from openpyxl.styles import Font

from robots.models import Robot


class ProductionData:
    """
    Data preparation for the production summary.
    """

    @classmethod
    def get_data_for_period(cls, start_date, end_date):
        """
        Production data for a given period grouped by model and version.
        """
        print(end_date)
        print(start_date)
        return (
            Robot.objects.filter(created__range=(start_date, end_date))
            .values("model", "version")
            .annotate(count=models.Count("id"))
            .order_by("model", "version")
        )

    @classmethod
    def get_last_week_data(cls):
        end_date = now()
        start_date = end_date - timedelta(days=7)
        return cls.get_data_for_period(start_date, end_date)


class ExcelGenerator:
    def __init__(self, data):
        self.data = data

    def generate(self):
        """
        Generate an Excel file with the production summary.
        """
        workbook = openpyxl.Workbook()
        workbook.remove(workbook.active)  # Remove default sheet

        prepared_data = self._prepare_data_for_excel()

        for model, entries in prepared_data.items():
            sheet = workbook.create_sheet(title=f"Model {model}")
            sheet.append(["Модель", "Версия", "Количество за неделю"])
            for cell in sheet[1]:
                cell.font = Font(bold=True)

            for entry in entries:
                sheet.append([model, entry["version"], entry["count"]])

        file = BytesIO()
        workbook.save(file)
        file.seek(0)
        return file

    def _prepare_data_for_excel(self):
        """
        Groups data by model for organization in the file.
        """
        prepared_data = {}
        for entry in self.data:
            model = entry["model"]
            if model not in prepared_data:
                prepared_data[model] = []
            prepared_data[model].append({"version": entry["version"], "count": entry["count"]})
        return prepared_data


class ProductionSummaryService:
    """
    Combines data preparation and Excel generation for the production summary.
    """
    @staticmethod
    def generate_production_summary_excel():
        data = ProductionData.get_last_week_data()
        return ExcelGenerator(data).generate()
