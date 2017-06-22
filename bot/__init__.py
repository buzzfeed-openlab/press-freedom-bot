from flask import Flask
import csv
import os
import re

def create_app():
    app = Flask(__name__)

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
