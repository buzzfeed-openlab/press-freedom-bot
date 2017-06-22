from flask import redirect, request, render_template, Response, session
from functools import wraps
from bot import create_app, RESOURCE_DATA
from bot.app_config import ADMIN_USER, ADMIN_PASS, SECRET_KEY, \
                                    TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NO, \
                                    GDOC_ID
import twilio.twiml
from twilio.rest import TwilioRestClient


application = create_app()

@application.route("/")
def index():
    return render_template('index.html')



@application.route("/respond", methods=['GET', 'POST'])
def respond():
    """Respond to incoming texts"""


    resp = twilio.twiml.Response()

    incoming_msg = request.values.get('Body', '')

    if(incoming_msg=='clear'):
        # this clears all cookies
        session['seen_greeting'] = False
        session['seen_resources'] = False
        resp.sms("erasing my memory of our conversation")
        return str(resp)
    elif session.get('seen_resources') == True:
        # person has responding w/ description of their issue
        # TODO: store the response here
        resp.sms("thanks for reporting!")
    elif session.get('seen_greeting') == True:
        # person is responding with state

        # TODO: more robust matching here
        clean_state = incoming_msg.lower().strip()
        state_info = RESOURCE_DATA.get(clean_state)

        if state_info:
            session['seen_resources'] = True

            txt = "here are some resources:\n{} - {}"\
                .format(
                    state_info['name_press_assn'],
                    state_info['phone_press_assn']
                )

            resp.sms(txt)
            resp.sms("if you'd like, tell us about your issues. [more copy here about how this info will be used]")
        else:
            resp.sms("sorry, I don't recognize that state. what state are you in?")
    else:
        # this is the first time someone has texted
        session['seen_greeting'] = True
        resp.sms("hello! [intro text here]\nwhat state are you in?")


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

@application.route('/grabcsv')
@requires_auth
def grab_csv():
    import requests

    url = "https://docs.google.com/spreadsheets/d/{}/export?format=csv".format(GDOC_ID)
    r = requests.get(url)
    data = r.content

    outfile = 'bot/data/resources.csv'
    with open(outfile, 'wb') as f:
        f.write(data)

    # TODO: error handling, flash message with success/failure
    return render_template('index.html')



if __name__ == "__main__":

    application.secret_key = SECRET_KEY
    application.run(debug=True, host='0.0.0.0')
