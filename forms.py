from flask.ext.wtf import Form
from wtforms.fields import TextField, PasswordField, BooleanField, DateField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo

class LoginForm(Form):
    username = TextField('Username', validators=[DataRequired(), Length(min=5)])
    password = PasswordField('Passwort', validators=[DataRequired()])
    remember = BooleanField('Remember me', default=False)

class RegisterForm(Form):
    username = TextField("Benutzername:",validators=[DataRequired(),Length(min=3)])
    password = PasswordField("Passwort:", validators=[DataRequired(),Length(min=1)])
    confirm = PasswordField("Passwort wiederholen:", validators=[DataRequired(),Length(min=1),EqualTo("password",message="Ups. Deine Eingaben passen nicht zusammen")])

class EditPasswordForm(Form):
    old_password = PasswordField('Aktuelles Passwort', validators=[DataRequired()])
    password = PasswordField('Passwort', validators=[DataRequired(), EqualTo('confirm', message='Passwoerter muessen uebereinstimmen!'), Length(min=8)])
    confirm = PasswordField('Passwort wiederholen', validators=[DataRequired()])

class EditUserPasswordForm(Form):
    password = PasswordField('Passwort', validators=[DataRequired(), EqualTo('confirm', message='Passwoerter muessen uebereinstimmen!'), Length(min=8)])
    confirm = PasswordField('Passwort wiederholen', validators=[DataRequired()])

class NewUserForm(Form):
    username = TextField('Username', validators=[DataRequired(), Length(min=5)])
    password = PasswordField('Passwort', validators=[DataRequired()])
    active = BooleanField('Active', default=True)

class EditUserForm(Form):
    username = TextField('Username', validators=[DataRequired(), Length(min=5)])
    active = BooleanField('Active', default=True)

# class TagebuchForm(Form):
#     tagebuch = TextField('Tagebuch', validators=[DataRequired(), Length(min=5)])


class NewContactForm(Form):
    lastname = TextField('Nachname', validators=[DataRequired()])
    firstname = TextField('Vorname')
    title = TextField('Titel')
    street = TextField('Strasse')
    zip = TextField('PLZ')
    city = TextField('Stadt')
    birthdate = TextField('Geburtsdatum')
    landline = TextField('Telefon (Festnetz)')
    mobile_phone = TextField('Telefon (mobil)')
    email = TextField('E-Mail')
    homepage = TextField('Homepage')
    handy = TextField('Handynummer')
    twitter = TextField('Twitter', validators=[Length(max=15)])

class NewDiaryForm(Form):
    date = TextField('Datum', validators=[DataRequired()])
    text = TextField('Text', validators=[DataRequired()])

class ContactSearchForm(Form):
    searchfield = SelectField('Suche Nach:', choices=[('lastname', 'Nachname'), ('firstname', 'Vorname'), ('city', 'Stadt')])
    searchterm = TextField('searchterm', validators=[DataRequired()])