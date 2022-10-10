from django import forms
from .models import Movie, Comment


class MovieForm(forms.ModelForm):

    class Meta:
        model = Movie
        fields = ['title', 'movie_image', 'summary', 'nation', 'genre', 'release_date']


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        exclude = ['user']