from flask import Flask, render_template, request, redirect
import simplejson as json
import requests

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
  obj = json.loads(page.content)

  #after loading json into a variable it will create a dictionary so you can add the properties of the json by name
  print(obj.__class__) #dict

  #return only the dates with the prices part
  #from now on you need to clean the data to use it in pandas. I suppose ;)
  return obj["Time Series (Daily)"]

if __name__ == '__main__':
  app.run(port=33507)
