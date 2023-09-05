from django import forms
from .models import Review, Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = '__all__'


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = '__all__'
