from django.db import models
import uuid
    
class User(models.Model):
    CONFIRMATION_CHOICES = (
        ("User", "User"),
        ('ADMIN', 'ADMIN'),  
    )
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    user_id = models.CharField(max_length=200)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=50, choices=CONFIRMATION_CHOICES, default="User")
    is_identified = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name
    
    
    
