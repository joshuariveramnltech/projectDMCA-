from django.urls import path
from . import views

app_name = 'admission'

urlpatterns = [
    path('', views.home, name='home'),
    path('admission/dmca/appointment-request/',
         views.appointment_request, name='appointment_request'),
    path('admission/appointment-request/<int:appointment_request_id>/<slug:appointment_request_slug>/pdf/',
         views.appointment_request_pdf, name='appointment_request_pdf'),
    path('admission/appointment-request/<int:appointment_request_id>/<slug:appointment_request_slug>/success/',
         views.appointment_request_success, name='appointment_request_success'),
    path('admission/cancel/<int:appointment_request_id>/appointment-request/',
         views.cancel_appointment_request, name='cancel_appointment_request'),
]
