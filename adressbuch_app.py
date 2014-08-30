from flask import Flask, render_template, url_for, redirect, flash, request, session
import config
from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user
from models import User, Contact, Diary
from database import db_session
from forms import LoginForm, RegisterForm, EditPasswordForm, NewDiaryForm, NewUserForm, EditUserForm, EditUserPasswordForm, NewContactForm, ContactSearchForm
from hash_passwords import make_hash
from sqlalchemy import asc, func
import datetime
from collections import OrderedDict
from database import *



app = Flask(__name__)
app.debug = True
app.config.from_object(config)

# Integration von Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/')
def index():
    return render_template('index.jinja')


@app.route('/adressbuch')                           # URL
def adressbuch():                                   # Name der Methode
    return render_template('adressbuch.jinja')      # Name der JINJA-Datei


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.valid_password(form.password.data):
            if login_user(user, remember=form.remember.data):
                session.permanent = not form.remember.data
                flash('Du bist erfolgreich eingeloggt / You successfully logged in')
                return redirect(request.args.get('next') or url_for('logged_in'))
            else:
                flash('Dieser Account ist deaktiviert / This account is deactivated')
        else:
            flash('Falscher Username oder Passwort. / Wrong username or password')
    return render_template('login.jinja', form=form)

@app.route("/register",methods=["GET","POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            new_user = User(username=form.username.data, password=make_hash(form.password.data))
            if new_user:
                db_session.add(new_user)
                db_session.commit()
            return redirect(url_for("login"))
        else:
            flash('Username still exists!')
    return render_template("register.jinja",form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Geschafft! Du hast dich gerade erfolgreich ausgeloggt. Bis zum naechsten Mal / Done! You successfully logged out')
    return redirect(url_for('index'))

@app.route("/dashboard")
@login_required
def logged_in():
    return render_template('dashboard.jinja')

@app.route('/tagebuch', methods=["GET", "POST"])
@login_required
def tagebuch():
    user = User.query.filter_by(id=current_user.id).first()
    form = TagebuchForm()
    if form.validate_on_submit():
        if user is not None:
            user.tagebucheintrag = form.tagebuch
            db_session.add(user)
            db_session.commit()
            flash('Du hast einen Tagebucheintrag erstellt! /You created a diary entry!')
        return redirect(url_for('dashboard'))
    return render_template('tagebuch.jinja', form=form)

@app.route('/password', methods=["GET", "POST"])
@login_required
def password():
    user = User.query.filter_by(id=current_user.id).first()
    form = EditPasswordForm()
    if form.validate_on_submit():
        if user is not None and user.valid_password(form.old_password.data):
            user.password = make_hash(form.password.data)
            db_session.add(user)
            db_session.commit()
            flash('Passwort erfolgreich aktualisiert! / Password updated successfully!')
            return redirect(url_for('dashboard'))
        else:
            flash('Passwort nicht aktualisiert! Aktuelles Passwort nicht korrekt! / Password not updated! Contemporary password not orrect!')
    return render_template('password.jinja', form=form)

@app.route('/user/add', methods=["GET", "POST"])
@login_required
def user_add():
    form = NewUserForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, password=make_hash(form.password.data), active=form.active.data)
        if new_user:
            db_session.add(new_user)
            db_session.commit()
            flash('Neuer Nutzer erfolgreich angelegt! / New user successfully created!')
            return redirect(url_for('dashboard'))
        else:
            flash('Neuer Nutzer konnte nicht angelegt werden! / New user couldnt be created!')
    return render_template('user_add.jinja', form=form)

@app.route('/user/edit/<user_id>', methods=["GET", "POST"])
@login_required
def user_edit(user_id):
    user = User.query.filter_by(id=user_id).first()
    form = EditUserForm(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        db_session.add(user)
        db_session.commit()
        flash('Nutzerdaten erfolgreich aktualisiert! / Userdata successfully updated!')
        return redirect(url_for('user_list'))
    return render_template('user_edit.jinja', form=form, user=user)

@app.route('/user/password/<user_id>', methods=["GET", "POST"])
@login_required
def user_password(user_id):
    user = User.query.filter_by(id=user_id).first()
    form = EditUserPasswordForm()
    if form.validate_on_submit():
        if user is not None:
            user.password = make_hash(form.password.data)
            db_session.add(user)
            db_session.commit()
            flash('Passwort erfolgreich aktualisiert! / Password successfully updated!')
            return redirect(url_for('user_list'))
        else:
            flash('Passwort nicht aktualisiert! Aktuelles Passwort nicht korrekt! / Password not updated! Contemporary password not correct!')
    return render_template('user_password.jinja', form=form, user=user)

@app.route('/user/list')
@login_required
def user_list():
    users = User.query.order_by(asc('username')).all()
    return render_template('user_list.jinja', users=users)

# Neue Routen und View-Funktionen fuer Projekt 1 - BEGINN

@app.route('/contacts')
@login_required
def contacts():
    result = Contact.query.filter_by(user_id=current_user.id).order_by('lastname').all()
    return render_template('contacts.jinja', contacts=result)

@app.route('/diaries')
@login_required
def diaries():
    result = Diary.query.filter_by(user_id=current_user.id).order_by('date').all()
    return render_template('diaries.jinja', diaries=result)

@app.route('/contac/add', methods=["GET", "POST"])
@login_required
def contact_add():
    form = NewContactForm()
    if form.validate_on_submit():
        new_contact = Contact(lastname=form.lastname.data, firstname=form.firstname.data, user_id=current_user.id, title=form.title.data, street=form.street.data, zip=form.zip.data, city=form.city.data, birthdate=form.birthdate.data, landline=form.landline.data, mobile_phone=form.mobile_phone.data, email=form.email.data, homepage=form.homepage.data, twitter=form.twitter.data)
        db_session.add(new_contact)
        db_session.commit()
        flash('Neuer Kontakt angelegt! / New contact created!')
        return redirect(url_for('contacts'))
    return render_template('contact_add.jinja', form=form)

@app.route('/diary/add', methods=["GET", "POST"])
@login_required
def diary_add():
    form = NewDiaryForm()
    if form.validate_on_submit():
        new_diary = Diary(date=form.date.data, text=form.text.data, user_id=current_user.id)
        db_session.add(new_diary)
        db_session.commit()
        flash('Neuer Tagebucheintrag angelegt! / New diary entry created!')
        return redirect(url_for('diaries'))
    return render_template('diary_add.jinja', form=form)

@app.route('/diary/edit/<contact_id>', methods=["GET", "POST"])
@login_required
def diary_edit(diary_id):
    result = Diary.query.filter_by(id=diary_id).first()
    if not result:
        flash('Tagebucheintrag existiert nicht! / Diary entry doesnt exist!')
        return redirect(url_for('diaries'))
    form = NewDiaryForm(obj=result)
    if form.validate_on_submit():
        form.populate_obj(result)
        db_session.add(result)
        db_session.commit()
        flash('Tagebucheintrag erfolgreich aktualisiert! / Diary entry successfully updated!')
        return redirect(url_for('diaries'))
    return render_template('dairy_edit.jinja', form=form, diary=result)

@app.route('/contact/edit/<contact_id>', methods=["GET", "POST"])
@login_required
def contact_edit(contact_id):
    contact = Contact.query.filter_by(user_id=current_user.id, id=contact_id).first()
    if not contact:
        flash('Kontakt existiert nicht! / Contact doesnt exist!')
        return redirect(url_for('contacts'))
    form = NewContactForm(obj=contact)
    if form.validate_on_submit():
        form.populate_obj(contact)
        db_session.add(contact)
        db_session.commit()
        flash('Kontakt erfolgreich aktualisiert! / Contaxt successfully updated!')
        return redirect(url_for('contacts'))
    return render_template('contact_edit.jinja', form=form, contact=contact)

@app.route('/contact/delete/<contact_id>')
@login_required
def contact_delete(contact_id):
    # schoenere Variante: vorher noch eine Seite, die abfragt,
    # ob der ausgewaehlte Nutzer wirklich geloescht werden soll
    contact = Contact.query.filter_by(user_id=current_user.id, id=contact_id).first()
    if not contact:
        flash('Kontakt existiert nicht! / Contact doesnt exist!')
        return redirect(url_for('contacts'))
    db_session.delete(contact)
    db_session.commit()
    flash('Kontakt entfernt! / Contact deleted!')
    return redirect(url_for('contacts'))

@app.route('/contacts/cities')
@login_required
def contacts_cities():
    # http://docs.sqlalchemy.org/en/rel_0_9/orm/tutorial.html#counting
    cities = db_session.query(Contact.city, func.count(Contact.city)).filter_by(user_id=current_user.id).filter(Contact.city!='').group_by(Contact.city).order_by('city').all()
    return render_template('contacts_cities.jinja', cities=cities)
    """
    # Alternative:
    contacts_with_city = Contact.query.filter(Contact.city!='').filter_by(user_id=current_user.id).all()
    cities = list(set([contact.city for contact in contacts_with_city]))
    city_data = {}
    for city in cities:
        city_data[city] = Contact.query.filter_by(user_id=current_user.id, city=city).count()
    return render_template('contacts_cities_alternative.jinja', city_data=city_data)
    """

@app.route('/contacts/birthdays')
@login_required
def contacts_birthdays():
    contacts_months = {}
    contacts = Contact.query.filter_by(user_id=current_user.id).order_by('lastname').all()
    for contact in contacts:
        if contact.birthdate.month in contacts_months:
            contacts_months[contact.birthdate.month]['contacts'].append(contact)
        else:
            contacts_months[contact.birthdate.month] = {}
            contacts_months[contact.birthdate.month]['contacts'] = [contact]
            contacts_months[contact.birthdate.month]['month'] = contact.birthdate.strftime('%B')
    # https://docs.python.org/dev/library/collections.html#ordereddict-examples-and-recipes
    contacts_sorted = OrderedDict(sorted(contacts_months.items(), key=lambda t: t[0]))
    return render_template('contacts_birthdays.jinja', contacts_sorted=contacts_sorted)

@app.route('/contacts/birthdays/upcoming')
@login_required
def contacts_birthdays_upcoming():
    days_upcoming = 30
    today = datetime.date.today()
    contacts_all = Contact.query.filter_by(user_id=current_user.id).all()
    contacts = {}
    date_list = [((today + datetime.timedelta(days=x)).month, (today + datetime.timedelta(days=x)).day) for x in range(1, days_upcoming+1)]

    for contact in contacts_all:
        if (contact.birthdate.month, contact.birthdate.day) in date_list:
            age = today.year - contact.birthdate.year - ((today.month, today.day) > (contact.birthdate.month, contact.birthdate.day))
            contacts[contact] = {"age":age, "birthdate":contact.birthdate}
            print contacts[contact], type(contacts[contact])
    return render_template('contacts_birthdays_upcoming.jinja', contacts=contacts)

@app.route('/contacts/search', methods=["GET", "POST"])
@login_required
def contacts_search():
    form = ContactSearchForm()
    results = []
    if form.validate_on_submit():
        if form.searchfield.data == 'lastname':
            results = Contact.query.filter_by(user_id=current_user.id).filter(Contact.lastname.like('%'+form.searchterm.data+'%')).order_by('lastname').all()
            return render_template('contacts_search.jinja', form=form, results = results)
        elif form.searchfield.data == 'firstname':
            results = Contact.query.filter_by(user_id=current_user.id).filter(Contact.firstname.like('%'+form.searchterm.data+'%')).order_by('firstname').all()
            return render_template('contacts_search.jinja', form=form, results = results)
        elif form.searchfield.data == 'city':
            results = Contact.query.filter_by(user_id=current_user.id).filter(Contact.city.like('%'+form.searchterm.data+'%')).order_by('city').all()
            return render_template('contacts_search.jinja', form=form, results = results)
        else:
            flash('Ungueltige Feldoption! / Invalid fieldoption!')
            return redirect(url_for('contacts_search'))
    return render_template('contacts_search.jinja', form=form)

if __name__ == "__main__":
    init_db()
    app.run()