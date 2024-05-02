from django.db import models


class AuthKey(models.Model):
    key = models.UUIDField(auto_created=True)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
