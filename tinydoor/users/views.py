from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from watch.models import Score

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"

    def get(self, request, username):
        """
        Shows Profile information for one User.

        Parameters:
        request(HttpRequest): GET request sent to server
        username(str): the username of the User being shown

        Returns:
        HttpResponse: a view of the User and their information

        """
        # get the user
        user = self.model.objects.filter(username=username)
        # error handling
        if len(user) != 1:
            # correct user not found
            raise Http404("User was not found")
        else:
            # set the user to the User instance found
            user = user.first()
        # get associated scores
        scores = Score.objects.filter(user=user)
        # set the context
        context = {"object": user, "scores": scores, "user_id": user.id}
        return render(request, "users/user_detail.html", context)


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    fields = ["name"]

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return User.objects.get(username=self.request.user.username)

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.INFO, _("Infos successfully updated")
        )
        return super().form_valid(form)


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()
