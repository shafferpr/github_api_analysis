#! /usr/local/bin/python

import os
import sys
import string
import requests
import json
import numpy as np
import math
from bokeh.plotting import figure, output_file, show
from dateutil.parser import parse

def createDateTimeFigure(repoString):
    payload = {}

    r=requests.get('https://api.github.com/repos/'+repoString+'/commits', auth=('shafferpr@gmail.com','chem1633'), params=payload)

    myList = []

    for i in range (len(r.json())):
        myList.append(r.json()[i]['sha'])

        q=[]
    for i in range (len(myList)):
        q.append(requests.get('https://api.github.com/repos/'+repoString+'/commits/'+myList[i],auth=('shafferpr@gmail.com','chem1633'), params=payload))

    x=[]

    for i in range(len(q)):
        x.append(parse(q[i].json()['commit']['author']['date']))

    y=[]

    for i in range(len(q)):
        y.append(q[i].json()['stats']['total'])

    output_file("./static/plot.html")

    p = figure(title="commit size over time", x_axis_label='date of commit', y_axis_label='size of commit', x_axis_type="datetime")

    p.line(x, y, legend=repoString, line_width=2, line_color="blue")

    show(p)

createDateTimeFigure("tensorflow/tensorflow")
