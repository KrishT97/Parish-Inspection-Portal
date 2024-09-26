from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Parish(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(default="")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Inspection(models.Model):
    CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
        ('dont_know', "Don't Know")
    ]

    parish = models.ForeignKey(Parish, on_delete=models.CASCADE, related_name="inspections")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    # Questions for Inspection
    signage = models.CharField(max_length=10, choices=CHOICES, default='dont_know')
    general_surfaces_debris = models.CharField(max_length=10, choices=CHOICES, default='dont_know')
    general_surfaces_grids = models.CharField(max_length=10, choices=CHOICES, default='dont_know')
    litter_bins_secure = models.CharField(max_length=10, choices=CHOICES, default='dont_know')
    litter_bins_empty = models.CharField(max_length=10, choices=CHOICES, default='dont_know')
    seating_stable = models.CharField(max_length=10, choices=CHOICES, default='dont_know')
    swing_supports_secure = models.CharField(max_length=10, choices=CHOICES, default='dont_know')
    swing_caps_fitted = models.CharField(max_length=10, choices=CHOICES, default='dont_know')
    swing_unit_stable = models.CharField(max_length=10, choices=CHOICES, default='dont_know')
    swing_seats_secure = models.CharField(max_length=10, choices=CHOICES, default='dont_know')
    swing_chains_wear = models.CharField(max_length=10, choices=CHOICES, default='dont_know')
    swing_surfacing_condition = models.CharField(max_length=10, choices=CHOICES, default='dont_know')
    slide_secure = models.CharField(max_length=10, choices=CHOICES, default='dont_know')
    slide_clean = models.CharField(max_length=10, choices=CHOICES, default='dont_know')
    slide_surfacing_condition = models.CharField(max_length=10, choices=CHOICES, default='dont_know')
    cableway_supports_secure = models.CharField(max_length=10, choices=CHOICES, default='dont_know')
    cableway_unit_stable = models.CharField(max_length=10, choices=CHOICES, default='dont_know')
    cableway_caps_present = models.CharField(max_length=10, choices=CHOICES, default='dont_know')
    cableway_suspension_chain = models.CharField(max_length=10, choices=CHOICES, default='dont_know')
    cableway_traveller_smooth = models.CharField(max_length=10, choices=CHOICES, default='dont_know')
    cableway_take_off = models.CharField(max_length=10, choices=CHOICES, default='dont_know')
    cableway_surfacing_condition = models.CharField(max_length=10, choices=CHOICES, default='dont_know')
    tunnel_damage_free = models.CharField(max_length=10, choices=CHOICES, default='dont_know')
    tunnel_clean = models.CharField(max_length=10, choices=CHOICES, default='dont_know')
    tunnel_palisade_stable = models.CharField(max_length=10, choices=CHOICES, default='dont_know')
    tunnel_surfacing_condition = models.CharField(max_length=10, choices=CHOICES, default='dont_know')
    logs_secure = models.CharField(max_length=10, choices=CHOICES, default='dont_know')
    logs_free_of_decay = models.CharField(max_length=10, choices=CHOICES, default='dont_know')
    logs_surfacing_condition = models.CharField(max_length=10, choices=CHOICES, default='dont_know')
    climber_logs_secure = models.CharField(max_length=10, choices=CHOICES, default='dont_know')
    climber_components_secure = models.CharField(max_length=10, choices=CHOICES, default='dont_know')
    climber_unit_stable = models.CharField(max_length=10, choices=CHOICES, default='dont_know')
    climber_holds_present = models.CharField(max_length=10, choices=CHOICES, default='dont_know')
    climber_surfacing_condition = models.CharField(max_length=10, choices=CHOICES, default='dont_know')

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
            ('dont_know', "Don't Know")
        ]
    )

    def __str__(self):
        return self.question_text


class GeneralComment(models.Model):
    inspection = models.OneToOneField(Inspection, on_delete=models.CASCADE)
    comment_text = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Comment for {self.inspection.parish.name}"
