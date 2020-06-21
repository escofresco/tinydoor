from django.urls import path

from tinydoor.users.views import (
<<<<<<< HEAD
    user_redirect_view,
    user_update_view,
    user_detail_view,
=======
    user_detail_view,
    user_redirect_view,
    user_update_view,
>>>>>>> dd4fd56341cdf9156f4b0a7016225b2ebdc82048
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]
