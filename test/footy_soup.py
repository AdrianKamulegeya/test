#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests

txt = u'http://dbpedia.org/data/David_Witteveen__10'
other_txt = u'http://dbpedia.org/resource/David_Witteveen__10'
data = requests.get(txt + '.json').json()
messi = data[other_txt]

height = messi['http://dbpedia.org/ontology/numberOfGoals']

for h in height:
    print h['value']
print height












