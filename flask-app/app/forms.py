from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, Field
from wtforms.validators import DataRequired

# Processes month to match index format. 
class MonthField(Field):
    def process_formdata(self, month):
        if month:
            self.data = month[0].replace('-', '_')
        else:
            self.data = []

class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class SearchForm(Form):
    # todo: maybe make some of these no required if you want to, uh, search for generic words. 
    subreddit = StringField('subreddit', validators=[DataRequired()])
    topic = StringField('topic', validators=[DataRequired()])
    year_month = MonthField('year_month', validators=[DataRequired()])
