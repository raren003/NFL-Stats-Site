from django import forms
from django.core import validators

# Define years that the combine was held to select from
SEASON_YEARS = [tuple([x,x]) for x in range(2004, 2020)]
SEASON_YEARS.insert(0, ('', ''))

# Define the season "types" (preseason, regular, postseason)
SEASON_TYPES = [
    ('PRE','Preseason'),
    ('REG','Regular season'),
    ('POST','Postseason')
]

# Form to enter NFL year in which to review standings
class YearForm(forms.Form):
    year_val = forms.IntegerField(label = 'season year', required = False, widget = forms.Select(choices=SEASON_YEARS))
    season_val = forms.CharField(label='season type', required=False, widget = forms.Select(choices=SEASON_TYPES))
    # This is extra protection code to prevent a bot from entering bogus info on your site
    bot_catcher = forms.CharField(required=False, 
                                  widget=forms.HiddenInput, # Field won't show up on page for user, will be in background HTML
                                  validators=[validators.MaxLengthValidator(0)]) # Ensure a bot didn't fill in something