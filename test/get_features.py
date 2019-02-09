#!/usr/bin/python
# encoding=utf8
import requests
import csv
import pickle
from clubfilehandler import ClubFileHandler
from datetime import date


def collect_info():
    with open('uris.csv', "r") as csv_file, \
            open('transfer_tup.pickle', 'wb') as trans_handle, \
            open('player_tup.pickle', 'wb') as player_handle, \
            open('club_tup.pickle', 'wb') as club_handle:
        reader = csv.reader(csv_file)
        for row in reader:
            player_uri = row[0].decode('utf-8')
            club_uri = row[1].decode('utf-8')
            print(player_uri)
            print(club_uri)
            if player_uri not in player_list:
                player_list.append(player_uri)
                get_player_details(player_uri, player_handle)
            if club_uri not in club_list:
                club_list.append(club_uri)
                get_club_details(club_uri, club_handle)
            transfer_happened = did_transfer_happen(player_uri, club_uri)
            print("TRANSFER HAPPENED = " + str(transfer_happened))
            print("------------------------------------------------------------------------------------------")

            transfer_data = {'player': get_name(player_uri),
                             'rumoured_club': get_name(club_uri),
                             'successful': transfer_happened}

            pickle.dump(transfer_data, trans_handle, protocol=pickle.HIGHEST_PROTOCOL)

        csv_file.close()
        trans_handle.close()
        player_handle.close()
        club_handle.close()


def get_data(txt):
    formatted_text = txt.replace('resource', 'data')
    formatted_text = formatted_text.replace('&', '%26')
    formatted_text = formatted_text + ".json"
    return requests.get(formatted_text).json()


def get_dictionary(data, txt):
    return data[txt]


def get_player_details(uri, handle):
    data = get_data(uri)
    player_dict = get_dictionary(data, uri)
    career_stations = get_career_stations(player_dict)
    name = get_name(uri)
    height = get_height(player_dict)
    position = get_position(player_dict)
    age = get_age(player_dict)
    goals = get_no_of_goals(career_stations)
    apps = get_appearances(career_stations)
    teams_played_for = get_teams_played_for(player_dict)
    print("NAME: " + name + ", POSITION: " + position + ", AGE: " + str(age) +
          ", GOALS: " + str(goals) + ", APPS: " + str(apps) + ", HEIGHT: " + str(height))

    player_data = {'player': name,
                   'uri': uri,
                   'position': position,
                   'age': age,
                   'teams_played_for': teams_played_for,
                   'goals': goals,
                   'apps': apps,
                   'height': height}

    pickle.dump(player_data, handle, protocol=pickle.HIGHEST_PROTOCOL)


def get_club_details(uri, handle):
    data = get_data(uri)
    club_dict = get_dictionary(data, uri)
    name = get_name(uri)
    manager = get_club_manager(club_dict)
    ground = get_ground(club_dict)
    capacity = get_capacity(club_dict)
    chairman = get_chairman(club_dict)

    player_data = {'club': name,
                   'uri': uri,
                   'manager': manager,
                   'ground': ground,
                   'capacity': capacity,
                   'chairman': chairman}

    pickle.dump(player_data, handle, protocol=pickle.HIGHEST_PROTOCOL)


def did_transfer_happen(player, club):
    player_data = get_data(player)
    player_dict = get_dictionary(player_data, player)
    teams = get_teams_played_for(player_dict)
    rumoured_team = get_name(club)
    print("RUMOURED: " + rumoured_team)
    for team in teams:
        if rumoured_team == team:
            return True

    return False


def get_name(uri):
    return uri.split('/')[4].replace('_', ' ').encode('utf-8')


def get_club_manager(reference):
    try:
        return reference['http://dbpedia.org/ontology/manager'][0]['value'].split('/')[4]\
            .replace("_", " ").encode('utf-8')
    except KeyError:
        print("no club manager field found")
        return "NONE"


def get_clubs_managed(reference):
    try:
        teams_uri = reference['http://dbpedia.org/ontology/managerClub']
        teams = []
        for uri in teams_uri:
            if uri['value'] != 'http://www.njsa04.com':
                teams.append(get_name(uri['value']))
        return teams
    except KeyError:
        print("no teams fields found")
        return []


def get_ground(reference):
    try:
        return reference['http://dbpedia.org/ontology/ground'][0]['value'].split('/')[4].replace("_", " ")\
            .replace(" (stadium)", "").encode('utf-8')
    except KeyError:
        print("no ground field found")
        return "NONE"


def get_capacity(reference):
    try:
        return reference['http://dbpedia.org/ontology/capacity'][0]['value'].encode('utf-8')
    except KeyError:
        print("no capacity field found")
        return 0


def get_chairman(reference):
    try:
        return reference['http://dbpedia.org/ontology/chairman'][0]['value'].split('/')[4].replace("_", " ")\
            .replace(" (businessman)", "")
    except KeyError:
        print("no chairman field found")
        return "NONE"


def get_height(reference):
    try:
        return reference['http://dbpedia.org/ontology/height'][0]['value']
    except KeyError:
        print("no height field found")
        return 0


def get_age(reference):
    try:
        birth_date = reference['http://dbpedia.org/ontology/birthDate'][0]['value']
        date_fields = birth_date.split('-')
        birth_year = int(date_fields[0])
        birth_month = int(date_fields[1])
        birth_day = int(date_fields[2])
        today = date.today()
        return today.year - birth_year - ((today.month, today.day) < (birth_month, birth_day))
    except KeyError:
        print("no age field found")
        return 0


def get_teams_played_for(reference):
    try:
        teams_uri = reference['http://dbpedia.org/ontology/team']
        teams = ()
        for uri in teams_uri:
            if uri['value'] != 'http://www.njsa04.com':
                teams += (get_name(uri['value']),)
        return teams
    except KeyError:
        print("no teams fields found")
        return []


def get_position(reference):
    try:
        return reference['http://dbpedia.org/ontology/position'][0]['value'].split('/')[4].encode('utf-8')\
            .replace("_(association_football)", "").replace("_(football)", "")
    except KeyError:
        print("no position field found")
        return "NONE"


def get_career_stations(reference):
    try:
        return reference['http://dbpedia.org/ontology/careerStation']
    except KeyError:
        print("no career stations field found")
        return {}


def get_no_of_goals(career_stations):
    no_of_goals = 0
    try:
        for station in career_stations:
            try:
                request_text = station['value'].replace('resource', 'data')
                request_text = request_text + ".json"
                data = requests.get(request_text).json()
                player = data[station['value']]
                no_of_goals += player['http://dbpedia.org/ontology/numberOfGoals'][0]['value']
            except KeyError:
                print("no goals in that year")
    except KeyError:
        print("no goals field found")
    print(no_of_goals)
    return no_of_goals


def get_appearances(career_stations):
    no_of_apps = 0
    try:
        for station in career_stations:
            try:
                request_text = station['value'].replace('resource', 'data')
                request_text = request_text + ".json"
                data = requests.get(request_text).json()
                player = data[station['value']]
                no_of_apps += player['http://dbpedia.org/ontology/numberOfMatches'][0]['value']
            except KeyError:
                print("no apps that year")
    except KeyError:
        print("no apps field found")
    print(no_of_apps)
    return no_of_apps


player_fields = ["player", "position", "age", "goals", "apps", "height"]
club_fields = ["club", "manager", "ground", "capacity", "chairman"]
transfer_fields = ["player", "rumoured_club", "successful"]
player_list = []
club_list = []
collect_info()
