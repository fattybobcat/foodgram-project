from django.forms import ModelForm
from django.forms.widgets import CheckboxSelectMultiple

from .models import Recipe

class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ["title", "description", "time", "image"]# "tag",

      #  widgets = {
      #      "tag": CheckboxSelectMultiple(),
      #  }

