from flask import redirect, request, render_template, Response, session
from functools import wraps
from bot import create_app
from bot.app_config import ADMIN_USER, ADMIN_PASS, SECRET_KEY, \
                                    TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NO
import twilio.twiml
from twilio.rest import TwilioRestClient


application = create_app()

@application.route("/")
def index():
    # TODO: grab some recordings to show
    return render_template('index.html')



@application.route("/respond", methods=['GET', 'POST'])
def respond():
    """Respond to incoming texts"""


    resp = twilio.twiml.Response()

    incoming_msg = request.values.get('Body', '')

    # this clears all cookies
    if(incoming_msg=='clear'):
        session['seen_prompt'] = False
        session['gave_rec'] = False
        session['extra_msg'] = False
        resp.sms("erasing my memory of our conversation")
        return str(resp)


    resp.sms("hello world")

    return str(resp)



def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == ADMIN_USER and password == ADMIN_PASS

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your credentials for that url', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

# @application.route('/review')
# @requires_auth
# def review():
#     return render_template('review.html')




if __name__ == "__main__":

    application.secret_key = SECRET_KEY
    application.run(debug=True, host='0.0.0.0')
