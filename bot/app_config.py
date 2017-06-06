import os


# TODO: tighten this up

# if app_config_secret.py exists, use that to set config variables
if os.path.isfile(os.path.dirname(__file__)+'/app_config_secret.py'):
    from .app_config_secret import ADMIN_USER, ADMIN_PASS, SECRET_KEY, \
                                    TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NO

# otherwise, set config variables from environment variables,
# & assigns them to defaults if env vars don't exist
# (this is for deploying w/ docker)
else:

    ADMIN_USER = os.getenv('ADMIN_USER', 'admin')
    ADMIN_PASS = os.getenv('ADMIN_PASS', 'something-secret')

    SECRET_KEY = os.getenv('SECRET_KEY', 'another-secret-thing')

    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', '')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', '')
    TWILIO_PHONE_NO = os.getenv('TWILIO_PHONE_NO', '')