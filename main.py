# Importing the required Packages
import json
import pytz
from datetime import datetime, timedelta
import requests
from flask import Flask, render_template,request
from plotly.utils import PlotlyJSONEncoder
from plotly.subplots import make_subplots
import plotly.graph_objects as go

app = Flask(__name__)

@app.route("/",methods=["POST", "GET"])
def data():
    """
    Home Page 
    The result from the api is collected and Tables and Figures are generated 
    """
    if request.method == "GET":
        return render_template('home.html',)
    else:
        option = request.form['TimeZone']
        id = request.form['id']
        error = None
        utc=pytz.UTC
        
        measures = requests.get('https://environment.data.gov.uk/flood-monitoring/id/stations/{}/measures'.format(id))
        measures_one_station = json.loads(measures.text)
        now = utc.localize(datetime.now())
        today = now.strftime('%Y-%m-%d')
        yest = (datetime.now() - timedelta(hours=24)).strftime('%Y-%m-%d')
        if 'past' in option:
            x = requests.get('https://environment.data.gov.uk/flood-monitoring/id/stations/{}/readings?startdate={}&enddate={}'.format(id,yest,today)).text
        else:
            x = requests.get('https://environment.data.gov.uk/flood-monitoring/id/stations/{}/readings?{}'.format(id,option)).text
        measure_set = set()
        x_json = json.loads(x)
        if x_json['items'] :
            for j in measures_one_station['items']:
                measure_set.add(j['notation'])
            meas_dic = {i:[] for i in measure_set}
            meas_dic['time'] = []
            for i in x_json['items']:
                time_ = datetime.strptime(i['dateTime'], '%Y-%m-%dT%H:%M:%S%z')
                _start = now-timedelta(hours=24)
                if _start <= time_ <= now:
                    for j in meas_dic.keys():
                        if j in i['measure']:
                            meas_dic[j].append(i['value'])
                    meas_dic['time'].append(time_)
            meas_dic['time'] = list(dict.fromkeys(meas_dic['time']))
            graphJSON = make_plot(meas_dic,measures_one_station)
            return render_template('home.html', image = graphJSON)
        else:
            error = 'Invalid ID, Please Check and Try again'
            return render_template('home.html', error = error)

def make_plot(meas,measures):
    """
    Funtion To Create Plot
    @param:meas dict- contains the measured values with measure as keys
    @param:measures dict-contains the 
    """
    from plotly.graph_objs.scatter import Line
    specs=[[{"type": "table"}]]
    subplot_titles = ["Measured Values From <b>{}</b> To <b>{}</b>".format(min(meas['time']),max(meas['time']))]
    for i in range(len(meas.keys())-1):
        specs.append([{"type": "scatter"}])
    for i in meas.keys():
        if i != 'time':
            subplot_titles.append('{} Vs Time'.format(i))
    subplot_titles.append('Assosiated Properties of Measures')
    subplot_titles = tuple(subplot_titles)
    specs.append([{"type": "table"}])
    fig = make_subplots(rows=len(meas.keys())+1, cols=1,shared_xaxes=True,
    vertical_spacing=0.1,specs=specs,
    subplot_titles=subplot_titles,
    )

    fig.add_trace(go.Table(header=dict(values=[i for i in meas.keys()],
            font=dict(size=10),
            align="left"
        ),
        cells=dict(
            values=[meas[k] for k in meas],
            align = "left")
    ),row=1, col=1)
    traces = []
    for i,keys in enumerate(meas):
        if keys != 'time':
            traces.append(go.Scatter(x = meas['time'], y = meas[keys],text='time',name=keys, line = Line({'color': 'rgb(0, 0, 128)', 'width': 1})))
    x=2
    for i in range(0,len(traces)):
        fig.add_traces(traces[i],rows=x,cols=1)
        x+=1
    measure_details = {ky:[] for ky in measures['items'][0].keys()}
    measure_details.pop('latestReading', None)    
    for k in measures['items']:
        for ky in measure_details.keys():
            measure_details[ky].append(k[ky])
    fig.add_trace(go.Table(header=dict(values=[i for i in measure_details.keys()],
            # align="left",
            line_color='darkslategray',
            fill_color='royalblue',
            align=['left','center'],
            font=dict(color='white', size=12),
            height=40
        ),
        cells=dict(
            values=[measure_details[k] for k in measure_details.keys()],
            align = "left")
    ),row=x, col=1)
    fig.update_layout(height=1500, width=1250, title_text="Measured Values")
    graphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)
    return graphJSON