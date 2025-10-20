import hashlib
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Custom user model with role-based access."""
    ROLE_CHOICES = [
        ('simple', 'Simple'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='simple')

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class HunterIP(models.Model):
    """Class for storing hashed IP addresses reported by users."""
    ip_hash = models.CharField(max_length=64, unique=True, null=False)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_ips')
    
    def set_ip(self, ip_address):
        self.ip_hash = hashlib.sha256(ip_address.encode()).hexdigest()

    def check_ip(self, ip_address):
        return self.ip_hash == hashlib.sha256(ip_address.encode()).hexdigest()

    def __str__(self):
        return f"IP reported by {self.added_by.username}"
