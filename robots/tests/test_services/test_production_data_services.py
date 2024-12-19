from datetime import datetime
from unittest.mock import patch

from django.test import TestCase

from robots.services.excel_export_services import ProductionData


class ProductionDataTests(TestCase):
    fixtures = ['robots_fixtures.json']

    def test_get_data_for_period(self):
        start_date = datetime(2024, 12, 5, 23, 59, 59)
        end_date = datetime(2024, 12, 12, 23, 59, 59)
        data = ProductionData.get_data_for_period(start_date, end_date)
        self.assertEqual(len(data), 8)
        self.assertEqual(data[0]["model"], "RM")
        self.assertEqual(data[0]["version"], "01")
        self.assertEqual(data[0]["count"], 2)

    @patch('robots.services.excel_export_services.now')
    def test_get_last_week_data(self, mock_now):
        mock_now.return_value = datetime(2024, 12, 19, 23, 59, 59)
        data = ProductionData.get_last_week_data()
        self.assertEqual(len(data), 11)
        self.assertEqual(data[0]["model"], "RM")
        self.assertEqual(data[0]["version"], "01")
        self.assertEqual(data[0]["count"], 2)
