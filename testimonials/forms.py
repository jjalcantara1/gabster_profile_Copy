# forms.py
from django import forms

from accounts.models import UserAccount
from .models import Testimonial


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['content']

    user_to = forms.ModelChoiceField(
        queryset=UserAccount.objects.all(),
        widget=forms.HiddenInput(),  # Use a hidden input field
        required=False  # Make the field non-required
    )

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content')

        if not content:
            raise forms.ValidationError('Testimonial content is required.')
