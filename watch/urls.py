from django.urls import path
from django.views.generic import TemplateView

from .views import HomeView, WatchedView

urlpatterns = [
    # home page
    path("", HomeView.as_view(), name="home"),
    path("viewing/<str:task_id>/", WatchedView.as_view(), name="watched-view"),
    # about page
    path(
        "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    ),
]
