import json
import requests
import os
import pandas as pd
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

token=os.environ['github_auth_token']

def create_connection_dictionary(org):
    #qu_string= ' query{ organization(login: "'+org+'") { repositories(first: 5, orderBy: {field: CREATED_AT, direction: DESC}) { edges{ node{ name mentionableUsers(first: 5) { edges { node { contributedRepositories(first: 5){ edges{ node{ name } } } } } } } } } } } '
    qu_string= ''' query{
                    organization(login: "%s") {
                         repositories(first: 5, orderBy: {field: CREATED_AT, direction: DESC}) {
                          edges{
                           node{
                            name mentionableUsers(first: 5) {
                             edges {
                              node {
                               contributedRepositories(first: 5){
                                edges{
                                 node{
                                  name
                                 }
                                }
                               }
                              }
                             }
                            }
                           }
                          }
                         }
                        }
                      } ''' %(org)
    print (qu_string)
    data={"query" : qu_string}

    r=requests.post('https://api.github.com/graphql', json=data, auth=('shafferpr@gmail.com', 'chem1633'))

    all_data=pd.DataFrame.from_dict(r.json())
    list_temp=all_data['data']['organization']['repositories']['edges']
    listOfNames=[item['node']['name'] for item in list_temp]


    dict1=dict.fromkeys(listOfNames,0)
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

def create_connection_dictionary2(org):
    #qu_string= ' query{ organization(login: "'+org+'") { repositories(first: 5, orderBy: {field: CREATED_AT, direction: DESC}) { edges{ node{ name mentionableUsers(first: 5) { edges { node { contributedRepositories(first: 5){ edges{ node{ name } } } } } } } } } } } '
    qu_string= ''' query{
                    organization(login: "%s") {
                         repositories(first: 15, orderBy: {field: CREATED_AT, direction: DESC}) {
                          edges{
                           node{
                            name
                            mentionableUsers(first: 15) {
                             edges{
                              node{
                               name
                              }
                             }
                            }
                           }
                          }
                         }
                        }
                      } ''' %(org)

    data={"query" : qu_string}

    r=requests.post('https://api.github.com/graphql', json=data, auth=('shafferpr@gmail.com', 'chem1633'))

    all_data=pd.DataFrame.from_dict(r.json())
    list_temp=all_data['data']['organization']['repositories']['edges']
    listOfNames=[item['node']['name'] for item in list_temp]


    dict1=dict.fromkeys(listOfNames,0)
    dict2=dict.fromkeys(listOfNames,dict1)


    for item1 in list_temp:
        name1=item1['node']['name']
        list_tempA= item1['node']['mentionableUsers']['edges']
        list_of_users1=[user['node']['name'] for user in list_tempA]
        set_of_users1=set(list_of_users1)
        for item2 in list_temp:
            name2=item2['node']['name']
            list_tempB= item2['node']['mentionableUsers']['edges']
            list_of_users2=[user['node']['name'] for user in list_tempB]
            set_of_users2=set(list_of_users2)
            inter_sets=set.intersection(set_of_users1, set_of_users2)
            #print(inter_sets)
            dict2[name1][name2]=len(inter_sets)*len(inter_sets)*len(inter_sets)/50.0



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

def create_user_connection_dictionary(org):
    qu_string= ''' query{
                    organization(login: "%s") {
                         members(first: 30) {
                          edges{
                           node{
                            name
                            contributedRepositories(first: 12) {
                             edges{
                              node{
                               name
                              }
                             }
                            }
                           }
                          }
                         }
                        }
                      } ''' %(org)

    data={"query" : qu_string}
    r=requests.post('https://api.github.com/graphql', json=data, auth=('shafferpr@gmail.com', 'chem1633'))
    all_data=pd.DataFrame.from_dict(r.json())
    print(all_data)
    list_temp=all_data['data']['organization']['members']['edges']
    listOfNames=[item['node']['name'] for item in list_temp]

    dict1=dict.fromkeys(listOfNames,0)
    dict2=dict.fromkeys(listOfNames,dict1)

    for item1 in list_temp:
        name1=item1['node']['name']
        list_tempA= item1['node']['contributedRepositories']['edges']
        list_of_repos1=[repo['node']['name'] for repo in list_tempA]
        set_of_repos1=set(list_of_repos1)
        for item2 in list_temp:
            name2=item2['node']['name']
            list_tempB= item2['node']['contributedRepositories']['edges']
            list_of_repos2=[repo['node']['name'] for repo in list_tempB]
            set_of_repos2=set(list_of_repos2)
            inter_sets=set.intersection(set_of_repos1, set_of_repos2)
            #print(inter_sets)
            dict2[name1][name2]=len(inter_sets)*len(inter_sets)/10

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
