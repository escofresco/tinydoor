from django.shortcuts import render
from .forms import EmptyForm
from django.views.generic import TemplateView
from django.http import JsonResponse
from .tasks import start_watching

# Create your views here.
class HomeView(TemplateView):
    template_name = "pages/home.html"
    form_class = EmptyForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["room_name"] = "test"
        return context

    def post(self, request, *args, **kwargs):
        if "file_url" in request.POST:
            # start a worker task for processing file located at file_url
            res = start_watching.apply_async(
                (request.POST["file_url"],), time_limit=60 * 20, soft_time_limit=60 * 15
            )
            return JsonResponse({"task_id": res.id})
