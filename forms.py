from django import forms
from .models import Student

#define the form
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['fname', 'lname', 'teachername', 'socialrank', 'focus', 'sound_env', 'friend', 'board_distance']