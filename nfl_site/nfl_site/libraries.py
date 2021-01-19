'''
Author: FSt. J
Comments: We'll use this .py file to maintain all of our user-defined functions for the project
          Note that functions within this code can be called using the following syntax
          from nfl_site.nfl_site.libraries import <my_function1>, <my_function2>, ... : for specific functions OR
          from nfl_site.nfl_site.libraries import * : for all functions
'''

'''
Author: FSt.J
Comments: Global function to convert  heigh in decimal inches to cleaner view
'''
import pandas as pd
#for getting image from .html
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re


def conv_height(h):
    ft = int(divmod(h,12)[0])
    inch = round(int(divmod(h,12)[1]),0)
    if h == 0 or h == "" or h == " ":
        return ""
    else:
        return str(ft)+"'"+str(inch)+"\""

# For getting the record number or index of a certain record in a data frame
# params: ( dataframe, value of row to take out) e.g: (players, playerID)
def getIndexes(dfObj, value):
    ''' Get index positions of value in dataframe i.e. dfObj.'''
    listOfPos = list()
    # Get bool dataframe with True at positions where the given value exists
    result = dfObj.isin([value])
    # Get list of columns that contains the value
    seriesObj = result.any()
    columnNames = list(seriesObj[seriesObj == True].index)
    # Iterate over list of columns and fetch the rows indexes where value exists
    for col in columnNames:
        rows = list(result[col][result[col] == True].index)
        for row in rows:
            listOfPos.append((row, col))
    # Return a list of tuples indicating the positions of value in the dataframe
    return listOfPos



# ================== Below are functions that are used by the Rushers site ==================
# import pathlib

# def readPlayers():
#     if not pathlib.Path('static/archive/').exists():
#         return
#     return pd.read_csv("static/archive/players.csv")

# def readRushers():
#     if not pathlib.Path('static/archive/').exists():
#         return
#     return pd.read_csv("static/archive/rusher.csv")

# def readTeams():
#     if not pathlib.Path('static/archive/').exists():
#         return
#     df = pd.read_csv("static/archive/draft.csv")
#     team_df = df[['teamId','draftTeam']].drop_duplicates()
#     return team_df

# df_rusher = readRushers()
# df_teams = readTeams()

# def get_Tuple(df_players,first_name,last_name):
#     name_filter = df_players.loc[(df_players['nameFirst'] == first_name) & (df_players['nameLast'] == last_name)]
#     if len(name_filter) == 0:
#         # if player does not exist set tuple to false and empty string
#         return False, []
#     else:
#         # if player does exist return list of id's of all players with the same name
#         player_id_list = name_filter['playerId'].tolist()
#         return True, player_id_list



# def getPlayerTeam(player_id):
#     filter_df = df_rusher.loc[(df_rusher['playerId'] == player_id)]
#     get_team = filter_df['teamId'].drop_duplicates().tolist()
#     return get_team

# def getTeamName(team_id):
#     team_names = []
#     for i in team_id:
#         team_name = df_teams[df_teams['teamId'] == i]['draftTeam'].unique().tolist()
#         team_names.append(team_name)
#     return team_names

# def get_player_dict(df_players, first_name, last_name, df_rusher):
#     player_dict = {} 
#     outputDataFrame = pd.DataFrame() 
#     player_tuple = get_Tuple(df_players,first_name, last_name)

#     if not player_tuple[0]:
#         # if first value in the tuple is false the name entered does not exist in data set
#         # return empty dict
#         return outputDataFrame
#     else:
#         # for each player id in the player id list (the second value in temp tup) find all occuences of the player
#         # id in the receiver csv
#         for player_id in player_tuple[1]:
#             print(player_id)
#             # get all rusher yards for playerId as long as they exist and were not overturned
#             rushers_filter \
#                 = df_rusher.loc[(df_rusher['playerId'] == player_id) & (df_rusher['rushNull'] == 0)]
#             # sum the rushYards row of the data frame
#             total_rush_yards = rushers_filter['rushYards'].sum()

#             player_dict[player_id] = int(total_rush_yards)
#             player_team_id = getPlayerTeam(player_id) #list of teams player 
#             player_team = getTeamName(player_team_id) 
#             print(player_team)
#             outputDataFrame = outputDataFrame.append([[first_name,last_name,player_id,player_dict[player_id],player_team]])
        
#         outputDataFrame.columns = ['First Name', 'Last Name', 'Player ID','Rush Yards','Team(s)']
#         return outputDataFrame


# # function to get a rushers yards in the dictionary 
# def get_rushers_yards(dic , rusher_id):
#     for key,value in dic.items():
#         if key == rusher_id:
#             return value

# def get_name(df_players, player_id):
#     player_df = df_players.loc[(df_players['playerId'] == player_id)].drop_duplicates()
#     first_name = player_df["nameFirst"].values
#     last_name = player_df["nameLast"].values
#     # we use first_name[0] becuase the name is "['Tom'] "", this makes it just "Tom"
#     # i think this is due it being an array 
#     full_name = [first_name[0],last_name[0]]
#     return full_name

# # function to get rushers dictionary {player id} = {total yards they have}
# def get_rusher_yards_dic(df_rusher):
#     total_rusher_dic = {}
#     all_rushers = df_rusher[["playerId","rushYards","rushNull"]]
#     player_id = all_rushers[["playerId"]].drop_duplicates().values.tolist()

#     for id in player_id:
#         rushers_filter = all_rushers.loc[(all_rushers['playerId'] == id[0]) & (all_rushers['rushNull'] == 0)]
#         total_yards = rushers_filter['rushYards'].sum()
#         total_rusher_dic.update({id[0]:total_yards})

#     return total_rusher_dic

# def get_top_rushers_df(df_players,top_rushers):
#     outputDataFrame = pd.DataFrame()
#     rank = 0

#     for id in top_rushers:
#         full_name = get_name(df_players,id)
#         first_name = full_name[0]
#         last_name = full_name[1]
#         rusher_total_yds = int(get_rushers_yards(top_rushers,id))
#         player_team_id = getPlayerTeam(id)
#         player_team = getTeamName(player_team_id) 
#         rank = rank + 1
#         outputDataFrame = outputDataFrame.append([[rank,first_name,last_name,id,rusher_total_yds,player_team]])
    
#     outputDataFrame.columns = ['Rank','First Name', 'Last Name', 'Player ID','Rush Yards','Team(s)']
#     print(outputDataFrame)
#     return outputDataFrame

# def create_ALL_TIME_context(form,team_form,team_submit,outputDataFrame,exists):
#     context = {'form': form, 'team_form': team_form,'team_submit': team_submit,'columns' : outputDataFrame.columns, 'output':outputDataFrame,
#     'exists':exists}
#     return context


# def getImageLinks(first_name,last_name):
#     site ='https://www.nfl.com/players/'+str(first_name)+'-'+str(last_name)+'/'
#     substr = 'https://static.www.nfl.com/image/private/t_player_profile_landscape/'
#     html = urlopen(site)
#     bs = BeautifulSoup(html, 'html.parser')
#     full_name = str(first_name)+' '+str(last_name)
#     images = bs.find_all('img', {"alt": full_name })
#     pathToImage = ''
#     for image in images:
#         url = image['src']
#         if substr in url:
#             pathToImage = url.replace('t_lazy/','')
#             print(pathToImage)
#     return pathToImage

# ================== Above are functions that are used by the Rushers site ==================
'''
Author: FSt.J
Comments: Moving Rob's read_csv code to libraries.py for import around our application
'''
import re
import pandas as pd
def csv_to_dict(file_name, to_df = 0):
    # regex to get data from each line of the csv file
    row_regex = re.compile(r'(?:,|\n|^)("(?:(?:"")*[^"]*)*"|[^",\n]*|(?:\n|$))')

    csv_dict = {}  # dictionary to contain all the columns of a csv file
    misses = 0  # count how many records in a file where not extractable

    with open(file_name) as f:

        line = f.readline()  # read in fist line that should contain csv headers

        # get the headers of the csv file from first line using regex
        csv_headers = row_regex.findall(line.strip())

        lines = f.readlines()  # get all lines after the header line in the csv

    # create dictionary of arrays with csv headers (column names) as keys
    for header in csv_headers:
        csv_dict[header] = []

    # loop through each line extracted from the csv and get data
    for line in lines:
        counter = 0  # counter to cycle through values extracted from a line
        temp_list = row_regex.findall(line.strip())  # grab all values for a line

        # in the number of values extracted from the line is equal to the number of csv headers (columns)
        # data is valid and can be added to csv dictionary
        if len(csv_headers) == len(temp_list):
            for header in csv_headers:
                # if the value in a field was not empty add it to proper column else insert None
                if temp_list[counter]:
                    csv_dict[header].append(temp_list[counter])
                else:
                    csv_dict[header].append(None)
                counter += 1
        else:
            # increment counter to indicate that a line could not be added to csv dictionary
            misses += 1

    print('missed rows (' + file_name + '): ', misses)

    if to_df:
        return pd.DataFrame(csv_dict)
    else:
        return csv_dict

'''
Author: FSt.J
Comments: custom "average" calculation that takes in a Pandas DataFrame and a named column, and computes the average from scratch
'''
import math # to access isnan function
import numpy as np

def sumf(df, column):
    ret = 0
    for x in df[column]:
        if not math.isnan(x):
            ret += x
    return ret

def mean(df, column):
    ret = 0
    counter = 0
    for x in df[column]:
        if not math.isnan(x):
            counter += 1
            ret = ret + x
    if counter > 0:
        return ret / counter
    else:
        return math.nan # If can't compute avg, return NaN

'''
Author: FSt.J
Comments: custom "standard deviation" calculation that takes in a Pandas DataFrame and named column, and computes the std. dev. from scratch
'''
def stddev(df, column):
    avg = mean(df, column)
    if sum(1 if not np.isnan(x) else 0 for x in df[column]):
        variance = sum([(x - avg)**2 for x in df[column] if not np.isnan(x)]) / sum(1 if not np.isnan(x) else 0 for x in df[column])
    else:
        return math.nan
    return math.sqrt(variance)

