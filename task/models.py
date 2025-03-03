from django.db import models
from account.models import User,BaseModel
from django.utils.timezone import now
# Create your models here.

class Actions(BaseModel):
    STATUS_CHOICES = [
        ('assigned', 'Assigned'),
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE,related_name="assigned_tasks")
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name="created_tasks")
    assigned_date = models.DateField(default=now)  # Set default to today's date
    due_date = models.DateField()
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='assigned')
    heading = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.heading} - {self.status}"