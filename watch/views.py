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
    """
    Calls pipeline with the task id passed by the url,
    then displays the results.
    """

    template_name = "pages/watched.html"

    def get(self, request, task_id):
        """
        Return a view of one specific Score model.

        Parameters:
        request(HttpRequest): the GET request object sent to the server
        task_id(str): the id of the Celery task that
                      is encapsulated by one of the
                      Score models. Each task id is
                      unique.

        Returns: HttpResponse of the WatchedView template.

        """
        # add the task id to the context
        context = {"task_id": task_id}
        # query for the Score model with this task_id
        score_queryset = Score.objects.filter(task_id=task_id)
        # if the QuerySet has something, add it to the context too
        if len(score_queryset) > 0:
            context["model"] = score_queryset.first()
        # send the response to the server
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """
        Instaniate a Score model based upon the video upload.

        Parameters:
        request(HttpRequest): the POST request object sent to the server

        Returns: JsonResponse: includes two fields to indicate whether
                 the valence score if finished beding calculated yet
                 or not. Is logged repeatedly to the console until the
                 "ready" field holds a True value. This score value is
                 then encapsulated in a new Score model instance.

        """
        if "task_id" in request.POST:
            task_identifier = request.POST["task_id"]
            async_res = start_watching.AsyncResult(task_identifier)
            # save Score if the results are ready
            if async_res.ready():
                # construct JSON we log on the console
                val_score = float(async_res.get("score")["score"])
                # get the user
                post_user = request.user  # set user object
                # make a new model instance
                score = Score.objects.create(
                    user=post_user if post_user.is_authenticated else None,
                    task_id=task_identifier,
                    emotion_score=val_score,
                )
                score.save()
                return JsonResponse({"ready": True, **async_res.get()})
            return JsonResponse({"ready": False})
