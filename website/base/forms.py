from django import forms
from .models import Entry

class CommentUpdateForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['comments']