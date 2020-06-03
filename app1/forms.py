from django import forms

class ProfileForm(forms.Form):
   file = forms.FileFields()