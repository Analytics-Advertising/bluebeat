from django.urls import path
from dealer import views

urlpatterns = [
    
    path('create-application/', views.submit_application, name="create-application"),
    path('dealer-dashboard/',views.dashboard, name="dealer-dashboard"),
    path('commercials/',views.commercials, name="commercials"),
    path('choose-schedule/', views.choose_schedule, name="choose-schedule"),
    path('agreements/',views.agreements, name="agreements"),
    path('contract/', views.view_contract, name="contract"),
    path('choose-contract/', views.choose_contract, name="choose-contract"),
    path('acknowledgment/', views.acknowledgment_section, name="acknowledgment"),
    path('acknowledgment/state/', views.acknowledgment_state, name='acknowledgment_state'),
    path('verification-documents', views.verification_documents, name='verification-documents'),
    path('upload-documents/', views.upload_documents, name='upload-documents'),
    path('get-documents/', views.get_documents, name="get-documents"),
    # path('sign-contract-online/', sign_contract_online, name='sign-contract-online'),


]

