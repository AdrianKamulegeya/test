# -*- coding: utf-8 -*-

import requests
from clubfilehandler import ClubFileHandler

txt_files = ['prem.txt', 'la_liga.txt', 'bundesliga.txt', 'ligue_1.txt', 'serie_a.txt']
fields = ["club", "ground", "capacity", "manager", "chairman"]

handler = ClubFileHandler("club2.csv", fields)
writer = handler.get_csv_writer()
writer.writeheader()

for f in txt_files:
    club_file = open(f, "r")
    for club in club_file.readlines():
        try:
            club = club.replace("\n", "")
            data = requests.get('http://dbpedia.org/data/' + club + '.json').json()
            info = data['http://dbpedia.org/resource/' + club]

            capacity = info['http://dbpedia.org/ontology/capacity'][0]['value']
            capacity = handler.format_data(capacity)
            ground = info['http://dbpedia.org/ontology/ground'][0]['value']
            ground = handler.format_data(ground)
            manager = info['http://dbpedia.org/ontology/manager'][0]['value']
            manager = handler.format_data(manager)
            chairman = info['http://dbpedia.org/ontology/chairman'][0]['value']
            chairman = handler.format_data(chairman)

            club = club.replace("_", " ")
            writer.writerow({'club': club, 'ground': ground, 'capacity': capacity,
                             'manager': manager, 'chairman': chairman})
        except KeyError:
           # soup = FootySoup(club)
            #soup_data = soup.getData()
            #print soup_data
            club = club.replace("_", " ")
            writer.writerow({'club': club, 'ground': '', 'capacity': '',
                             'manager': '', 'chairman': ''})



handler.close_file()
