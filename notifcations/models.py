# notifications/models.py
from django.db import models
from members.models import User
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    type = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    extra_data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return str(self.user) + " | " +str(self.message)