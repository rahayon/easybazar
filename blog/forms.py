from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    name = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control my-3', 'placeholder':'Your Name'}))
    body = forms.CharField(label='',widget=forms.Textarea(attrs={'class':'form-control my-3', 'rows':4, 'placeholder':'Your comment here...'}))
    email = forms.EmailField(label='',widget=forms.EmailInput(attrs={'class': 'form-control my-3', 'placeholder':'Your Email'}))
    
    class Meta:
        model = Comment
        fields = ('name','email','body')