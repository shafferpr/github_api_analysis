import json
import requests
import os
import pandas as pd
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

#token=os.environ['github_auth_token']

def create_connection_dictionary():
    qu_string= 'query{ organization(login: "Facebook") { repositories(first: 5, orderBy: {field: CREATED_AT, direction: DESC}) { edges{ node{ name mentionableUsers(first: 10) { edges { node { contributedRepositories(first: 5){ edges{ node{ name } } } } } } } } } } }'
    data={"query" : qu_string}

    r=requests.post('https://api.github.com/graphql', json=data, auth=('shafferpr@gmail.com', 'chem1633'))
    all_data=pd.DataFrame.from_dict(r.json())
    list_temp=all_data['data']['organization']['repositories']['edges']
    listOfNames=[item['node']['name'] for item in list_temp]


    dict1=dict.fromkeys(listOfNames,1)
    dict2=dict.fromkeys(listOfNames,dict1)


    for item in list_temp:
        name1=item['node']['name']
        list_temp2=item['node']['mentionableUsers']['edges']
        for item2 in list_temp2:
            list_temp3=item2['node']['contributedRepositories']['edges']
            for item3 in list_temp3:
                name2 = item3['node']['name']
                if(name2 in listOfNames):
                    dict2[name1][name2] += 1

    links=[]
    nodes=[]
    for key in dict2:
        individual_dictionary1={"id": key, "group" : 1}
        nodes.append(individual_dictionary1)
        for key2 in dict2[key]:
            individual_dictionary2={"source": key, "target": key2, "value": dict2[key][key2]}
            links.append(individual_dictionary2)

    full_dictionary={"nodes": nodes, "links": links}
    with open('./static/connections.json', 'w') as fp:
        json.dump(full_dictionary, fp)
    return json.dumps(full_dictionary)
