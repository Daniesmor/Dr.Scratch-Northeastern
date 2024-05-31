from django.urls import path
from .views import handle_request

urlpatterns = [
    path('handle-request/<str:project_id>/', handle_request, name='handle_request'),
]