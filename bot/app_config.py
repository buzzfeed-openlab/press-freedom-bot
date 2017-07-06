import json
import os

DEFAULT_SETTINGS = {
    "ADMIN_USER" : "admin",
    "ADMIN_PASS" : "something-secret",
    "DB_USER" : "root",
    "DB_PW" : "",
    "DB_HOST" : "localhost",
    "DB_NAME" : "pfb",
    "TWILIO_ACCOUNT_SID" : "",
    "TWILIO_AUTH_TOKEN" : "",
    "TWILIO_PHONE_NO" : "", # "+12223456789"
    "SECRET_KEY" : "another-secret-thing",
    "GDOC_ID" : ""
}



config_filepath = os.path.dirname(__file__)+'/app_config_secret.json'


# make a config file if it doesnt exist, based on default values & env vars
if not os.path.isfile(config_filepath):
    # TODO: a more elegant way of doing this?

    config_settings = {}
    for k, default_v in DEFAULT_SETTINGS.items():
        # if env var exists, use env var value - otherwise use default value
        config_settings[k] = os.getenv(k, default_v)

    with open(config_filepath, 'w') as f:
        json.dump(config_settings, f, indent=4)


# TODO: handle when config file exists but env vars have been updated


# read settings from config file
with open(config_filepath) as f:
    json_config = json.load(f)

    # TODO: a more elegant way of doing this?
    ADMIN_USER = json_config.get('ADMIN_USER', DEFAULT_SETTINGS['ADMIN_USER'])
    ADMIN_PASS = json_config.get('ADMIN_PASS', DEFAULT_SETTINGS['ADMIN_PASS'])
    DB_USER = json_config.get('DB_USER', DEFAULT_SETTINGS['DB_USER'])
    DB_PW = json_config.get('DB_PW', DEFAULT_SETTINGS['DB_PW'])
    DB_HOST = json_config.get('DB_HOST', DEFAULT_SETTINGS['DB_HOST'])
    DB_NAME = json_config.get('DB_NAME', DEFAULT_SETTINGS['DB_NAME'])
    TWILIO_ACCOUNT_SID = json_config.get('TWILIO_ACCOUNT_SID', DEFAULT_SETTINGS['TWILIO_ACCOUNT_SID'])
    TWILIO_AUTH_TOKEN = json_config.get('TWILIO_AUTH_TOKEN', DEFAULT_SETTINGS['TWILIO_AUTH_TOKEN'])
    TWILIO_PHONE_NO = json_config.get('TWILIO_PHONE_NO', DEFAULT_SETTINGS['TWILIO_PHONE_NO'])
    SECRET_KEY = json_config.get('SECRET_KEY', DEFAULT_SETTINGS['SECRET_KEY'])
    GDOC_ID = json_config.get('GDOC_ID', DEFAULT_SETTINGS['GDOC_ID'])
