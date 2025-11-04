"""Module for defining Django models related to user management and IP/password handling"""
import hashlib
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Custom user model with role-based access."""
    ROLE_CHOICES = [
        ('simple', 'Simple'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('architect', 'Architect'),
        ('inquisition', 'Inquisition')
    ]
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='simple')
    force_password_change = models.BooleanField(default=False)
    def __str__(self):
        """Return a string representation of the User model"""
        return f"{self.username} ({self.get_role_display()})"

class UserLoginIP(models.Model):
    """Class for storing user login IP addresses."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_ips')
    ip_hash = models.CharField(max_length=64, null=False)
    def set_ip(self, ip_address):
        """Hash and store an IP address using SHA-256"""
        self.ip_hash = hashlib.sha256(ip_address.encode()).hexdigest()

    def check_ip(self, ip_address):
        """Check if a provided IP address matches the stored hash"""
        return self.ip_hash == hashlib.sha256(ip_address.encode()).hexdigest()

    def __str__(self):
        return f"{self.user.username} — {self.ip_address}"

class Government(models.Model):
    """Class for storing hashed IP addresses reported by users."""
    ip_hash = models.CharField(max_length=64, unique=True, null=False)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_ips', null=True, blank=True)

    def set_ip(self, ip_address):
        """Hash and store an IP address using SHA-256"""
        self.ip_hash = hashlib.sha256(ip_address.encode()).hexdigest()

    def check_ip(self, ip_address):
        """Check if a provided IP address matches the stored hash"""
        return self.ip_hash == hashlib.sha256(ip_address.encode()).hexdigest()

    def __str__(self):
        """Return a string representation of the Government model"""
        return f"IP reported by {self.added_by.username}"

class EntryPassword(models.Model):
    """Class for entry password."""
    password_hash = models.CharField(max_length=128, null=False)

    def set_password(self, raw_password):
        """Hash and store a password using SHA-256"""
        self.password_hash = hashlib.sha256(raw_password.encode()).hexdigest()

    def check_password(self, raw_password):
        """Check if a provided password matches the stored hash"""
        return self.password_hash == hashlib.sha256(raw_password.encode()).hexdigest()

    def __str__(self):
        """Return a string representation of the EntryPassword model"""
        return "Entry password to get access to application"
