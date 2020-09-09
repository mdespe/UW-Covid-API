from flask import Flask
from flask_restful import Api, Resource, reqparse
import requests
from bs4 import BeautifulSoup
import pandas as pd


app = Flask(__name__)
api = Api(app)


def remove_percent(data):
    split = data.split(' ')
    return split[0]


# get data from UW Dashboard
def get_dashboard_data():
    url = 'https://smartrestart.wisc.edu/dashboard/#data-notes'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    df = pd.read_html(str(table))[0]
    df.columns = ['Date', 'Students positive', 'Total student tests', 'Employees positive', 'Total employee tests']
    df['Students positive'] = df.apply(lambda x: remove_percent(x['Students positive']), axis=1)
    df['Employees positive'] = df.apply(lambda x: remove_percent(x['Employees positive']), axis=1)
    return df


class Stats(Resource):
    def get(self, date=''):
        try:
            df = get_dashboard_data()
            if date == '':
                pass
            else:
                df = df[df['Date'] == date]
            json = df.to_json(orient='records')
            return json, 200
        except:
            return 'Data not found', 404


# @app.route('/')
# def hello_world():
#     return 'Hello World!'

api.add_resource(Stats, '/uw-covid', '/uw-covid/', '/uw-covid/<string:date>')


if __name__ == '__main__':
    app.run(debug=True)
