from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Trial(models.Model):
    TYPE_CHOICES = (
        ('Class', 'Hold'),
        ('Fitness', 'Fitness'),
    )
    STATUS_CHOICES = (
        ('Pending', 'Afventer'),
        ('SignedUp', 'Tilmeldt'),
    ('DidNotSignup', 'Blev ikke meldt ind'),
    )
    name = models.CharField(max_length=200)
    trial_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date = models.DateField()
    time = models.TimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    reason = models.TextField(blank=True, null=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'trial_type': self.trial_type,
            'date': self.date.isoformat(),
            'time': self.time.strftime('%H:%M:%S') if self.time else None,
            'created_by': self.created_by.username if self.created_by else None,
            'status': self.status,
            'reason': self.reason,
        }

    def __str__(self):
        return f"{self.name} ({self.trial_type}) on {self.date}"


class CleaningRecord(models.Model):
    date = models.DateField(unique=True)
    arrived = models.TimeField(null=True, blank=True)
    left = models.TimeField(null=True, blank=True)

    def to_dict(self):
        return {
            'date': self.date.isoformat(),
            'arrived': self.arrived.strftime('%H:%M:%S') if self.arrived else None,
            'left': self.left.strftime('%H:%M:%S') if self.left else None,
        }

    def __str__(self):
        return f"Cleaning {self.date}"


class ShiftMessage(models.Model):
    date = models.DateField(unique=True)
    message = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        return {
            'date': self.date.isoformat(),
            'message': self.message,
            'author': self.author.username if self.author else None,
            'updated_at': self.updated_at.isoformat(),
        }


class ManagerMessage(models.Model):
    date = models.DateField(unique=True)
    message = models.TextField(blank=True)
    reply = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        return {
            'date': self.date.isoformat(),
            'message': self.message,
            'reply': self.reply,
            'author': self.author.username if self.author else None,
            'updated_at': self.updated_at.isoformat(),
        }
