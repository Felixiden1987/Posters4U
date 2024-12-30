from django.contrib import admin
from .models import ContactEnquiry


class ContactEnquiryAdmin(admin.ModelAdmin):
    """ Display list in admin page for contact us page"""

    list_display = ('full_name',
                    'email',
                    'subject',
                    'created_at')

    list_filter = ('created_at',)


admin.site.register(ContactEnquiry, ContactEnquiryAdmin)