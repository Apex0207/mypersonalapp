from flask import Flask

from flask_wtf.csrf import CSRFProtect

from flask_sqlalchemy import SQLAlchemy

app =Flask(__name__,instance_relative_config=True)



csrf =CSRFProtect(app)



from mypersonalapp import config



app.config.from_object(config.ProductionConfig)
app.config.from_pyfile('config.py',silent=False)
db = SQLAlchemy(app)
from mypersonalapp import models
from mypersonalapp import forms
from mypersonalapp import routes
