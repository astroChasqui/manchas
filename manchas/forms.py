from flask.ext.wtf import Form
from wtforms import SelectField, SubmitField


class DateForm(Form):
    year = SelectField(choices = [(x, x) for x in range(2001, 2014+1)],
                       coerce=int)
    month = SelectField(choices = [(x, x) for x in range(1, 12+1)],
                        coerce=int)
    day = SelectField(choices = [(x, x) for x in range(1, 31+1)],
                      coerce=int)
    weeks = SelectField(choices = [(x, x) for x in range(1, 8)],
                        coerce=int)
    submit = SubmitField('Submit')
