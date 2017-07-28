from flask import flash, redirect, request, render_template, Response, session
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from bot import create_app, resource_csv2dict
from bot import config
from bot.models import Answer
from bot.database import db
import twilio.twiml
from twilio.rest import TwilioRestClient
import importlib
import re
import us


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
        session['state'] = ''
        resp.sms("erasing my memory of our conversation")
        return str(resp)
    elif session.get('seen_resources') == True:
        # person has responding w/ description of their issue

        # only if there is an incoming msg
        if incoming_msg:
            new_report = Answer(
                    request.values.get('SmsSid'),
                    request.values.get('From'),
                    session.get('state'),
                    incoming_msg
                )
            db.session.add(new_report)
            db.session.commit()

        resp.sms("thanks for reporting!")
    elif session.get('seen_greeting') == True:
        # person is responding with state

        state = us.states.lookup(incoming_msg)
        # TODO: smarter way of doing this?
        resource_data = resource_csv2dict()
        state_info = resource_data.get(state.abbr) if state else None

        if state_info:
            session['seen_resources'] = True
            session['state'] = state.abbr

            resource_list = []
            if state_info['name_press_assn'] and state_info['phone_press_assn']:
                more_info = "{} - {}".format(
                        state_info['name_press_assn'],
                        state_info['phone_press_assn'])
                resource_list.append(more_info)
            if state_info['name_atty_gen'] and state_info['phone_atty_gen']:
                more_info = "{} AG {} - {}".format(
                        state.abbr,
                        state_info['name_atty_gen'],
                        state_info['phone_atty_gen'])
                resource_list.append(more_info)

            if resource_list:
                resource_list.insert(0, "here are some resources:")
                txt = '\n\n'.join(resource_list)
            else:
                txt = "no resources yet for {}".format(state.name)

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
    ADMIN_USER = config.CONFIG_VARS['ADMIN_USER']
    ADMIN_PASS = config.CONFIG_VARS['ADMIN_PASS']
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

@application.route('/reports')
@requires_auth
def reports():
    reports = Answer.query.all()
    return render_template('reports.html', reports=reports)

@application.route('/settings', methods=['GET', 'POST'])
@requires_auth
def settings():

    if request.method == 'POST':

        new_config = {
            "GDOC_ID": request.form['gdoc-id']
        }

        config.update_config(new_config)
        importlib.reload(config)

        flash("settings updated!")

    return render_template('settings.html', CONFIG_VARS=config.CONFIG_VARS)


@application.route('/grabcsv')
@requires_auth
def grab_csv():
    import requests

    GDOC_ID = config.CONFIG_VARS['GDOC_ID']
    url = "https://docs.google.com/spreadsheets/d/{}/export?format=csv".format(GDOC_ID)
    r = requests.get(url)
    data = r.content

    if r.status_code==200:

        outfile = 'bot/data/resources.csv'
        with open(outfile, 'wb') as f:
            f.write(data)

        flash("resources CSV updated!")

    else:
        flash("ERROR: couldn't download CSV. check GDOC_ID to make sure it is valid")

    return redirect('/')


@application.route('/initialize')
@requires_auth
def initialize():
    db.create_all()
    flash("db initialized!")
    return redirect('/')



if __name__ == "__main__":

    application.run(host='0.0.0.0')
