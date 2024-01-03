from django import forms


from .models import course_model,HOD_model,student_model,teacher_model

class course_form(forms.ModelForm):
    class Meta:
        model=course_model
        fields=["course_name","time_period"]

class HOD_form(forms.ModelForm):
    class Meta:
        model=HOD_model
        fields=["HOD_name","course"]

class student_form(forms.ModelForm):
    class Meta:
        model=student_model
        fields=["student_name","student_course","student_head",]

class teacher_form(forms.ModelForm):
    class Meta:
        model=teacher_model
        fields=["teacher_name","teacher_course","HOD"]