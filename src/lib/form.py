import re
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import validators
from wtforms import SelectField
from wtforms import StringField
from wtforms import RadioField


class AutocompleteForm(FlaskForm):
	message = StringField('Anything wanted', [
		validators.Length(max=25)])
