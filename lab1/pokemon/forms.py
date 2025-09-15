from django import forms
from .models import Pokemon
import os

class PokemonForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True
    class Meta:
        model = Pokemon
        fields = ["name", "type", "level", "hp", "note", "image"]
        widgets = {
            "level": forms.NumberInput(),
            "hp": forms.NumberInput(),
        }



    def clean_name(self):
        value = self.cleaned_data.get("name", "").strip()
        if len(value) < 3:
            raise forms.ValidationError("Name must be at least 3 characters long.")
        return value

    def clean_level(self):
        value = self.cleaned_data.get("level")
        if not (1 <= value <= 100):
            raise forms.ValidationError("Level must be between 1 and 100.")
        return value

    def clean_hp(self):
        value = self.cleaned_data.get("hp")
        if not (1 <= value <= 999):
            raise forms.ValidationError("HP must be between 1 and 999.")
        return value

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image:
            ext = os.path.splitext(image.name)[1].lower()
            if ext not in [".jpg", ".jpeg"]:
                raise forms.ValidationError("Only JPG files are allowed.")
        return image