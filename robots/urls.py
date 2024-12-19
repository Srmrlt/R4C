from django.urls import path

from robots.views import ProductionSummaryView, RobotCreateView

urlpatterns = [
    path('robots/', RobotCreateView.as_view(), name='robots'),
    path('production-summary/', ProductionSummaryView.as_view(), name='production-summary')
]
