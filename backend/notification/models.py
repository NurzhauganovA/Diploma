from django.db import models
from authorization.models import User


class Notification(models.Model):
    from_who = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_who')
    to_who = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_who')
    title = models.CharField(max_length=255)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        db_table = 'notifications'
