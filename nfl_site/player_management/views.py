from django.shortcuts import render
import pandas as pd
import pathlib
import numpy as np
from pandasql import sqldf
from player_management import forms
from nfl_site.libraries import conv_height, getIndexes
from datetime import date, datetime

# Create your views here.
'''
Author: FSt.J
Code Comments: adding relative path variable to point to the directory location of my NFL datasets.
               For me, they're one directory above our project directory in a folder called nfl_data
'''
# NFL Data relative path
data_path = 'static/archive/'
save_path = 'static/saves/'

# Global Variables
players = pd.DataFrame()
players_filtered = pd.DataFrame()
player_first_name = ''
player_last_name = ''
data_edited = False

# Check if the csv path exists
if pathlib.Path(data_path).exists():
    #Read in combine.csv dataset
    players = pd.read_csv(data_path + 'players.csv')
    # Get collegeId to college mapping
    colleges = players[['collegeId','college']]
    colleges = colleges.drop_duplicates()

# Check if saves exist
if pathlib.Path(save_path).exists():
    saves_list = []

# response/combine page rendering
def player_management(request):
    player_form = forms.PlayerForm()
    edit_form = forms.EditForm()
    df_dict = []
    df_rec = []
    global players, players_filtered, player_first_name, player_last_name, data_edited 

    if players.empty:
        players = pd.read_csv(data_path + 'players.csv')
    
    # Set holding variables
    player_dict = {} # Store the player's ID and associated combine statistic
    player_pos = ''
    player_dob = ''
    player_college = ''
    player_height = ''
    player_weight = 0.0
    player_exists = False
    submit = False
    
    if request.method == "POST": # Means someone filled out our player_form
        player_form = forms.PlayerForm(request.POST)
        if player_form.is_valid():
            submit = True
            player_dict.clear()
            player_first_name = player_form.cleaned_data.get('player_first_name').title()
            player_last_name = player_form.cleaned_data.get('player_last_name').title()
            
            # Filter the players.csv for the entered info
            player_first_name = "\'" + player_first_name + "\'"
            player_last_name = "\'" + player_last_name + "\'"

            name_filter = players.loc[(players['nameFirst'] == player_first_name.strip('\'')) & (players['nameLast'] == player_last_name.strip('\''))]
            # Set variable if player exists or not
            if not name_filter.empty:
                player_exists = True
            else:
                player_exists = False
                context = {'player_form': player_form, 'edit_form': edit_form, 'df_dict':df_dict, 'df_rec':df_rec, 'does_not_exist': 'Player does not exist!', 'submit':submit}
                return render(request, 'player_management/player_management.html', context)
 
            # Filter the players dataframe
            players_filtered = sqldf(f"SELECT playerid AS 'Player ID', nameFirst AS 'First Name', nameLast AS 'Last Name', position AS 'Position', college AS 'College', heightInches AS 'Height(in)', weight AS 'Weight(lbs)', dob AS 'DOB', homeCity AS 'City', homeState AS 'State', homeCountry AS 'Country' FROM players WHERE nameFirst = {player_first_name} AND nameLast = {player_last_name};", globals())
            df_dict = players_filtered.to_dict()
            df_rec = players_filtered.to_dict(orient='records')


    if request.POST.get('Add Player') == 'Add Player':
        edit_form = forms.EditForm(request.POST)
        player_exists = True
        submit = True
        data_edited = True
        if edit_form.is_valid():
            # Grab the data entered on the form
            player_pos = edit_form.cleaned_data.get('player_pos')
            player_dob = edit_form.cleaned_data.get('player_dob')
            player_college = edit_form.cleaned_data.get('player_college')
            player_height = edit_form.cleaned_data.get('player_height')
            player_weight = edit_form.cleaned_data.get('player_weight')
            
            # Add a new record to players.csv with playerID = max(playerID) + 1
            pid = max(players.playerId) + 1
            
            # Create an empty player dictionary, add the appropriate values from the form
            new_player = {
                'playerId': pid,
                'nameFirst': player_first_name.strip('\''),
                'nameLast': player_last_name.strip('\''),
                'nameFull' : player_first_name.strip('\'') + " " + player_last_name.strip('\''),
                'position' : None,
                'collegeId': None,
                'nflId': None,
                'combineId': None,
                'college': None,
                'heightInches': None,
                'weight': None,
                'dob': None,
                'ageAtDraft': None,
                'playerProfileUrl': 'https://www.ucr.edu/',
                'homeCity': "Riverside",
                'homeState': "CA",
                'homeCountry': "USA",
                'highSchool': "Riverside Prep",
                'hsCity': "Riverside",
                'hsState': "CA",
                'hsCountry': "USA"
            }

            # Note that you need to reassign the dataframe when doing append.  Append does not edit the dataframe in place
            players = players.append(new_player, ignore_index = True)
            
            # Check the values entered, and update the dictionary appropriately
            if player_pos:
                players.loc[(players['playerId'].values == pid, 'position')] = player_pos
            
            if player_dob:
                players.loc[(players['playerId'].values == pid, 'dob')] = str(player_dob).split()[0]
            
            if player_college:
                # Check to ensure the college maps to an existing college by collegeId
                if player_college in colleges.college.values:
                    players.loc[(players['playerId'].values == pid, 'college')] = player_college
                    players.loc[(players['playerId'].values == pid, 'collegeId')] = int(colleges[colleges['college'] == player_college].collegeId.values)
                else:
                    # Try and clean the college string, then remap
                    if len(player_college) == 3:
                        player_college = player_college.upper()
                    elif len(player_college) == 4 and player_college[0].upper() == 'U':
                        player_college = player_college.upper()
                    else:
                        player_college = player_college.title()

                    players.loc[(players['playerId'].values == pid, 'college')] = player_college

                    # if college exists in dataframe already set it to the same collegeId, otherwise set it to NaN
                    if player_college in colleges.college.values:
                        players.loc[(players['playerId'].values == pid, 'collegeId')] = int(colleges[colleges['college'] == player_college].collegeId.values)
                    else:
                        players.loc[(players['playerId'].values == pid, 'collegeId')] = np.nan

                
            if player_height:
                players.loc[(players['playerId'].values == pid, 'heightInches')] = float(player_height)

            if player_weight:
                players.loc[(players['playerId'].values == pid, 'weight')] = float(player_weight)
                
            players_filtered = \
                    players[
                        (players['playerId'] == pid)  
                    ][['playerId','nameFirst','nameLast','position','collegeId','college','heightInches','weight','dob','homeCity','homeState','homeCountry']]
            players_filtered.columns = [
                'Player ID',
                'First Name',
                'Last Name',
                'Position',
                'College ID',
                'College',
                'Height(in)',
                'Weight(lbs)',
                'DOB',
                'City',
                'State',
                'Country'
            ]
            df_dict = players_filtered.to_dict()
            df_rec = players_filtered.to_dict(orient='records')


    if request.POST.get('Edit Player') == 'Edit Player':
        edit_form = forms.EditForm(request.POST)
        player_exists = True
        submit = True
        data_edited = True
        if edit_form.is_valid():
            # ADD FIELD FOR PID IF > 1
            player_pos = edit_form.cleaned_data.get('player_pos')
            player_dob = edit_form.cleaned_data.get('player_dob')
            player_college = edit_form.cleaned_data.get('player_college')
            player_height = edit_form.cleaned_data.get('player_height')
            player_weight = edit_form.cleaned_data.get('player_weight')
        
        pid = players_filtered['Player ID'].values[0]

        if player_pos:
            players.loc[(players['playerId'].values == pid, 'position')] = player_pos
        
        if player_dob:
            players.loc[(players['playerId'].values == pid, 'dob')] = str(player_dob).split()[0]
        
        if player_college:
            players.loc[(players['playerId'].values == pid, 'college')] = player_college
            # if college exists in dataframe already set it to the same collegeId, otherwise set it to NaN
            if player_college in colleges.college.values:
                players.loc[(players['playerId'].values == pid, 'collegeId')] = int(colleges[colleges['college'] == player_college].collegeId.values)
            else:
                players.loc[(players['playerId'].values == pid, 'collegeId')] = np.nan

        if player_height:
            players.loc[(players['playerId'].values == pid, 'heightInches')] = float(player_height)

        if player_weight:
            players.loc[(players['playerId'].values == pid, 'weight')] = float(player_weight)

        # Filter the players dataframe
        players_filtered = sqldf(f"SELECT playerid AS 'Player ID', nameFirst AS 'First Name', nameLast AS 'Last Name', position AS 'Position', college AS 'College', heightInches AS 'Height(in)', weight AS 'Weight(lbs)', dob AS 'DOB', homeCity AS 'City', homeState AS 'State', homeCountry AS 'Country' FROM players WHERE nameFirst = {player_first_name} AND nameLast = {player_last_name};", globals())
        df_dict = players_filtered.to_dict()
        df_rec = players_filtered.to_dict(orient='records')


    if request.POST.get('Delete Player') == 'Delete Player':
        data_edited = True
        tup = getIndexes(players,players_filtered['Player ID'].values[0])
        drop_me  = tup[0][0]
        players = players.drop(drop_me)

    
    if data_edited and request.POST.get('Save Changes') == 'Save Changes':
        data_edited = False
        if not pathlib.Path(save_path).exists():
            save_dir = pathlib.Path(save_path)
            save_dir.mkdir(parents=True)

        today = date.today()
        date_time = datetime.now()
        t_date = today.strftime("%m%d%y")
        t_time = date_time.strftime("%H%M%S")

        players.to_csv(f'{save_path}players_{t_date}_{t_time}.csv')
        
        
    context = {'player_form': player_form, 'edit_form': edit_form, 'df_dict':df_dict, 'df_rec':df_rec, 'exists':player_exists, 'submit':submit, 'data_edited': data_edited}
    return render(request, 'player_management/player_management.html', context)