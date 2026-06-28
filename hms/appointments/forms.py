from django import forms
from .models import AvailabilitySlot


class AvailabilitySlotForm(forms.ModelForm):

    class Meta:
        model = AvailabilitySlot
        fields = ['date', 'start_time', 'end_time']

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }