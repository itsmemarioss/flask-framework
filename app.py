from flask import Flask, render_template, request, redirect
import simplejson as json
import requests
import datetime
from bokeh.plotting import figure, output_file, show
from bokeh.resources import CDN
from bokeh.embed import file_html

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/about')
def about():
  return render_template('about.html')

#new route to handle the request from index page 
@app.route('/print', methods=['POST'])
def print_symbol():
  
  #retrieve the value of the symbol informed by the user
  symbol = request.form['symbol']
  
  #format the url adding the symbol parameter to it
  url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&apikey=NRZTU4B1MMEPE0EJ&datatype=json'.format(symbol)

  #request the json and load it
  page = requests.get(url)
  json_var = json.loads(page.content)

#---------------------------
  date_time_str = '2018-06-29 08:15:27.243860'
  date_time_obj = datetime.datetime.fromisoformat(date_time_str)
  #date_time_obj
  JV_Date = [datetime.datetime.fromisoformat(date) for date in json_var['Time Series (Daily)'].keys()]
  JV_Date = JV_Date[0:22]
  JV_Close_Price = list(json_var['Time Series (Daily)'].values())
  JV_Close = [float(row['5. adjusted close']) for row in JV_Close_Price]
  JV_Close = JV_Close[0:22]

  # create a new plot with a title and axis labels
  p = figure(title="Daily stock adjusted close price", x_axis_label='Date', y_axis_label='Adj. Close Price', x_axis_type='datetime')

  # add a line renderer with legend and line thickness
  p.line(JV_Date, JV_Close, line_width=2)

  html = file_html(p, CDN, symbol + " - Daily stock adjusted close price")

  return html
  

if __name__ == '__main__':
  app.run(port=33507)
