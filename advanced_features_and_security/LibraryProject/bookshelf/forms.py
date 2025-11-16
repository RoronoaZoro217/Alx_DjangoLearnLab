from django import forms
from .models import Book

class ExampleForm(forms.ModelForm):
    """
    Example form for creating or updating Book entries.
    Uses Django ModelForm for validation and automatic input sanitization.
    """

    class Meta:
        model = Book
        fields = ['title', 'author']

    def clean_title(self):
        """
        Validate the title field to prevent invalid input or XSS.
        """
        title = self.cleaned_data.get('title')
        if "<script>" in title.lower():  # basic XSS check
            raise forms.ValidationError("Invalid characters in title.")
        return title
