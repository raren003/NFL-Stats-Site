from django.shortcuts import render
from passing import forms
from static.team42libraries.csvtodict import csv_to_dict
from operator import itemgetter
from pandasql import sqldf

import pandas as pd
import pathlib
import plotly
import plotly.graph_objs as go
import plotly.express as px
import numpy as np
import time

_DATA_PATH = 'static/archive/'
_DROP_FRAME = [ 
    'passId',
    'playId',
    'teamId',
    'playerId',
    'passAtt',
    'passComp',
    'passTd',
    'passInt',
    'passIntTd',
    'passSack',
    'passSackYds',
    'passHit',
    'passDef',
    'passNull',
    ]

_RENAME_COLS = {
    'passPosition' : 'Pass Position',
    'passOutcomes' : 'Pass Outcome',
    'passDirection' : 'Pass Direction',
    'passDepth' : 'Pass Depth',
    'passLength' : 'Pass Length'
    }

pass_df = pd.DataFrame()
players_df = pd.DataFrame()
top_players_df = pd.DataFrame()
new_pass = pd.DataFrame()
previous_time = 0

if pathlib.Path('static/archive/').exists():
    # Read associated csv files
    pass_df = csv_to_dict(f'{_DATA_PATH}passer.csv', 1)
    players_df = csv_to_dict(f'{_DATA_PATH}players.csv', 1)


# Create your views here.
def pass_page(request):
    global pass_df, players_df, previous_time, top_players_df, new_pass

    run_time = 0

    if pass_df.empty or players_df.empty:
        pass_df = csv_to_dict(f'{_DATA_PATH}passer.csv', 1)
        players_df = csv_to_dict(f'{_DATA_PATH}players.csv', 1)
        top_players_df = pd.DataFrame()


    # Set holding variables
    form = forms.PassingForm()
    analytics = forms.PassingAnalytics()
    context = {'form': form, 'analytics': analytics}

    if request.POST.get('Search') == 'Search':
        form = forms.PassingForm(request.POST)
        if form.is_valid():
            context = parse_form_entries(form)
            context['analytics'] = analytics

    if request.POST.get('Show Table') == 'Show Table' or request.POST.get('Show Graph') == 'Show Graph' or request.POST.get('Show Scatter Plot') == 'Show Scatter Plot':
        start_time = time.time()
        analytics = forms.PassingAnalytics(request.POST)
        if analytics.is_valid():
            top_player_count = analytics.cleaned_data.get('top_player_count')
            if top_players_df.empty:
                passing_analytics()
            context = {'analytics': analytics, 'results': top_players_df.head(abs(top_player_count)), 'columns' : top_players_df.columns, 'n_count' : top_player_count}
            run_time = time.time() - start_time
            if previous_time != 0:
                context['previous_time'] = str(previous_time)
            previous_time = run_time
            context['time'] = str(run_time)
            context['form'] = form
            context['exists'] = True

        if request.POST.get('Show Graph') == 'Show Graph':
            results = context['results']
            top_player_count = context['n_count']
            context['results'] = pd.DataFrame()

            fig = go.Figure(data=[
                go.Bar(name='Total Passing Length (Yards)', x=results['Player Name'], y=results['Total Passing Length (Yards)']),
                go.Bar(name='Total Times Passed (from csv)', x=results['Player Name'], y=results['Total Times Passed (from csv)'])
                ], 
                layout_title_text=f'Top {top_player_count} Players (Total Passing Yards)' )

            fig.update_layout(barmode='group')
            graph_div = plotly.offline.plot(fig, output_type="div")
            context['graph_div'] = graph_div

        if request.POST.get('Show Scatter Plot') == 'Show Scatter Plot':
            results = context['results']
            top_player_count = context['n_count']
            context['results'] = pd.DataFrame()

            fig = px.scatter(results, x="Total Passing Length (Yards)", y="Total Times Passed (from csv)", hover_name="Player Name", title="Total Passing Length vs Total Times Passed")
            graph_div = plotly.offline.plot(fig, output_type="div")
            context['graph_div'] = graph_div

    if request.POST.get('Add') == 'Add':
        form = forms.PassingForm(request.POST)
        if form.is_valid():
            add_passing_player(form)
            context['form'] = form
            context['results'] = new_pass
            context['columns'] = new_pass.columns
            context['new_entry'] = "New Entry Added"

    if request.POST.get('Delete') == 'Delete' or request.POST.get('Delete Player') == 'Delete Player':
        form = forms.PassingForm(request.POST)
        if form.is_valid():
            if request.POST.get('Delete') == 'Delete':
                delete_passing_player(form)
                context['player_delete'] = "Passing Data for Player Deleted"
            if request.POST.get('Delete Player') == 'Delete Player':
                delete_passing_player(form, 1)
                context['player_delete'] = "Player Deleted"
            context['form'] = form

    return render(request,'passing/passing.html', context) 


def parse_form_entries(form):
    global pass_df, players_df
    results = pd.DataFrame()

    # Get values from form
    player_name = form.cleaned_data.get('player_name').title()
    passing_outcome = form.cleaned_data.get('passing_outcome')
    passing_direction = form.cleaned_data.get('passing_direction')
    passing_depth = form.cleaned_data.get('passing_depth')
    passing_length = str(form.cleaned_data.get('passing_length'))

    if player_name:
        player_name = player_name.split()
        first_name = player_name[0]

        if len(player_name) < 2:
            return {'form': form, 'empty': 'Last Name Not Entered!'}

        last_name = player_name[1]
        name_filter = players_df.loc[(players_df['nameFirst'] == first_name) & (players_df['nameLast'] == last_name)]

        if len(name_filter) == 0:
            return {'form': form, 'empty': 'Player Does Not Exist!'}

    # Get dataframe of the player the user selects
    results = pass_df.loc[(name_filter['playerId'].values[0] == pass_df['playerId'].values)]

    # If user selects passng outcome
    if passing_outcome != "":
        results = results.loc[(results['passOutcomes'] == passing_outcome)]

    # If user selects passing direction
    if passing_direction != '':
        results = results.loc[(results['passDirection'] == passing_direction)]

    # If user selects passing depth
    if passing_depth != '':
        results = results.loc[(results['passDepth'] == passing_depth)]

    # If user enters passing length
    if passing_length != 'None':
        results = results.loc[(results['passLength'] == passing_length)]

    # If results has data
    if not results.empty:
        results.insert(0, 'Player Name', f'{first_name} {last_name}')
        results = results.drop(columns=_DROP_FRAME)
        results = results.rename(columns=_RENAME_COLS)
        results.insert(loc=0, column='#', value=np.arange(start=1, stop=len(results)+1))

    return {'form': form, 'results': results, 'columns' : results.columns}


def passing_analytics():
    global top_players_df

    # Get overall passing yards for each player without pandas
    top_player_dict = top_n_passing_yards()

    r_dict={}
    temp_df = pd.DataFrame()
    results = pd.DataFrame()

    for key, value in top_player_dict.items():
        r_dict = {
            'Player Name' : get_player_name(key),
            'Total Passing Length (Yards)': value[0],
            'Total Times Passed (from csv)': value[1],
            'Average Passing Length (Yards)': value[2],
        }
        temp_df = pd.DataFrame(r_dict, index=[0])
        results = results.append(temp_df, ignore_index=True)

    results.insert(loc=0, column='#', value=np.arange(start=1, stop=len(results)+1))

    top_players_df = results


# Analytics are done not using Pandas
def top_n_passing_yards():
    global pass_df
    total_passing_dict = {}
    temp_df = pass_df[['playerId', 'passLength']]
    pass_dict = temp_df.to_dict()
    for i in range(len(pass_dict['playerId'])):
        cell_val = pass_dict['passLength'][i]
        player_id = pass_dict['playerId'][i]
        if cell_val:
            list_key = [int(cell_val), 1, 0]
            if player_id in total_passing_dict:
                total_passing_dict[player_id][0] += list_key[0]
                total_passing_dict[player_id][1] += list_key[1]
            else:
                total_passing_dict[player_id] = list_key


    passing_yards_desc = sorted(total_passing_dict.items(), key=itemgetter(1), reverse=True)
    # get the top n records from list and cast into a dictionary
    records = dict(passing_yards_desc)

    # Calculate average passing yards
    for key, value in records.items():
        value[2] = round(value[0]/value[1], 3)

    return records


def get_player_name(player_id):
    global players_df
    return players_df.loc[(players_df['playerId'] == player_id)]['nameFull'].values[0]


def add_passing_player(form):
    global pass_df, players_df, top_players_df, new_pass

    max_pass_id = int(pass_df['passId'].max())
    max_player_id = int(players_df['playerId'].max())

    # Get values from form
    player_name = form.cleaned_data.get('player_name').title()
    passing_outcome = form.cleaned_data.get('passing_outcome')
    passing_direction = form.cleaned_data.get('passing_direction')
    passing_depth = form.cleaned_data.get('passing_depth')
    passing_length = form.cleaned_data.get('passing_length')

    full_name = player_name.split()
    first_name = full_name[0]
    last_name = full_name[1]

    name_filter = players_df.loc[(players_df['nameFirst'] == first_name) & (players_df['nameLast'] == last_name)]

    if len(name_filter) == 0:
        player_id = str(max_player_id+1)
        new_player = pd.DataFrame({'playerId' : player_id, 
                                   'nameFirst' : first_name, 
                                   'nameLast' : last_name, 
                                   'nameFull' : f'{first_name} {last_name}', 
                                   'position': 'QB'
                                   },
                                   index=[0]
                                   )

        players_df = players_df.append(new_player, ignore_index=True)
    else:
        player_id = name_filter['playerId'].values[0]

    if not passing_outcome:
        passing_outcome = 'None'

    if not passing_direction:
        passing_direction = 'None'

    if not passing_depth:
        passing_depth = 'None'

    if not passing_length:
        passing_length = '0'

    new_pass = pd.DataFrame({'passId': str(max_pass_id+1),
                               'playerId': player_id,
                               'passPosition': 'QB',
                               'passOutcomes': passing_outcome,
                               'passDirection': passing_direction,
                               'passDepth': passing_depth,
                               'passLength': str(passing_length)
                               },
                               index=[0]
                               )

    pass_df = pass_df.append(new_pass, ignore_index=True)
    pass_df = pass_df.reset_index(drop=True)

    new_pass.insert(0, 'Player Name', f'{first_name} {last_name}')
    new_pass = new_pass.drop(columns=['passId', 'playerId'])
    new_pass = new_pass.rename(columns=_RENAME_COLS)
    new_pass.insert(loc=0, column='#', value=np.arange(start=1, stop=len(new_pass)+1))

    if not top_players_df.empty:
        temp_df = top_players_df.loc[top_players_df['Player Name']==player_name]
        if not temp_df.empty:
            new_pass_length = temp_df['Total Passing Length (Yards)'].values[0] + int(passing_length)
            new_times_passed = temp_df['Total Times Passed (from csv)'].values[0] + 1
            
            top_players_df.loc[top_players_df['Player Name']==player_name, ['Total Passing Length (Yards)', 'Total Times Passed (from csv)', 'Average Passing Length (Yards)']] = [new_pass_length, new_times_passed, round(new_pass_length/new_times_passed, 3)]
            top_players_df = top_players_df.sort_values('Total Passing Length (Yards)', ascending=False)
            
        else:
            new_top_n = pd.DataFrame({'Player Name': player_name,
                                    'Total Passing Length (Yards)': int(passing_length),
                                    'Total Times Passed (from csv)': 1,
                                    'Average Passing Length (Yards)': round(int(passing_length)/1, 3),

                                    },
                                    index=[0]
                                    )
            top_players_df = top_players_df.append(new_top_n, ignore_index=True)
            top_players_df = top_players_df.sort_values('Total Passing Length (Yards)', ascending=False)

        top_players_df = top_players_df.drop('#', 1)
        top_players_df.insert(loc=0, column='#', value=np.arange(start=1, stop=len(top_players_df)+1))

def delete_passing_player(form, full_delete = 0):
    global pass_df, players_df, top_players_df

    # Get values from form
    player_name = form.cleaned_data.get('player_name').title()
    passing_outcome = form.cleaned_data.get('passing_outcome')
    passing_direction = form.cleaned_data.get('passing_direction')
    passing_depth = form.cleaned_data.get('passing_depth')
    passing_length = str(form.cleaned_data.get('passing_length'))

    full_name = player_name.split()
    first_name = full_name[0]
    last_name = full_name[1]

    name_filter = players_df.loc[(players_df['nameFirst'] == first_name) & (players_df['nameLast'] == last_name)]

    if len(name_filter) != 0:

        # Get dataframe of the player the user selects
        results = pass_df.loc[(name_filter['playerId'].values[0] == pass_df['playerId'].values)]

        # Delete Player From
        if full_delete:
            pass_df = pass_df.drop(results.index)
            pass_df = pass_df.reset_index(drop=True)
            players_df = players_df.drop(name_filter.index)
            players_df = players_df.reset_index(drop=True)
            if not top_players_df.empty:
                top_players_df = top_players_df.drop(top_players_df.loc[top_players_df['Player Name']==player_name].index)
                top_players_df = top_players_df.reset_index(drop=True)

        else:
            # If user selects passng outcome
            if passing_outcome != '':
                results = results.loc[(results['passOutcomes'] == passing_outcome)]

            # If user selects passing direction
            if passing_direction != '':
                results = results.loc[(results['passDirection'] == passing_direction)]

            # If user selects passing depth
            if passing_depth != '':
                results = results.loc[(results['passDepth'] == passing_depth)]

            # If user enters passing length
            if passing_length != 'None':
                results = results.loc[(results['passLength'] == passing_length)]

            pass_df = pass_df.drop(results.index)
            pass_df = pass_df.reset_index(drop=True)

            if not top_players_df.empty:
                results['passLength'] = results['passLength'].astype(int)
                results_total_passing_length = results['passLength'].sum()
                results_count = len(results)
                temp_df = top_players_df.loc[top_players_df['Player Name']==player_name]
                new_pass_length = temp_df['Total Passing Length (Yards)'].values[0] - results_total_passing_length
                new_times_passed = temp_df['Total Times Passed (from csv)'].values[0] - results_count
                
                top_players_df.loc[top_players_df['Player Name']==player_name, ['Total Passing Length (Yards)', 'Total Times Passed (from csv)', 'Average Passing Length (Yards)']] = [new_pass_length, new_times_passed, round(new_pass_length/new_times_passed, 3)]
                top_players_df = top_players_df.sort_values('Total Passing Length (Yards)', ascending=False)

        if not top_players_df.empty:
            top_players_df = top_players_df.drop('#', 1)
            top_players_df.insert(loc=0, column='#', value=np.arange(start=1, stop=len(top_players_df)+1))
