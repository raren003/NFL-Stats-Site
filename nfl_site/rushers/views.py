from django.shortcuts import render
import pandas as pd
from .forms import RushersForm , TeamPickForm
from .nfldata import get_player_df,get_rusher_yards_dic,get_top_rushers_df, create_ALL_TIME_context, getImageLinks , deletePlayer, get_AVG_of_top_df, getFullTeamName, getTeamImage
from .nfldata import getFirstValue, get_top_rushing_team, get_top_team

import plotly
import plotly.graph_objs as go
import plotly.express as px 
import datetime

def rusher_page(request):
    
    # store players id and rushing yards
    player_dict = {}  
    context = {}
    first_name = ''
    last_name = ''
    outputDataFrame = pd.DataFrame()
    exists = None
    player_img = ''
    deletable = False

    submitbutton = request.POST.get("Search")
    team_submit = request.POST.get("Team Picker")
    show_graph_button = request.POST.get("Show Graph")
    delete_button = request.POST.get("Delete Player")

    #check if name form has been clicked or not
    form = RushersForm()
    #check if team name form has been clicked or not
    team_form = TeamPickForm()

    if(submitbutton == 'Search' or delete_button == 'Delete Player'):
        form = RushersForm(request.POST)
        if form.is_valid():
            player_dict.clear()  # clear info from previous search
            first_name = form.cleaned_data.get("first_name")  # get player first name from form
            last_name = form.cleaned_data.get("last_name") # get player last name from form
            # filter out players based on the name entered

            if(delete_button == 'Delete Player'):
                deletePlayer(first_name,last_name)

            outputDataFrame = get_player_df(first_name,last_name)

            # if dictionary is empty player does not exist in data frame
            # prepare display message indicating so
            if outputDataFrame.empty:
                first_name = "Player Does Not Exist"
                last_name = "In Data Set!"
                exists = 0
            else:
                player_img =  getImageLinks(first_name,last_name)
                deletable = True
            context = {'form': form, 'team_form':team_form, 'first_name': first_name, 'last_name':last_name, 
            'submit_button': submitbutton,  'columns' : outputDataFrame.columns, 'output':outputDataFrame,
            'exists':exists, 'player_img':player_img, 'deletable':deletable}       
    
    if (team_submit == 'Team Picker' or show_graph_button == 'Show Graph'):
        team_form = TeamPickForm(request.POST)
        if team_form.is_valid():
            #get team abbreviation and convert it to full team name
            team_name  = team_form.cleaned_data.get('team_name')
                
            a = datetime.datetime.now()

            #dictionary of player id to their yards
            rusher_dic = get_rusher_yards_dic(team_name) 

            if team_name != 'all time':
                team_name = getFullTeamName(team_name)
                team_img = getTeamImage(team_name)
            else:
                team_img = "https://www.freepnglogos.com/uploads/nfl-logo-png-0.png"


            #getting the top 20 rushers [player id] = [total rush yards] 
            #Reverse ordered because we want top players first
            top_rushers = dict(sorted(rusher_dic.items(), key = lambda kv:(kv[1], kv[0]),reverse=True)[:20])
            outputDataFrame = get_top_rushers_df(top_rushers)
            exists = 1
            total_avg_yards = get_AVG_of_top_df(outputDataFrame)
            context = create_ALL_TIME_context(form,team_form,team_submit,show_graph_button, outputDataFrame,exists,team_name,total_avg_yards)
            context['team_img'] = team_img

            context['top_rusher'] = getFirstValue(outputDataFrame)
            context['top_rushing_team'] = get_top_rushing_team(outputDataFrame)
            context['top_team'] = get_top_team()


            
            b = datetime.datetime.now()
            t_time = b - a
            context['t_time'] = t_time



            if(show_graph_button == 'Show Graph'):
                results = outputDataFrame[['Rush Yards','Total Plays']]
                fig = px.scatter(results, x="Rush Yards", y="Total Plays", title="Total Rushing Yards per Play")
                graph_div = plotly.offline.plot(fig, output_type="div")
                context['graph_div'] = graph_div

    if not context:
        context = {'form': form, 'team_form': team_form}

    return render(request, 'rushers/rusher.html', context)
