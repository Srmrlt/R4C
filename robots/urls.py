from django.urls import path

from robots.views import RobotCreateView

urlpatterns = [
    path('robots/', RobotCreateView.as_view(), name='robots')
]
