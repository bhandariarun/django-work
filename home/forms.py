from django import forms

class UploadForm(forms.Form):
    title = forms.CharField(max_length=100)
    files = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
