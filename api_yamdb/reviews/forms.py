from django import forms
from .models import Title, Category, Genre


class TitleForm(forms.ModelForm):

    class Meta:
        model = Title
        fields = '__all__'


class GenreForm(forms.ModelForm):

    class Meta:
        model = Genre
        fields = '__all__'


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = '__all__'
