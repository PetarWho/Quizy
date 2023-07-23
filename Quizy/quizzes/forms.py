from django import forms
from .models import Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image_url']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Adding custom classes to each field using a loop
        for field_name in self.fields:
            field = self.fields[field_name]
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'