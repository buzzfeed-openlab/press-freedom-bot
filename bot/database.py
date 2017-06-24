from flask_sqlalchemy import SQLAlchemy
from bot import create_app


app = create_app()
db = SQLAlchemy(app)
