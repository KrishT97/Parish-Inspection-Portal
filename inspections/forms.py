from django import forms
from .models import Parish, Inspection, GeneralComment


class ParishForm(forms.ModelForm):
    class Meta:
        model = Parish
        fields = ['image', 'name', 'description']

    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))


class InspectionForm(forms.ModelForm):
    # Adding comment_text to the form manually
    comment_text = forms.CharField(
        required=False,  # Allow this to be empty
        widget=forms.Textarea(attrs={'rows': 3}),
        label="General Comment"
    )
    YES_NO_DONT_KNOW = [
        ('yes', 'Yes'),
        ('no', 'No'),
        ('dont_know', "Don't Know")
    ]

    class Meta:
        model = Inspection
        fields = [
            'signage', 'general_surfaces_debris', 'general_surfaces_grids',
            'litter_bins_secure', 'litter_bins_empty', 'seating_stable',
            'swing_supports_secure', 'swing_caps_fitted', 'swing_unit_stable',
            'swing_seats_secure', 'swing_chains_wear', 'swing_surfacing_condition',
            'slide_secure', 'slide_clean', 'slide_surfacing_condition',
            'cableway_supports_secure', 'cableway_unit_stable', 'cableway_caps_present', 'cableway_suspension_chain',
            'cableway_traveller_smooth', 'cableway_take_off', 'cableway_surfacing_condition',
            'tunnel_damage_free', 'tunnel_clean', 'tunnel_palisade_stable',
            'tunnel_surfacing_condition', 'logs_secure', 'logs_free_of_decay',
            'logs_surfacing_condition', 'climber_logs_secure', 'climber_components_secure',
            'climber_unit_stable', 'climber_holds_present', 'climber_surfacing_condition'
        ]
        widgets = {
            field_name: forms.Select(choices=[('yes', 'Yes'), ('no', 'No'), ('dont_know', "Don't Know")])
            for field_name in fields
        }

    def __init__(self, *args, **kwargs):
        # Allow passing the existing comment when editing
        if 'instance' in kwargs and kwargs['instance']:
            # Set initial comment_text from the existing GeneralComment (if any)
            inspection_instance = kwargs['instance']
            general_comment = GeneralComment.objects.filter(inspection=inspection_instance).first()
            kwargs['initial'] = kwargs.get('initial', {})
            kwargs['initial']['comment_text'] = general_comment.comment_text if general_comment else ""
        super().__init__(*args, **kwargs)
