from django import forms

class ImageGenForm(forms.Form):
    image         = forms.URLField()
    prompt = forms.CharField(max_length=500)
