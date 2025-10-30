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


class CleaningTask(models.Model):
    """A reusable cleaning task template for a weekday.

    weekday: 0=Monday .. 6=Sunday
    time: textual time (e.g., '06:45')
    area: area string
    title: short task title
    details: longer description
    status: one of Pending/Done/NotUsed/NotDone
    """
    STATUS_CHOICES = (
        ('Pending', 'Afventer'),
        ('Done', 'Udført'),
        ('NotUsed', 'Ikke i brug'),
        ('NotDone', 'Ikke udført'),
    )

    weekday = models.IntegerField(help_text='0=Monday .. 6=Sunday')
    time = models.CharField(max_length=16, blank=True)
    area = models.CharField(max_length=200, blank=True)
    title = models.CharField(max_length=200, blank=True)
    details = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def to_dict(self):
        return {
            'id': self.id,
            'weekday': self.weekday,
            'time': self.time,
            'area': self.area,
            'title': self.title,
            'details': self.details,
            'status': self.status,
        }

    def __str__(self):
        return f"[{self.get_weekday_display() if hasattr(self,'get_weekday_display') else self.weekday}] {self.title} ({self.time})"


class PTLead(models.Model):
    """Persistent PT lead collected by receptionists.

    Fields mirror the UI: name, note, phone, email, receptionist (FK), contacted_at.
    """
    name = models.CharField(max_length=255, blank=True)
    note = models.TextField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=254, blank=True)
    receptionist = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='pt_leads')
    contacted_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_pt_leads')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'note': self.note,
            'phone': self.phone,
            'email': self.email,
            'receptionist': self.receptionist.username if self.receptionist else None,
            'receptionist_id': self.receptionist.id if self.receptionist else None,
            'contacted_at': self.contacted_at.isoformat() if self.contacted_at else None,
            'created_by': self.created_by.username if self.created_by else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    def __str__(self):
        return f"PTLead {self.id}: {self.name or '(no name)'}"
