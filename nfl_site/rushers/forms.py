from django import forms
from .nfldata import readTeams

get_teams = readTeams()
team_names =""
if get_teams is not None:
    team_names = sorted(get_teams['draftTeam'].to_list())

TEAM_CHOICES= [('all time','All Time'),]
for name in team_names:
    TEAM_CHOICES.append((str(name),name))

class RushersForm(forms.Form):
    first_name = forms.CharField(label = 'First Name', max_length=100,required=True)
    last_name = forms.CharField(label = 'Last Name', max_length=100,required=True)

class TeamPickForm(forms.Form):
    team_name = forms.CharField(label = 'Top Rushers',required = True, widget=forms.Select(choices=TEAM_CHOICES) )