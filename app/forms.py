from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class VehicleForm(FlaskForm):
    vehicle_number = StringField('Vehicle Number', validators=[DataRequired()])
    make = StringField('Make', validators=[DataRequired()])
    model = StringField('Model', validators=[DataRequired()])
    color = StringField('Color', validators=[DataRequired()])
    issue_date = DateField('Issue Date', format='%Y-%m-%d', validators=[DataRequired()])
    registration_status = SelectField('Status', choices=[('Active','Active'), ('Expired','Expired')])
    owner_id = SelectField('Assign to Customer', coerce=int)
    submit = SubmitField('Save')

class CustomerForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password (leave blank to keep unchanged)')
    submit = SubmitField('Save')
