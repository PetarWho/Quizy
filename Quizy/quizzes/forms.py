from django import forms
from .models import Category, Question, Quiz


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image_url']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            field = self.fields[field_name]
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['category', 'question_text', 'option1', 'option2', 'option3', 'option4', 'correct_answer']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            field = self.fields[field_name]
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['category', 'image_url', 'name']

    def __init__(self, *args, **kwargs):
        categories = kwargs.pop('categories')
        super().__init__(*args, **kwargs)
        self.fields['category'].choices = [(category.pk, category.name) for category in categories]

        # Add a multiple-choice field for selecting questions based on the category
        questions = Question.objects.filter(category__in=categories)
        self.fields['questions'] = forms.ModelMultipleChoiceField(
            queryset=questions,
            widget=forms.SelectMultiple,  # Changed from CheckboxSelectMultiple to SelectMultiple
            label="Select Questions"
        )

        for field_name in self.fields:
            field = self.fields[field_name]
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'
