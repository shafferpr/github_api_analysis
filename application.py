from flask import Flask,render_template,request,redirect
from github_analysis import createDateTimeFigure
from bokeh.embed import components
from github_analysis2 import create_connection_dictionary

app = Flask(__name__)

app.vars={}

@app.route('/',methods=['GET','POST'])
def index():
    # this is a comment, just like in Python
    # note that the function name and the route argument
    # do not need to be the same.
    if request.method == 'GET':
        #return render_template('homepage.html')
        script = create_connection_dictionary()
        return render_template('index.html', script=script)
    else:
        #request was a post
        app.vars['repository']=request.form['repository']
        plot = createDateTimeFigure(app.vars['repository'])
        script, div = components(plot)
        return render_template('1st.html', script=script, div=div)
    #return redirect('/next')
    #return render_template('layout_lulu.html', num=1,question='How many eyes do you have?', ans1='1',ans2='2',ans3='3')




@app.route('/next',methods=['GET','POST'])
def next():
    if request.method == 'GET':
        return render_template('1st.html', script=script, div=div)
    else:
        return redirect('/next2')

@app.route('/next2',methods=['GET'])
def next6():
    if request.method == 'GET':
        return render_template('end.html')

#################
## Important: I have separated /next_lulu into GET and POST
## you can also do this in one function with IF and Else
## the attribute that contains GET and POST is request.method
###################


#@app.route('/usefulfunction_lulu',methods=['GET','POST'])
#def usefulfunction_lulu():
#    return render_template('end_lulu.html')
#return render_template('layout_lulu.html',num=1,question='Which fruit do you like best?',ans1='banana',ans2='mango',ans3='pineapple')

if __name__ == '__main__':
    app.run()
