from django.shortcuts import render
from .forms import EmptyForm, AnalysisForm
from django.views.generic import TemplateView
from django.http import JsonResponse
from .tasks import start_watching
from django.views.generic.edit import CreateView
from .models import Analysis

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


class AnalysisCreate(CreateView):
    '''Submit a form to create new Analysis.'''
    model = Analysis
    form_class = AnalysisForm
    template_name = "analyzer/create.html"

    def form_valid(self, form):
        '''Initializes image field (if there is one of new Analysis.'''
        form.instance.image = self.request.FILES.get('image')
        return super().form_valid(form)
