from django.urls import path
from .import views
from .views import reset_shopping_bag_flag


urlpatterns = [
    path('', views.testimonials_view, name='testimonials'),
    path('testimonials/add/',views.add_testimonials_view, name='add_testimonials'),
    path('testimonials/edit/<int:testimonial_id>',views.edit_testimonials_view, name='edit_testimonials'),
    path('testimonials/delete/<int:testimonial_id>',views.delete_testimonials_view, name='delete_testimonials'),
    path('reset-shopping-bag-flag/',reset_shopping_bag_flag, name='reset_shopping_bag_flag'),
]