from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from .forms import EmptyForm
from .models import Score
from .tasks import start_watching


class HomeView(TemplateView):
    template_name = "pages/home.html"
    form_class = EmptyForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        if "file_url" in request.POST:
            # start a worker task for processing file located at file_url
            res = start_watching.apply_async(
                (request.POST["file_url"],), time_limit=60 * 20, soft_time_limit=60 * 15
            )
            return JsonResponse({"task_id": res.id})


class WatchedView(TemplateView):
    """Calls pipeline with the task id passed by the url, then displays the
    results."""

    template_name = "pages/watched.html"

    def get(self, request, task_id):
        # get the Score model with this task_id
        score = Score.objects.filter(task_id=task_id).first()
        context = {"model": score, "task_id": task_id}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if "task_id" in request.POST:
            task_identifier = request.POST["task_id"]
            async_res = start_watching.AsyncResult(task_identifier)
            # save initial Score model
            post_user = request.user  # set user object
            score = Score.objects.create(
                user=post_user if post_user.is_authenticated else None,
                task_id=task_identifier,
                emotion_score=None,
            )
            score.save()
            if async_res.ready():
                # construct JSON we log on the console
                val_score = float(async_res.get("score")["score"])
                # now we're ready to add score to the model created before
                update_score = Score.objects.get(task_id=task_identifier)
                update_score.emotion_score = val_score
                update_score.save()
                return JsonResponse({"ready": True, **async_res.get()})
            return JsonResponse({"ready": False})
