from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo', 'title', 'bio', 'location', 'email', 'phone', 'github', 'linkedin', 'twitter', 'website']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'photo': forms.FileInput(attrs={'accept': 'image/*'}),
        }
