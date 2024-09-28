from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Inspection, Question

@receiver(post_save, sender=Inspection)
def create_default_questions(sender, instance, created, **kwargs):
    if created:
        default_questions = [
            "Signage: Is signage present, stable, legible and with no protruding bolts?",
            "General Surfaces: Are they free from debris, erosion, litter, weeds, slippery algae, etc.?",
            "General Surfaces: Are any ground grids present and secure?",
            "Litter Bins: Are they secure with liners present?",
            "Litter Bins: Are they empty or not in need of emptying?",
            "Seating – Various: Are the seats secured to the ground, stable, clean, undamaged, and showing no obvious signs of timber decay or corrosion/decay?",
            "Swing – Mixed – 2 Bay 4 Seat- Wicksteed: Are the supports and cross bar secure, undamaged, and free from any obvious signs of corrosion?",
            "Swing – Mixed – 2 Bay 4 Seat- Wicksteed: Are all caps fitted?",
            "Swing – Mixed – 2 Bay 4 Seat- Wicksteed: Is the unit stable?",
            "Swing – Mixed – 2 Bay 4 Seat- Wicksteed: Are the swing seats free from damage and secure?",
            "Swing – Mixed – 2 Bay 4 Seat- Wicksteed: Are the chains and shackles showing no signs of excessive wear and working freely?",
            "Swing – Mixed – 2 Bay 4 Seat- Wicksteed: Is the surfacing undamaged and in a good condition without erosion/puddling?",
            "Slide – Embankment: Is the starting section secure, stable and free from damage?",
            "Slide – Embankment: Is the slide-chute in a good condition, clean and free from any foreign objects and with no sharp edges?",
            "Slide – Embankment: Is the surfacing undamaged and in a good condition?",
            "(Cableway) Are all the supports, barriers secure and undamaged with no signs of obvious corrosion/decay present?",
            "(Cableway) Is the unit stable?",
            "(Cableway) Are all component parts present including caps?",
            "(Cableway) Are the cable, seat, and suspension chain present, secure and free from damage?",
            "(Cableway) Does the traveller run smoothly with no undue noise?",
            "(Cableway) Are the take-off and landing areas undamaged?",
            "(Cableway) Is the surfacing undamaged and free from trips?",
            "(Agility Tunnel Mound -Large) Are the tunnel ends free from damage?",
            "(Agility Tunnel Mound -Large) Is the tunnel clean and undamaged?",
            "(Agility Tunnel Mound -Large) Are the palisade logs, steps, ladder and barriers in a good stable condition with no obvious signs of decay?",
            "(Agility Tunnel Mound -Large) Is the surfacing in good order?",
            "(Natural Play – Logs) Are the logs secure, free from damage and any obvious signs of decay?",
            "(Natural Play – Logs) Is the unit free from slippery algae?",
            "(Natural Play – Logs) Is the surfacing undamaged and in a good condition with no erosion and puddling?",
            "(Climber - Logs) Are all supports stable, secure and free from damage and any obvious signs of decay?",
            "(Climber - Logs) Are all component parts present and secure including caps and holds?",
            "(Climber - Logs) Is the unit stable and free from slippery algae?",
            "(Climber - Logs) Are the climbing holds present, secure and non-rotating?",
            "(Climber - Logs) Is the surfacing undamaged and free from trips?"
        ]
        for question_text in default_questions:
            Question.objects.create(
                inspection=instance,
                question_text=question_text,
                response="dont_know"
            )
