import os


# TODO: tighten this up

# if app_config_secret.py exists, use that to set config variables
if os.path.isfile(os.path.dirname(__file__)+'/app_config_secret.py'):
    from .app_config_secret import ADMIN_USER, ADMIN_PASS, SECRET_KEY, \
                                    DB_USER, DB_PW, DB_HOST, DB_NAME, \
                                    TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NO, \
                                    GDOC_ID

# otherwise, set config variables from environment variables,
# & assigns them to defaults if env vars don't exist
# (this is for deploying w/ docker)
else:

    ADMIN_USER = os.getenv('ADMIN_USER', 'admin')
    ADMIN_PASS = os.getenv('ADMIN_PASS', 'something-secret')

    SECRET_KEY = os.getenv('SECRET_KEY', 'another-secret-thing')

    DB_USER = os.getenv('DB_USER', 'root')
    DB_PW = os.getenv('DB_PW', '')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_NAME = os.getenv('DB_NAME', 'pfb')

    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', '')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', '')
    TWILIO_PHONE_NO = os.getenv('TWILIO_PHONE_NO', '')

    GDOC_ID = os.getenv('GDOC_ID', '')
