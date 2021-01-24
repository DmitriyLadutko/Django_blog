from .models import Article, Comment, Profile
from django.forms.widgets import DateInput

from django.forms import ModelForm, TextInput, Textarea


class ArticleForms(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'body', 'category']
        widgets = {'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'input title'}),
                   'body': Textarea(attrs={'class': 'form-control', 'placeholder': 'input text post'})}


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text_comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields['text_comment'].widget = Textarea(attrs={"rows": 3})


class EditProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'date_of_birth', 'country', 'gender', 'bio']
        widgets = {'bio': Textarea(attrs={'class': 'form-control', 'placeholder': 'input your short description'}),
                   'date_of_birth': DateInput(attrs={'type': 'date'})}
