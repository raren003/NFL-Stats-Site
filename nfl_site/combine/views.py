from django.shortcuts import render
from combine import forms # Import forms module from combine app
from nfl_site.libraries import csv_to_dict, conv_height, mean, stddev, math, sumf # Get user functions
from pathlib import Path
import pandas as pd
import numpy as np
import time
# Dava viz packages
import plotly.offline as plot
import plotly.express as px
import plotly.graph_objects as go

# Create your views here.

# NFL Data relative path
data_path = 'static/archive/'

# Define a dict to map combine event header to clean name
COMBINE_DICT = {
    '': '', # Provide the option to not select a combine measurement
    'combineArm': 'Arm Length',
    'combine40yd': '40-yard dash',
    'combineVert': 'Vertical jump',
    'combineBench': 'Bench Press',
    'combineShuttle': 'Shuttle drill',
    'combineBroad': 'Broad Jump',
    'combine3cone': '3-Cone Drill',
    'combine60ydShuttle': '60-yard shuttle',
    'combineWonderlic':'Wonderlic',
}

# Read in the combine.csv data using Rob's CSV reader function
combine = ""
if Path(data_path).exists():
    combine = csv_to_dict(data_path + 'combine.csv', to_df = 1)
    combine['combineHeightConv'] = combine['combineHeight'].apply(lambda x: conv_height(float(x)))
    combine['combineYear'] = combine['combineYear'].apply(lambda x: int(x))
    for measure in COMBINE_DICT:
        if measure != '':
            combine[measure] = combine[measure].apply(lambda x: float(x) if x != None else x)

# Global sum, counter and avg variables that we'll check
total = 0
counter = 0

# response/combine page rendering
def combine_page(request):
    form = forms.CombineForm()
    statistics = forms.CombineStats()
    new_stats = forms.NewStats()
    df_dict = []
    df_rec = []

    # Define globals that will persist outside the combine_page function calls
    global combine
    global total
    global counter

    # Set holding variables
    player_first_name = ''
    player_last_name = ''
    combine_year = 0
    combine_event = ''
    combine_pos = ''
    num_players = 1
    user_stat = ""
    run_time = 0
    avg = 0
    sd = 0
    out_high = 0
    out_low = 0
    weight_fig = ""
    height_fig = ""
    hist_fig = ""
    player_exists = False
    dash_stat = 0
    vert_stat = 0
    bench_stat = 0
    shuttle_stat = 0
    broad_stat = 0
    cone_stat = 0
    shuttle_60_stat = 0
    new_player = ""
    stats_df = ""
    begin = 0
    end = 0

    # Holding variables for the data figures
    scat_fig = ""
    data_viz = combine

    if request.method == "POST": # Means someone filled out our form
        form = forms.CombineForm(request.POST)
        statistics = forms.CombineStats(request.POST)
        new_stats = forms.NewStats(request.POST)

        if form.is_valid(): 
            player_first_name = form.cleaned_data.get('player_first_name').title()
            player_last_name = form.cleaned_data.get('player_last_name').title()
            combine_year = form.cleaned_data.get('combine_year')
            combine_event = form.cleaned_data.get('combine_event')
            combine_pos = form.cleaned_data.get('combine_pos')
            if statistics.is_valid():
                num_players = statistics.cleaned_data.get('num_players')
                user_stat = statistics.cleaned_data.get('statistic')
            if new_stats.is_valid():
                dash_stat = new_stats.cleaned_data.get('dash_stat')
                vert_stat = new_stats.cleaned_data.get('vert_stat')
                bench_stat = new_stats.cleaned_data.get('bench_stat')
                shuttle_stat = new_stats.cleaned_data.get('shuttle_stat')
                broad_stat = new_stats.cleaned_data.get('broad_stat')
                cone_stat = new_stats.cleaned_data.get('cone_stat')
                shuttle_60_stat = new_stats.cleaned_data.get('shuttle_60_stat')
                
            combine_filtered = combine
            stats_df = combine
            # Filter the data based on player entries
            if player_first_name:
                combine_filtered = combine_filtered[combine_filtered['nameFirst'] == player_first_name]
            if player_last_name:
                combine_filtered = combine_filtered[combine_filtered['nameLast'] == player_last_name]
            if combine_year:
                combine_filtered = combine_filtered[combine_filtered['combineYear'] == combine_year]
                stats_df = stats_df[stats_df['combineYear'] == combine_year]
            if combine_pos:
                combine_filtered = combine_filtered[combine_filtered['combinePosition'] == combine_pos]
                stats_df = stats_df[stats_df['combinePosition'] == combine_pos]
            if combine_event:
                combine_filtered = combine_filtered[['playerId','combineYear','nameFirst','nameLast','combinePosition', 'position','college','combineHeightConv','combineWeight', combine_event]]
                combine_filtered.columns = ['Player ID','Year','First Name','Last Name','Combine Position','College Position','College','Height','Weight', COMBINE_DICT[combine_event]]
                if combine_event in ['combineArm','combineVert','combineBench','combineBroad','combineWonderlic']:
                            combine_filtered.sort_values(by=COMBINE_DICT[combine_event], ascending = False, inplace = True, na_position='last')
                else:
                    combine_filtered.sort_values(by=COMBINE_DICT[combine_event], ascending = True, inplace = True, na_position='last')
                # Change computations of the average and std.dev depending on if players were just added or deleted
                total = sumf(stats_df, combine_event) 
                counter = len(stats_df.index)
                begin = time.perf_counter()
                avg = mean(stats_df, combine_event)
                end = time.perf_counter()
                sd = stddev(stats_df, combine_event)
                if user_stat:
                    # Filter to players above the average ("above average" depends on the event, e.g. a 40-time < the average is considered above average)
                    if user_stat == 'aa':
                        if combine_event in ['combineArm','combineVert','combineBench','combineBroad','combineWonderlic']:
                            combine_filtered = combine_filtered[combine_filtered[COMBINE_DICT[combine_event]] > avg]
                            combine_filtered.sort_values(by=COMBINE_DICT[combine_event], ascending = False, inplace = True, na_position='last')
                        else:
                            combine_filtered = combine_filtered[combine_filtered[COMBINE_DICT[combine_event]] < avg]
                            combine_filtered.sort_values(by=COMBINE_DICT[combine_event], ascending = True, inplace = True, na_position='last')
                    # Filter to players below the average
                    if user_stat == 'ba':
                        if combine_event in ['combineArm','combineVert','combineBench','combineBroad','combineWonderlic']:
                            combine_filtered = combine_filtered[combine_filtered[COMBINE_DICT[combine_event]] < avg]
                            combine_filtered.sort_values(by=COMBINE_DICT[combine_event], ascending = True, inplace = True, na_position='last')
                        else:
                            combine_filtered = combine_filtered[combine_filtered[COMBINE_DICT[combine_event]] > avg]
                            combine_filtered.sort_values(by=COMBINE_DICT[combine_event], ascending = False, inplace = True, na_position='last')
                    # Filter to players who's performance was an outlier
                    if user_stat == 'o':
                        out_high = avg + (3 * sd)
                        out_low = avg - (3 * sd)
                        combine_filtered = combine_filtered[(combine_filtered[COMBINE_DICT[combine_event]] < out_low) | (combine_filtered[COMBINE_DICT[combine_event]] > out_high)]
                    # Filter top players - top and bottom differ depending on the event
                    if user_stat == 't':
                        if combine_event in ['combineArm','combineVert','combineBench','combineBroad','combineWonderlic']:
                            combine_filtered.sort_values(by=COMBINE_DICT[combine_event], ascending = False, inplace = True, na_position='last')
                        else:
                            combine_filtered.sort_values(by=COMBINE_DICT[combine_event], ascending = True, inplace = True, na_position='last')
                        if num_players:
                            combine_filtered = combine_filtered.head(n=num_players)
                    # Filter bottom players
                    if user_stat == 'b':
                        if combine_event in ['combineArm','combineVert','combineBench','combineBroad','combineWonderlic']:
                            combine_filtered.sort_values(by=COMBINE_DICT[combine_event], ascending = True, inplace = True, na_position='last')
                        else:
                            combine_filtered.sort_values(by=COMBINE_DICT[combine_event], ascending = False, inplace = True, na_position='last')
                        if num_players:
                            combine_filtered = combine_filtered.head(n=num_players)
                # Simply restrict the view to the number of players selected
                if num_players:
                    combine_filtered = combine_filtered.head(n=num_players)
            else:
                combine_filtered = combine_filtered[['playerId','combineYear','nameFirst','nameLast','combinePosition', 'position','college','combineHeightConv','combineWeight']]
                combine_filtered.columns = ['Player ID','Year','First Name','Last Name','Combine Position','Collge Position','College','Height','Weight']
            
            # Code below is to create a scatterplot of wide receiver times vs their weight
            if combine_event:
                # Get rid of the NaNs
                data_viz = combine_filtered
                data_viz.dropna(subset=[COMBINE_DICT[combine_event]], inplace = True)
                # Some of the combine measures had no valid values for a particular combine year or position group
                if (len(data_viz) > 0):
                    data_viz['Name'] = data_viz['First Name'] + ' ' + data_viz['Last Name']
                    
                    # Histogram annotated with the average
                    fig = go.Figure()
                    fig.add_trace(go.Histogram(
                        x=data_viz[COMBINE_DICT[combine_event]],
                        name=COMBINE_DICT[combine_event],
                        marker_color='black',
                        opacity=0.75
                    ))
                    fig.update_layout(
                        title_text='Histogram of {}'.format(COMBINE_DICT[combine_event]),
                        xaxis_title_text='Value',
                        yaxis_title_text='Count',
                        bargap=0.1,
                        bargroupgap=0.1,
                        font={'family':'Arial','color':'blue'}
                    )
                    fig.add_shape(
                        go.layout.Shape(type='line',xref='x', x0=avg, y0=0, x1=avg, y1=12, line={'dash':'dash','color':'red'})
                    )
                    fig.add_annotation(
                        x=avg,
                        y=12,
                        text="Avg. {}: {}".format(COMBINE_DICT[combine_event], round(avg,2)),
                        font={'color':'red'},
                        arrowhead=2
                    )
                    hist_fig = plot.plot(fig, output_type='div')

                    # Plot the combine event score vs. weight
                    fig = px.scatter(data_viz, x='Weight',y=COMBINE_DICT[combine_event],color='Name',title="Weight vs. {}".format(COMBINE_DICT[combine_event]), 
                    labels={'Name':'Player Name',
                            'Weight':'Weight (lbs)'})
                    fig.update_xaxes(title_font=dict(size=14, family='Arial', color='Blue'))
                    fig.update_yaxes(title_font=dict(size=14, family='Arial', color='Blue'))
                    fig.update_traces(marker=dict(
                        size=13,
                        line=dict(width=1.5,color='DarkSlateGrey')),
                    )
                    fig.update_layout(showlegend=False, title_text="Weight vs. {}".format(COMBINE_DICT[combine_event]), title_font=dict(size=18, family='Arial', color='Blue'))
                    weight_fig = plot.plot(fig, output_type='div')
                    
                    # Plot the combine event score vs. height
                    data_viz.Height = pd.Categorical(data_viz.Height, categories=[
                        "5\'6\"","5\'7\"","5\'8\"","5\'9\"","5\'10\"","5\'11\"","6\'0\"","6\'1\"","6\'2\"","6\'3\"","6\'4\"","6\'5\"","6\'6\"","6\'7\"","6\'8\""
                    ],
                    ordered = True)
                    data_viz.sort_values('Height', inplace = True)
                    fig = px.scatter(data_viz, x='Height',y=COMBINE_DICT[combine_event],color='Name',title="Height vs. {}".format(COMBINE_DICT[combine_event]), 
                    labels={'Name':'Player Name',
                            'Height':'Height (U.S. standard)'})
                    fig.update_xaxes(title_font=dict(size=14, family='Arial', color='Blue'))
                    fig.update_yaxes(title_font=dict(size=14, family='Arial', color='Blue'))
                    fig.update_traces(marker=dict(
                        size=13,
                        line=dict(width=1.5,color='DarkSlateGrey')),
                    )
                    fig.update_layout(showlegend=False, title_text="Height vs. {}".format(COMBINE_DICT[combine_event]), title_font=dict(size=18, family='Arial', color='Blue'))
                    height_fig = plot.plot(fig, output_type='div')

        # Update the data based on the first and last name entered
        name_filter = combine_filtered.loc[(combine_filtered['First Name'] == player_first_name) & (combine_filtered['Last Name'] == player_last_name)]
        if not name_filter.empty:
            player_exists = True
        if player_exists:
            if request.POST.get('Delete Player') == 'Delete Player':
                # Recompute stats
                total -= float(combine_filtered[(combine_filtered['First Name'] == player_first_name) & (combine_filtered['Last Name'] == player_last_name)][COMBINE_DICT[combine_event]])
                counter -= 1
                begin = time.perf_counter()
                avg = total / counter
                end = time.perf_counter()
                
                # Have to drop the player from the global combine dataset
                combine = combine[(combine['nameFirst'] != player_first_name) & (combine['nameLast'] != player_last_name)]
                combine_filtered = combine_filtered[(combine_filtered['First Name'] != player_first_name) & (combine_filtered['Last Name'] != player_last_name)]
        else:
            if request.POST.get('Add Player') == 'Add Player':
                # Add the new player to the combine dataframe
                new_player = {
                    'combineId':999999,
                    'playerId': 999999,
                    'combineYear':None,
                    'combinePosition':None,
                    'combineHeight':None,
                    'combineWeight':None,
                    'combineHand':None,
                    'nameFirst':player_first_name,
                    'nameLast':player_last_name,
                    'nameFull':player_first_name + " " + player_last_name,
                    'position':None,
                    'collegeId':999999,
                    'nflId':999999,
                    'college':None,
                    'heightInches':None,
                    'weight':None,
                    'dob':None,
                    'ageAtDraft':21,
                    'playerProfileUrl':"wwww.ucr.edu",
                    'homeCity': "Riverside",
                    'homeState': "CA",
                    'homeCountry': "USA",
                    'highSchool' : "Riverside High",
                    'hsCity' : "Riverside",
                    'hsState' : "CA",
                    'hsCountry': "USA",
                    'combineArm': np.nan,
                    'combine40yd': np.nan,
                    'combineVert': np.nan,
                    'combineBench': np.nan,
                    'combineShuttle': np.nan,
                    'combineBroad': np.nan,
                    'combine3cone': np.nan,
                    'combine60ydShuttle': np.nan,
                    'combineWonderlic': np.nan
                }
                
                # Update the records
                if combine_year:
                    new_player['combineYear'] = combine_year
                else:
                    #  Default to latest combine year in the dataset
                    new_player['combineYear'] = max(combine.combineYear)
                if combine_pos:
                    new_player['combinePosition'] = combine_pos
                else:
                    # Default to QB for simplicity
                    new_player['combinePosition'] = 'QB'

                if dash_stat:
                    new_player['combine40yd'] = dash_stat
                if vert_stat:
                    new_player['combineVert'] = vert_stat
                if bench_stat:
                    new_player['combineBench'] = bench_stat
                if shuttle_stat:
                    new_player['combineShuttle'] = shuttle_stat
                if broad_stat:
                    new_player['combineBroad'] = broad_stat
                if cone_stat:
                    new_player['combine3cone'] = cone_stat
                if shuttle_60_stat:
                    new_player['combine60ydShuttle'] = shuttle_60_stat 

                # Add to the combine dataset
                combine = combine.append(new_player, ignore_index = True)
                combine_filtered = combine
                if player_first_name:
                    combine_filtered = combine_filtered[combine_filtered['nameFirst'] == player_first_name]
                if player_last_name:
                    combine_filtered = combine_filtered[combine_filtered['nameLast'] == player_last_name]
                if combine_year:
                    combine_filtered = combine_filtered[combine_filtered['combineYear'] == combine_year]
                    stats_df = stats_df[stats_df['combineYear'] == combine_year]
                if combine_pos:
                    combine_filtered = combine_filtered[combine_filtered['combinePosition'] == combine_pos]
                    stats_df = stats_df[stats_df['combinePosition'] == combine_pos]
                if combine_event:
                    combine_filtered = combine_filtered[['playerId','combineYear','nameFirst','nameLast','combinePosition', 'position','college','combineHeightConv','combineWeight', combine_event]]
                    combine_filtered.columns = ['Player ID','Year','First Name','Last Name','Combine Position','College Position','College','Height','Weight', COMBINE_DICT[combine_event]]
                
                # Update the average calculation
                total += float(combine[(combine['nameFirst'] == player_first_name) & (combine['nameLast'] == player_last_name)][combine_event])
                counter += 1
                begin = time.perf_counter()
                avg = total / counter
                end = time.perf_counter()

        df_dict = combine_filtered.to_dict()
        df_rec = combine_filtered.to_dict(orient='records')
        avg = round(avg, 2)
        sd = round(sd, 2)
        out_high = round(avg + (3 * sd),2)
        out_low = round(avg - (3 * sd),2)
        run_time = round(end - begin,6)

    context = {'form': form, 'statistics': statistics, 'new_stats':new_stats,'df_dict':df_dict, 'df_rec':df_rec, 'avg':avg, 'std':sd, 'stat':user_stat, 'out_high':out_high, 'out_low':out_low, 'hist_fig':hist_fig, 'weight_fig':weight_fig,'height_fig':height_fig, "player_exists":player_exists, "run_time":run_time*(10**6)}

    return render(request, 'combine/combine.html', context)
