import pathlib
import pandas as pd
import plotly
import plotly.express as px
from operator import itemgetter
from nfl_site.libraries import csv_to_dict, mean


# create Dictionary to quickly look up player names
def create_id_name_lookup():
    pid_list = player_dict['playerId']

    lookup_dict = {}

    for i in range(len(pid_list)):
        lookup_dict[pid_list[i]] = player_dict['nameFull'][i]

    return lookup_dict


# returns a list of ids associated with a name in the players.csv
def get_player_id(firstname, lastname):
    # get columns of values
    list1 = player_dict['nameFirst']
    list2 = player_dict['nameLast']

    id_list = []  # list to hold player ids

    fullname = firstname + ' ' + lastname

    # if column length is not the same there is a problem with data
    if len(list1) == len(list1):
        # iterate through first and last name columns
        for i in range(len(list2)):
            list_name = list1[i] + ' ' + list2[i]
            # if name is found add id to list
            if fullname == list_name:
                player_id = player_dict['playerId'][i]
                id_list.append(player_id)

        # return list of ids
        return id_list
    else:
        print('Error: Mismatched column length')
        return None


# returns count of total receiving yards of a given player id in the receiver.csv
def get_receiving_yards(player_id):
    pid_list = receiver_dict['playerId']
    total_rec_yards = 0

    for i in range(len(pid_list)):
        if pid_list[i] == player_id:
            if receiver_dict['rec'][i] == '1' and receiver_dict['recPassInt'][i] == '0' \
                    and receiver_dict['recNull'][i] == '0':
                cell_val = receiver_dict['recYards'][i]  # get value contained in cell of recYards column
                # check to make sure cell does not contain the None data type to prevent addition errors
                if cell_val:
                    total_rec_yards += int(cell_val)

    return total_rec_yards


# gets receiving yard for players of a given name
# returns a dictionary of key(player id, player name)
# and value (total rec yards, avg rec yards per play, total rec plays)
def get_rec_yards_dict(firstname, lastname):
    player_ids = get_player_id(firstname, lastname)  # this is a list of player ids that match name
    full_name = firstname + ' ' + lastname
    if not player_ids:
        # if list returned by get_player_id is empty name does not exist in dataset
        # return empty dictionary
        return {}
    else:
        temp_dict = {}
        # if list returned by get_player_id is not empty get total rec yards for each id
        for pid in player_ids:
            total_yards = get_receiving_yards(pid)

            # create key to get rec plays from prp dictionary
            # tup_key = (pid, firstname + ' ' + lastname)

            if pid in rec_plays_count_dict.keys():

                temp_dict[pid] = [full_name, str(total_yards),
                                  str(float(total_yards) / float(rec_plays_count_dict[pid])),
                                  rec_plays_count_dict[pid]]
            else:
                temp_dict[pid] = [full_name, str(total_yards), '0.0', 0]

        return temp_dict


# gets the top n players by receiving dictionary
# returns a dictionary with key(player id, player name)
# and value (total rec yards, avg rec yards per play, total rec plays)
def top_n_rec_yards(num):

    pid_list = receiver_dict['playerId']
    total_rec_dict = {}
    total_avg_rec_dict = {}

    for i in range(len(pid_list)):
        if receiver_dict['rec'][i] == '1' and receiver_dict['recPassInt'][i] == '0' \
                and receiver_dict['recNull'][i] == '0':
            cell_val = receiver_dict['recYards'][i]  # get value contained in cell of recYards column
            # check to make sure cell does not contain the None data type to prevent addition errors
            if cell_val:
                # create key for dictionary which is a tuple containing player id and full name
                tup_key = (pid_list[i], player_id_name_lookup[pid_list[i]])
                # if tuple key containing player id and full name does not exisis in dictionary create a new
                # entry else add to the total rec yards
                if tup_key not in total_rec_dict:
                    total_rec_dict[tup_key] = int(cell_val)
                else:
                    total_rec_dict[tup_key] += int(cell_val)

    # sort dictionary by total rec yards in descending order
    # Note: this returns a list not a dictionary
    rec_yards_desc = sorted(total_rec_dict.items(), key=itemgetter(1), reverse=True)
    # get the top n records from list and cast into a dictionary
    n_records = dict(rec_yards_desc[:num])

    # create dictionary containing keys (player id, player name)
    # and values (receiving yards, avg receiving yards per play, and total plays)
    for key, val in n_records.items():

        pid = key[0]

        if pid in rec_plays_count_dict.keys():
            total_avg_rec_dict[key] = (val, float(val) / float(rec_plays_count_dict[pid]), rec_plays_count_dict[pid])
        else:
            total_avg_rec_dict[key] = (val, 0.0, 0.0)

    return total_avg_rec_dict


# get total receiving plays for players in receiver.csv
# returns a dictionary of key(player id, player name) and value total receiving plays
def player_rec_plays():
    pid_list = receiver_dict['playerId']
    rec_plays_dict = {}

    for i in range(len(pid_list)):

        if pid_list[i] in player_id_name_lookup.keys():
            dict_key = pid_list[i]
            # if tuple key containing player id and full name does not exist in dictionary create a new
            # entry else add to the rec plays
            if dict_key not in rec_plays_dict:
                rec_plays_dict[dict_key] = 1
            else:
                rec_plays_dict[dict_key] += 1

    return rec_plays_dict


# returns plotly div object given dictionary styled in same manner as out put of receiving functions
def avg_rec_yard_scatter(data_dict):
    df_dict = {'player_id': [], 'player_name': [], 'rec_plays': [], 'rec_yards_avg': []}

    # convert dictionary into a dictionary that is formatted for better conversion into pandas data frame
    for key, val in data_dict.items():
        df_dict['player_id'].append(key[0])
        df_dict['player_name'].append(key[1])
        df_dict['rec_plays'].append(val[2])
        df_dict['rec_yards_avg'].append(val[1])

    data_df = pd.DataFrame.from_dict(df_dict)

    # mean function is function created by Team member Ford.
    # DOES NOT USE PANDAS BUILT IN FUNCTION!!!
    df_mean = mean(data_df, 'rec_yards_avg')

    # Create and return plotly div object
    fig = px.scatter(data_df, x='rec_yards_avg', y='rec_plays', hover_name='player_name',
                     labels={
                         'rec_yards_avg': 'Average Receiving Yards Per Play (ARYPP)',
                         'rec_plays': 'Total Receiving Plays'
                     },
                     title='Total Receiving Plays vs Average Receiving Yards Per Play (ARYPP)')
    fig.add_vline(df_mean, line_dash='dash', annotation_text="Overall ARYPP: " + str(df_mean),
                  annotation_position="top right", line_color='green')
    graph_div = plotly.offline.plot(fig, output_type="div")

    return graph_div


# add a receiving play to the receiver_dict data store
def add_receiver_data(player_id, position, rec_yards):

    global rec_plays_count_dict

    data_dict = {'receiverId': '99999999', 'playId': '99999999', 'teamId': '99999999',
                 'playerId': player_id, 'recPosition': position, 'recYards': rec_yards,
                 'rec': '1', 'recYac': '0', 'rec1down': '0', 'recFumble': '0',
                 'recPassDef': '0', 'recPassInt': '0', 'recEnd': '0', 'recNull': '0'}

    # inserting data
    for key in receiver_dict.keys():
        receiver_dict[key].append(data_dict[key])

    # increment the receiving plays count of the player who had a receiving play record added
    # of player not in count dictionary add them
    if player_id in rec_plays_count_dict:
        rec_plays_count_dict[player_id] += 1
    else:
        rec_plays_count_dict[player_id] = 1


# add a receiving play to the receiver_dict data store, checks for player existence
# player exists returns true, if player dose not exist returns false
def add_existing_receiver_data(player_id, position, rec_yards):

    if player_id in player_dict['playerId']:

        add_receiver_data(player_id, position, rec_yards)

        return True

    return False


# returns the max player id value in data set
def get_max_player_id():

    pid_list_string = player_dict['playerId']

    # convert player id's from strings to ints
    pid_list = [int(i) for i in pid_list_string]

    max_val = max(pid_list)  # get max id value

    return max_val


# add a new player and return their newly generated player id
def add_player(firstname, lastname, position):

    global player_id_name_lookup

    new_pid = str(get_max_player_id() + 1)  # get a new player id for new player
    full_name = firstname + ' ' + lastname

    data_dict = {'playerId': new_pid, 'nameFirst': firstname, 'nameLast': lastname,
                 'nameFull': full_name, 'position': position, 'collegeId': '555555',
                 'nflId': '555555', 'combineId': '555555', 'college': 'UC', 'heightInches': '74',
                 'weight': '246', 'dob': '2020-14-11', 'ageAtDraft': '20', 'playerProfileUrl': 'https://www.nfl.com/',
                 'homeCity': 'Earth', 'homeState': 'Earth', 'homeCountry': 'Earth', 'highSchool': 'HS',
                 'hsCity': 'Earth', 'hsState': 'Earth', 'hsCountry': 'Earth'}

    # inserting new player data
    for key in player_dict.keys():
        player_dict[key].append(data_dict[key])

    # add new player to the id name look up dictionary
    player_id_name_lookup[new_pid] = full_name

    return new_pid


# function returns list of all indices a value is found at in a list
def find_index(value, val_list):
    index_list = []

    for i, j in enumerate(val_list):
        if j == value:
            index_list.append(i)

    return index_list


# remove player from players.csv data
def remove_from_player_csv(index_list):

    # delete all occurrences of player in players.csv data
    for i in index_list:
        for key in player_dict.keys():
            player_dict[key].pop(i)


# remove player from receiver.csv data
def remove_from_receiver_csv(index_list):
    # sort the list to delete indices from largest to smallest
    index_list = sorted(index_list, reverse=True)

    # delete all occurrences of player in receiver.csv data
    for i in index_list:
        for key in receiver_dict.keys():
            receiver_dict[key].pop(i)


# function deletes player form data store, returns tuple with success boolean and name of deleted player
def delete_player(player_id):
    global player_id_name_lookup
    global rec_plays_count_dict

    name_deleted = ''

    player_csv_pd_list = player_dict['playerId']  # list of player ids in player.csv
    receiver_csv_pid_list = receiver_dict['playerId']  # list of player ids in receiver.csv

    if player_id not in player_csv_pd_list:
        # if player does not exist there is nothing to delete
        return False, name_deleted
    else:

        # get indices of all player occurrences in the players.csv and receiver.csv data
        player_index_list = find_index(player_id, player_csv_pd_list)
        receiver_index_list = find_index(player_id, receiver_csv_pid_list)

        # remove player from players.csv and receiver.csv data
        remove_from_player_csv(player_index_list)
        remove_from_receiver_csv(receiver_index_list)

        # delete player from id name look up table and receiving plays count dictionary
        if player_id in player_id_name_lookup.keys():
            name_deleted = player_id_name_lookup.pop(player_id)

        if player_id in rec_plays_count_dict.keys():
            rec_plays_count_dict.pop(player_id)

        return True, name_deleted


# dictionaries that need to be loaded prior to running above functions
# these should remain at the end of the file
if pathlib.Path('static/archive/').exists():

    player_dict = csv_to_dict("static/archive/players.csv")
    receiver_dict = csv_to_dict("static/archive/receiver.csv")
    player_id_name_lookup = create_id_name_lookup()  # dictionary that can get player name given id
    rec_plays_count_dict = player_rec_plays()  # get dictionary containing players and their total receiving plays
