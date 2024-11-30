from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from .models import Event, Person, Cause,work

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),  # Use HTML5 date picker
        }

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            'name', 'photo', 'phone', 'email', 'address', 
            'disability_type', 'dis_percentage', 'udid_no', 
            'aadhaar_no', 'age', 'gender', 'dependent', 
            'occupation', 'salary', 'it_return'
        ]
        widgets = {
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'disability_type': forms.TextInput(attrs={'class': 'form-control'}),
            'dis_percentage': forms.TextInput(attrs={'class': 'form-control'}),
            'udid_no': forms.TextInput(attrs={'class': 'form-control'}),
            'aadhaar_no': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.TextInput(attrs={'class': 'form-control'}),
            'dependent': forms.TextInput(attrs={'class': 'form-control'}),
            'occupation': forms.TextInput(attrs={'class': 'form-control'}),
            'salary': forms.TextInput(attrs={'class': 'form-control'}),
            'it_return': forms.TextInput(attrs={'class': 'form-control'}),
        }

     # Override the default __init__ method to make each field required
    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True  # Make all fields required

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit() or len(phone) != 10:
            raise ValidationError("Phone number must be 10 digits.")
        return phone

    def clean_udid_no(self):
        udid_no = self.cleaned_data.get('udid_no')
        if not udid_no.isdigit() or len(udid_no) != 16:
            raise ValidationError("UDID number must be 16 digits.")
        return udid_no

    def clean_email(self):
        email = self.cleaned_data.get('email')
        validator = EmailValidator()
        try:
            validator(email)
        except ValidationError:
            raise ValidationError("Enter a valid email address.")
        return email

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            if not photo.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                raise ValidationError("Photo must be a .jpg, .jpeg, or .png file.")
            if photo.size > 2 * 1024 * 1024:  # 2 MB limit
                raise ValidationError("Photo size must be under 2 MB.")
        return photo    

    def clean_addhaar(self):
        aadhaar_no = self.cleaned_data.get('aadhaar_no')
        if not aadhaar_no.isdigit() or len(aadhaar_no) != 1:
            raise ValidationError("Aadhaar number must be 12 digits.")
        return aadhaar_no


class CauseForm(forms.ModelForm):
    class Meta:
        model = Cause
        fields = ['name', 'img', 'detail', 'raised', 'goal']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'img': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'detail': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'raised': forms.NumberInput(attrs={'class': 'form-control'}),
            'goal': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class WorkForm(forms.ModelForm):
    class Meta:
        model = work
        fields = ['name', 'img', 'detail']