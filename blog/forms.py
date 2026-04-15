from typing import Any
from django import forms

from .models import Commentary


class CommentaryForm(forms.ModelForm):
    class Meta:
        model = Commentary
        fields = ("content",)

    def clean_content(self) -> str:
        content: str = self.cleaned_data["content"]
        if not content.strip():
            raise forms.ValidationError("Content cannot be empty")
        return content
