from django.urls import path
from system_management import views


urlpatterns = [

    path("register-user/", views.register_user, name="register-user"),
    path("deactivate-user/", views.deactivate_user, name="deactivate-user"),
    path("get_user_details/<int:user_id>/", views.get_user_details, name='get_user_details'),
    path("sign-out", views.sign_out, name='sign-out'),
]

