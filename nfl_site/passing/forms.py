from django import forms
from django.core import validators

PASSING_OUTCOME = [
    ('',''),
    ('complete', 'Complete'), 
    ('incomplete', 'Incomplete'), 
    ('interception', 'Interception'),
    ('sack', 'Sack')
    ]

PASSING_DIRECTION = [
    ('',''),
    ('left', 'Left'), 
    ('middle', 'Middle'), 
    ('right', 'Right')
    ]

PASSING_DEPTH = [
    ('',''),
    ('short', 'Short'), 
    ('deep', 'Deep')
    ]

class PassingForm(forms.Form):
    player_name = forms.CharField(label = 'Player\'s Name', required = True)
    passing_outcome = forms.CharField(label = 'Passing Outcome', required = False, widget = forms.Select(choices=PASSING_OUTCOME))
    passing_direction = forms.CharField(label = 'Passing Direction', required = False, widget = forms.Select(choices=PASSING_DIRECTION))
    passing_depth = forms.CharField(label = 'Passing Depth', required = False, widget = forms.Select(choices=PASSING_DEPTH))
    passing_length = forms.IntegerField(label = 'Passing Length (Yards)', required = False)


class PassingAnalytics(forms.Form):
    top_player_count = forms.IntegerField(label = 'How Many?', required = True)