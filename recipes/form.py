from django import forms
from .models import Recipe, Tags

TAGS = (("breakfast", ("Завтрак", "orange")),
               ("lunch", ("Обед", "green")),
               ("dinner", ("Ужин", "purple")))

class RecipeForm(forms.ModelForm):
    #tags = ModelMultipleChoiceField(queryset=Tag.objects.all())
   # tags = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=TAGS)
   #p4_rasters = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=MP4_CHOICES)
    class Meta:
        model = Recipe
        fields = ["title", "tags", "time", "description", "image"]

        widgets = {
           "tags": forms.CheckboxSelectMultiple(),
        }

