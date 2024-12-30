from django.urls import path
from .import views

urlpatterns = [
    path('', views.contact_enquiry_view, name='contact'),
]