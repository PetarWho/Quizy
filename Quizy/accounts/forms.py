from django import forms
from .models import AppUser


class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(label="Username")
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput
    )

    class Meta:
        model = AppUser
        fields = ['username', 'first_name', 'last_name', 'age', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Adding custom classes to each field using a loop
        for field_name in self.fields:
            field = self.fields[field_name]
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
