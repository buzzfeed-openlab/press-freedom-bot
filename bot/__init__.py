from flask import Flask
from .app_config import DB_USER, DB_PW, DB_HOST, DB_NAME
import csv
import os
import re

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://{0}:{1}@{2}/{3}"\
                                            .format(DB_USER, DB_PW, DB_HOST, DB_NAME)

    return app


# loading data from csv
# is there a better place to put this?
RESOURCE_DATA = {}

with open(os.path.dirname(__file__)+'/data/resources.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        state_slug = re.sub(r'[^a-z]+', '_', row['state'].lower().strip())

        RESOURCE_DATA[state_slug] = {
            'name_press_assn': row['name_press_assn'],
            'phone_press_assn': row['phone_press_assn'],
            'name_atty_gen': row['name_atty_gen'],
            'phone_atty_gen': row['phone_atty_gen'],
            'url_reporters_committee': row['url_reporters_committee']
        }
