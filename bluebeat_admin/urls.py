from django.urls import path
from .views import dashboard, applications, applicant_view, user_management, send_status_email_view, update_application_status

urlpatterns = [

    path('admin-dashboard/', dashboard, name="admin-dashboard"),
    path('applications/', applications, name="applications"),
    path('applicant-view/<int:application_id>/', applicant_view, name="applicant-view"),
    path('user-management/',user_management, name="user-management"),
    path('send_status_email/', send_status_email_view, name='send_status_email'),
    path('change_application_status/', update_application_status, name='change_application_status')
]

