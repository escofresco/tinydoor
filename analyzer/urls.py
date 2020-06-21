from django.urls import path
from django.views.generic import TemplateView

from .views import HomeView, ListenedView

urlpatterns = [
    # home page
    path("", HomeView.as_view(), name="home"),
    path("<str:task_id>/", ListenedView.as_view(), name="listened-view"),
    # about page
    path(
        "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    ),
]
