from django import forms
from django.forms import fields, widgets
from .models import Contact,Post

class ContactForm(forms.ModelForm):
    class Meta:
        model=Contact
        fields='__all__'
    def __init__(self,*args,**kwargs):
            super().__init__(*args,**kwargs)
            self.fields['name'].label='My Name'
            self.fields['name'].initial='My Name'
            self.fields['phone'].initial='+880'
    def clean_name(self):
        value=self.cleaned_data.get('name')
        num_of_w=value.split(' ')
        if len(num_of_w)>3:
            self.add_error('name','Name can have maximum 3 words')
        else:
            return value

            
class ContactFormtwo(forms.ModelForm):
    class Meta:
        model=Contact
        fields='__all__'

class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        exclude=['user','id','slug','created_at']
        widgets={
            'class_in':forms.CheckboxSelectMultiple(attrs={
                'multiple':True
            }),
            'subject':forms.CheckboxSelectMultiple(attrs={
                'multiple':True
            }),

        }