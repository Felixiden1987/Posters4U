from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Testimonial(models.Model):
    """
    A model representing a testimonial given by a user for a product.

    This model stores information about the testimonial left by a user,
    including the user, the product they are reviewing,
    the testimonial message, and the timestamp when
    the testimonial was created.

    Attributes:
        user : indicating who wrote the testimonial.
        product :indicating the product being reviewed.
        message : The content of the testimonial message.
        created_at : The timestamp when the testimonial was created.

    Methods:
        __str__ (str): Returns the username of the
        user who wrote the testimonial.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='testimonials'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='testimonials', default=1
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}"