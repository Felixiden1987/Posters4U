from django.urls import path
from .import views


urlpatterns = [
    path('', views.testimonials_view, name='testimonials'),
    path('testimonials/add/',views.add_testimonials_view, name='add_testimonials'),
    path('testimonials/edit/<int:testimonial_id>',views.edit_testimonials_view, name='edit_testimonials'),
]