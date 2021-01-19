from django import forms
from django.core import validators
from enum import Enum

# Custom validator - an example of how you can create your own function to validate form entries
''' Example code, commented out
def check_for_z(value):
    if value[0].lower() != 'z':
        raise forms.ValidationError("Needs to start with lowercase z")
'''
# Define combine events that are present in the combine.csv dataset
COMBINE_EVENTS = [
    ('', ''), # Provide the option to not select a combine measurement
    ('combineArm', 'Arm Length'),
    ('combine40yd', '40-yard dash'),
    ('combineVert', 'Vertical jump'),
    ('combineBench', 'Bench Press'),
    ('combineShuttle', 'Shuttle drill'),
    ('combineBroad', 'Broad Jump'),
    ('combine3cone', '3-Cone Drill'),
    ('combine60ydShuttle', '60-yard shuttle'),
    ('combineWonderlic', 'Wonderlic'),
]

# Define combine position groups
COMBINE_POS = [
    ('', ''),
    ('QB', 'Quarterback'),
    ('WR', 'Wide Receiver'),     
    ('CB', 'Cornerback'),      
    ('RB', 'Running Back'),      
    ('DE', 'Defensive End'),      
    ('OLB', 'Outside Linebacker'),     
    ('OT', 'Offensive Tackle'),      
    ('DT', 'Defensive Tackle'),      
    ('TE', 'Tight-End'),      
    ('OG', 'Offensive Guard'),      
    ('ILB', 'Inside Linebacker'),     
    ('FS', 'Free Safety'),      
    ('SS', 'Strong Safety'),      
    ('C', 'Center'),       
    ('FB', 'Fullback'),      
    ('LB', 'Linebacker'),       
    ('P', 'Punter'),        
    ('OL', 'Offensive Line'),       
    ('K', 'Kicker'),        
    ('DL', 'Defensive Line'),       
    ('DB', 'Defensive Back'),       
    ('S', 'Safety'),        
    ('EDG', 'Edge'),      
    ('PK', 'Placekicker'),       
    ('LS', 'Left Safety'),        
    ('NT', 'Nosetackle'),  
]
# Define years that the combine was held to select from
COMBINE_YEARS = [tuple([x,x]) for x in range(1987, 2020)]
COMBINE_YEARS.insert(0, ('', ''))

# Form object that we will render to receive input
class CombineForm(forms.Form):
    player_first_name = forms.CharField(label = 'Enter player first name', required = False)
    player_last_name = forms.CharField(label = 'Enter player last name', required = False)
    combine_year = forms.IntegerField(label = 'Select combine year', required = False, widget = forms.Select(choices=COMBINE_YEARS))
    combine_event = forms.CharField(label = 'Select combine measurement', required = False, widget = forms.Select(choices=COMBINE_EVENTS))
    combine_pos = forms.CharField(label = 'Select combine position group', required = False, widget = forms.Select(choices=COMBINE_POS))

    # This is extra protection code to prevent a bot from entering bogus info on your site
    bot_catcher = forms.CharField(required=False, 
                                  widget=forms.HiddenInput, # Field won't show up on page for user, will be in background HTML
                                  validators=[validators.MaxLengthValidator(0)]) # Ensure a bot didn't fill in something
   
    ''' Example code of how to ensure required fields match
    def clean(self):
        all_clean_data = super().clean() # return all clean data for the form
        email = all_clean_data['email']
        vmail = all_clean_data['verify_email']
        if email != vmail:
            raise forms.ValidationError("Make sure emails match")   
    '''

class CombineStats(forms.Form):
    statistic = forms.CharField(label = "Select Statistic", required = False, widget = forms.Select(choices=[('',''),('aa','Above Average'),('ba','Below Average'),('o','Outlier'),('t','Top'),('b','Bottom')]))
    num_players = forms.IntegerField(label = "Number of players", max_value=100, min_value=1, required = False)

class NewStats(forms.Form):
    dash_stat = forms.FloatField(label = "40-yard Dash", required = False)
    vert_stat = forms.FloatField(label = "Vertical Jump", required = False)
    bench_stat = forms.IntegerField(label = "Bench Press", required = False)
    shuttle_stat = forms.FloatField(label = "Shuttle Drill", required = False)
    broad_stat = forms.FloatField(label = "Broad Jump", required = False)
    cone_stat = forms.FloatField(label = "3-Cone Drill", required = False)
    shuttle_60_stat = forms.FloatField(label = "60-yard Shuttle", required = False)
