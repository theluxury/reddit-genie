from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class SearchForm(Form):
    # todo: maybe make some of these no required if you want to, uh, search for generic words. 
    subreddit = StringField('subreddit', validators=[DataRequired()])
    topic = StringField('topic', validators=[DataRequired()])
    year_month = StringField('year_month', validators=[DataRequired()])
