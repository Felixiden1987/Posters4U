from django.db import models
from django.utils.timezone import now


class ContactEnquiry(models.Model):
    """
    Model to store contact form submissions.
    """
    ENQUIRY_TYPE_CHIOCES = [
        ('general', 'General enquiry'),
        ('product', 'Product complaint'),
        ('order', 'Order Issue'),
        ('feedback', 'Feedback'),
        ('other', 'Other'),
    ]

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    enquiry_type = models.CharField(max_length=25,
                                    choices=ENQUIRY_TYPE_CHIOCES,
                                    default='general',
                                    verbose_name="Type of Enquiry")
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return (f"{self.get_enquiry_type_display()} - "
                f"{self.full_name}: {self.subject}")