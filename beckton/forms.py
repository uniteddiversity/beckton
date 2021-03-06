from beckton import app
from flask_wtf import Form
from ukpostcodeutils import validation
from wtforms import BooleanField, TextField, RadioField, validators, ValidationError

_BECKTON_TERMS = []
for rate in app.config['BECKTON_RATES_CSV'].split('|'):
    items = rate.split(',')
    _BECKTON_TERMS.append((items[0], items[1]))

class Commitment(Form):
    name = TextField('Full name', [validators.Required(message="You need to enter your name"), validators.Length(max=100)])
    mobile_number = TextField('Mobile number', [validators.Regexp('(07[\d]{8,12}|447[\d]|\+447[\d]{7,11})', message="You need to enter a valid mobile phone number")])
    postcode = TextField('Postcode', [validators.Required(message="You need to enter a valid postcode")])
    rate = RadioField(app.config['BECKTON_RATES_LABEL'], [validators.Required(message="You need to choose an option")], choices=_BECKTON_TERMS)
    agree = BooleanField(app.config['BECKTON_TERMS'], [validators.InputRequired(message="You need to agree")])

    def validate_postcode(form, field):

        #is it a postcode?
        if not validation.is_valid_postcode(field.data.replace(' ', '').upper()):
            raise ValidationError('You need to enter a valid postcode')
                
        if app.config.get('BECKTON_POSTCODE_AREAS_CSV', False):
            #is it in the an allowed postcode?
            condition_postcode_areas = app.config['BECKTON_POSTCODE_AREAS_CSV'].split(',')
            if not condition_postcode_areas == []:
                in_bounds = False

                for postcode_area in condition_postcode_areas:
                    if field.data.lower().startswith(postcode_area.lower()):
                      in_bounds = True

                if not in_bounds:
                    postcode_areas_formatted = ', '.join(condition_postcode_areas)
                    raise ValidationError('You can currently only sign up if your postcode starts with %s' % postcode_areas_formatted)

