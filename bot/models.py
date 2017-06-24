import datetime

from .database import db


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text_sid = db.Column(db.String(255))
    from_number = db.Column(db.String(255))
    from_state = db.Column(db.String(255))
    answer_text = db.Column(db.Text)
    status_reviewed = db.Column(db.Boolean)
    status_desc = db.Column(db.String(255))
    dt = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, text_sid, from_number, from_state, answer_text):
        self.text_sid = text_sid
        self.from_number = from_number
        self.from_state = from_state
        self.answer_text = answer_text
        self.status_reviewed = False

    def __repr__(self):
        return '<Answer %r %r>' % (self.from_state, self.answer_text[:10])
