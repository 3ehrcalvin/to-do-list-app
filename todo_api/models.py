from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Todo(models.Model):
    note = models.CharField(max_length=255)
    due_date = models.DateField()
    is_complete = models.BooleanField()
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.note
