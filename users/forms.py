from .models import Contact, Education, Experience, Project
from django import forms
from django.forms import widgets
from django.contrib.auth.models import User

class SignupForm(forms.Form):
    dob=forms.DateField(label='Date of Birth: ',widget=widgets.DateInput(attrs={'type':'date'}))
    company=forms.CharField(label='Company: ', max_length=50)
    profile_img=forms.ImageField(label='')
    phone=forms.CharField(max_length=13)
    location=forms.CharField(max_length=25)

class FormattedModelForm(forms.ModelForm):
    def as_myformat(self):
        return self._html_output(
            normal_row='''<div class="form-group">
                            <div class="row">
                                <label class="control-label col-sm-3">%(label)s</label>
                                <div class="col-sm-5">
                                    %(field)s
                                    %(errors)s
                                </div>
                                <div class="col-sm-4"></div>
                            </div>
                            <div class="row">
                                %(help_text)s
                            </div>
                    </div>''',
            error_row='<span class="error">%s</span>',
            row_ender='</div>',
            help_text_html='<small class="gray offset-3 col-sm-9">%s</small>',
            errors_on_separate_row=False,
        )

class UserUpdateForm(FormattedModelForm):        #for updating info of the user on the profile page
    email=forms.EmailField()
    class Meta:
         model = User                            
         fields = ['username','email']

class ExperienceForm(FormattedModelForm):
    class Meta:
        model=Experience
        fields=['experience']

class ProjectForm(FormattedModelForm):
    class Meta:
        model=Project
        fields=['project']
    
class EducationForm(FormattedModelForm):
    class Meta:
        model=Education
        fields=['education']

class ContactUpdateForm(FormattedModelForm):        #for updating info of the user on the profile page
    class Meta:
         model = Contact                           
         fields = ['gmail','mobile','outlook','linkedin']