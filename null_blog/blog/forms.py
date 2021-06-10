from django import forms
from django.forms import ModelForm
from django.core.validators import RegexValidator

from blog.models import Post, Comment

# regex for validating passwords
passwordRegex = RegexValidator(
    r'^(?=[^a-z]*[a-z])(?=\D*\d)[^:&.~\s]{5,20}$',
    'Password must contain at least one lowercase letter and at least one digit.'
    )

'''
 The following is a set of classes that define forms that the django template engine will interpret as HTML forms.
 Each attribute in these classes is an HTML form input of type specified by the widget argument
'''

class AuthForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'input'}), label=False, max_length=64)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'password'}), label=False, max_length=64, validators=[passwordRegex])

class PostForm(ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Title'}), label=False, max_length=64)
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'input', 'placeholder': 'Content'}), label=False, max_length=2048)
    image = forms.ImageField(label=False)

    class Meta:
        model = Post
        fields = ['title', 'content', 'image']


class CommentForm(forms.ModelForm):
    content = forms.CharField(max_length=256, widget=forms.Textarea(attrs={'class': 'input', 'placeholder': 'Leave a comment...'}), label=False)

    class Meta:
        model = Comment
        fields = ['content']
