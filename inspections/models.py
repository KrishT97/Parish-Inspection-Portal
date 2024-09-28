from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
from django.conf import settings
import os


class Parish(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(default="")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='profile_pics/', default='default.jpg')

    def __str__(self):
        return self.name

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.height > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Inspection(models.Model):
    CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
        ('other', "Other")
    ]
    parish = models.ForeignKey(Parish, on_delete=models.CASCADE, related_name="inspections")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    # Question topics for Inspection
    signage = models.CharField(max_length=10, choices=CHOICES, default='other')
    general_surfaces_debris = models.CharField(max_length=10, choices=CHOICES, default='other')
    general_surfaces_grids = models.CharField(max_length=10, choices=CHOICES, default='other')
    litter_bins_secure = models.CharField(max_length=10, choices=CHOICES, default='other')
    litter_bins_empty = models.CharField(max_length=10, choices=CHOICES, default='other')
    seating_stable = models.CharField(max_length=10, choices=CHOICES, default='other')
    swing_supports_secure = models.CharField(max_length=10, choices=CHOICES, default='other')
    swing_caps_fitted = models.CharField(max_length=10, choices=CHOICES, default='other')
    swing_unit_stable = models.CharField(max_length=10, choices=CHOICES, default='other')
    swing_seats_secure = models.CharField(max_length=10, choices=CHOICES, default='other')
    swing_chains_wear = models.CharField(max_length=10, choices=CHOICES, default='other')
    swing_surfacing_condition = models.CharField(max_length=10, choices=CHOICES, default='other')
    slide_secure = models.CharField(max_length=10, choices=CHOICES, default='other')
    slide_clean = models.CharField(max_length=10, choices=CHOICES, default='other')
    slide_surfacing_condition = models.CharField(max_length=10, choices=CHOICES, default='other')
    cableway_supports_secure = models.CharField(max_length=10, choices=CHOICES, default='other')
    cableway_unit_stable = models.CharField(max_length=10, choices=CHOICES, default='other')
    cableway_caps_present = models.CharField(max_length=10, choices=CHOICES, default='other')
    cableway_suspension_chain = models.CharField(max_length=10, choices=CHOICES, default='other')
    cableway_traveller_smooth = models.CharField(max_length=10, choices=CHOICES, default='other')
    cableway_take_off = models.CharField(max_length=10, choices=CHOICES, default='other')
    cableway_surfacing_condition = models.CharField(max_length=10, choices=CHOICES, default='other')
    tunnel_damage_free = models.CharField(max_length=10, choices=CHOICES, default='other')
    tunnel_clean = models.CharField(max_length=10, choices=CHOICES, default='other')
    tunnel_palisade_stable = models.CharField(max_length=10, choices=CHOICES, default='other')
    tunnel_surfacing_condition = models.CharField(max_length=10, choices=CHOICES, default='other')
    logs_secure = models.CharField(max_length=10, choices=CHOICES, default='other')
    logs_free_of_decay = models.CharField(max_length=10, choices=CHOICES, default='other')
    logs_surfacing_condition = models.CharField(max_length=10, choices=CHOICES, default='other')
    climber_logs_secure = models.CharField(max_length=10, choices=CHOICES, default='other')
    climber_components_secure = models.CharField(max_length=10, choices=CHOICES, default='other')
    climber_unit_stable = models.CharField(max_length=10, choices=CHOICES, default='other')
    climber_holds_present = models.CharField(max_length=10, choices=CHOICES, default='other')
    climber_surfacing_condition = models.CharField(max_length=10, choices=CHOICES, default='other')

    def __str__(self):
        return f"Inspection for {self.parish.name} on {self.created_at}"


class Question(models.Model):
    inspection = models.ForeignKey(Inspection, on_delete=models.CASCADE)
    question_text = models.TextField()
    response = models.CharField(
        max_length=20,
        choices=[
            ('yes', 'Yes'),
            ('no', 'No'),
            ('other', "Other")
        ]
    )

    def __str__(self):
        return self.question_text


class GeneralComment(models.Model):
    inspection = models.OneToOneField(Inspection, on_delete=models.CASCADE)
    comment_text = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Comment for {self.inspection.parish.name}"
