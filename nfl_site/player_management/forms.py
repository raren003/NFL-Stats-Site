from django import forms
from django.core import validators

# Request input from user to amend players
class PlayerForm(forms.Form):
    player_first_name = forms.CharField(
        label = 'Enter player first name', 
        required = True
    )
    player_last_name = forms.CharField(label = 'Enter player last name', required = True)

    # This is extra protection code to prevent a bot from entering bogus info on your site
    bot_catcher = forms.CharField(required=False, 
                                  widget=forms.HiddenInput, # Field won't show up on page for user, will be in background HTML
                                  validators=[validators.MaxLengthValidator(0)]) # Ensure a bot didn't fill in something

class EditForm(forms.Form):
    player_pos = forms.CharField(
        label = "Position", 
        required = False, 
        max_length=2,
        widget=forms.TextInput(attrs={'placeholder':'Two character position group','class':'pos-placeholder'})
    )
    player_dob = forms.DateTimeField(
        required=False,
        input_formats=['%m/%d/%Y'],
        widget=forms.DateTimeInput(attrs = {
            'class':'form-control datetimepicker-input',
            'data-target':'#datetimepicker1'
        })
    )
    player_college = forms.CharField(label = "College", required = False)
    player_height = forms.DecimalField(label = "Height", required = False)
    player_weight = forms.DecimalField(label = "Weight", required = False)

    # This is extra protection code to prevent a bot from entering bogus info on your site
    bot_catcher = forms.CharField(required=False, 
                                  widget=forms.HiddenInput, # Field won't show up on page for user, will be in background HTML
                                  validators=[validators.MaxLengthValidator(0)]) # Ensure a bot didn't fill in something

#class SaveForm(forms.Form):
    #print('HI')