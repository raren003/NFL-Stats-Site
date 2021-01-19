from django import forms


POSITIONS = [
    ('WR', 'Wide Receiver'),
    ('QB', 'Quarterback'),
    ('RB', 'Running Back'),
    ('FB', 'Fullback'),
    ('HB', 'Halfback'),
    ('TE', 'Tight End'),
    ('OL', 'Offensive Lineman'),
    ('C', 'Center'),
    ('KR', 'Kick Returner'),
    ('K', 'Kicker'),
    ('OC', 'Offensive Center'),
    ('OT', 'Offensive Tackle'),
    ('DT', 'Defensive Tackle'),
    ('DE', 'Defensive End'),
    ('DB', 'Defensive Back'),
    ('CB', 'Cornerback'),
    ('LB', 'Linebacker'),
    ('OLB', 'Outside Linebacker'),
    ('MLB', 'Middle Linebacker'),
    ('OG', 'Offensive Guard'),
    ('FS', 'Free Safety'),
    ('S', 'Safety'),
    ('P', 'Punter'),
    ('PR', 'Punt Returner'),
    ]


class ReceiveForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)


class AddReceivingPlayForm(forms.Form):
    player_id = forms.CharField(label="Player Id", max_length=8, required=False)
    rec_yards = forms.IntegerField(label="Receiving Yards")
    rec_position = forms.CharField(label="Position", required=False, widget=forms.Select(choices=POSITIONS))


class TopReceiveForm(forms.Form):
    player_num = forms.IntegerField(label='Number of players', max_value=100, min_value=1)


class AddReceivingPlayerForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Last Name', max_length=100)
    rec_position = forms.CharField(label="Position", required=False, widget=forms.Select(choices=POSITIONS))


class DelReceivingPlayerForm(forms.Form):
    player_id = forms.CharField(label="Player Id", max_length=8, required=False)
