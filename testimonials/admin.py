from django.contrib import admin
from .models import Testimonial

class TestimonialAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'message',
        'created_at'
    )


admin.site.register(Testimonial, TestimonialAdmin)
