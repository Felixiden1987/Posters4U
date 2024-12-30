from django.urls import path
from .import views


urlpatterns = [
    path('testimonials/', views.testimonials_view, name='testimonials'),
    path('testimonials/add/',views.add_testimonials_view, name='add_testimonials'),
   
]