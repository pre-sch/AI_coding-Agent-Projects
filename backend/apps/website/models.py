from django.db import models


class Testimonial(models.Model):
    author = models.CharField(max_length=120)
    quote = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
