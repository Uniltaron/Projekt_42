from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import config
from hash_passwords import make_hash

engine = create_engine(config.DB_URI, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models
    clear_db()
    Base.metadata.create_all(bind=engine)


    admin_password = make_hash('test1234')
    admin_user = models.User(username='admin', password= admin_password, active=True)
    db_session.add(admin_user)
    db_session.commit()

    contact = models.Contact(lastname='Mustermann',firstname='Max',user_id='1',title='',street='Blubbstrasse',zip='33212',city='Duesseldorf',birthdate='31.12.1988',landline='0211-323421',mobile_phone='',email='mustermann@web.de',homepage='',twitter='')
    db_session.add(contact)
    contact = models.Contact(lastname='Musterfrau',firstname='Martina',user_id='1',title='', street='Musterweg 1', zip='33322', city='Duesseldorf',birthdate='12.03.1978',landline='0211-345522',mobile_phone='', email='musterfrau@googlemail.com',homepage='',twitter='')
    db_session.add(contact)
    contact = models.Contact(lastname='Merkel',firstname='Angela',user_id='1',title='', street='Kanzlerstrasse 8', zip='11234', city='Berlin',birthdate='04.12.1955',landline='0332-121212',mobile_phone='', email='kanzlerin@bundeskanzleramt.de',homepage='',twitter='')
    db_session.add(contact)
    contact = models.Contact(lastname='Evers',firstname='Horst',user_id='1',title='', street='Lachstrasse 2', zip='94322', city='Witzhausen',birthdate='13.03.1964',landline='0421-468932',mobile_phone='', email='horst@lachsack.de',homepage='',twitter='')
    db_session.add(contact)
    contact = models.Contact(lastname='Musterfrau',firstname='Martina',user_id='1',title='', street='Musterweg 1', zip='33322', city='Duesseldorf',birthdate='12.03.1978',landline='0211-345522',mobile_phone='', email='musterfrau@googlemail.com',homepage='',twitter='')
    db_session.add(contact)
    contact = models.Contact(lastname='Torsten',firstname='Straeter',user_id='1',title='', street='Im Witzwinkel 3', zip='54234', city='Laecheln',birthdate='12.11.1988',landline='0233-24567',mobile_phone='', email='straeter@googlemail.com',homepage='',twitter='')
    db_session.add(contact)
    contact = models.Contact(lastname='Wicht',firstname='Nicole',user_id='1',title='', street='Gartenallee 14', zip='22234', city='Hussum',birthdate='04.01.1998',landline='',mobile_phone='', email='wicht@aol.de',homepage='',twitter='')
    db_session.add(contact)
    contact = models.Contact(lastname='Tannenbaum',firstname='Lara',user_id='1',title='', street='Waldweg 133', zip='33322', city='Nadeln',birthdate='24.12.1965',landline='',mobile_phone='', email='krassseszeug@googlemail.com',homepage='',twitter='')
    db_session.add(contact)
    contact = models.Contact(lastname='Eichhorn',firstname='Benedikt',user_id='1',title='', street='Nussstrasse 1', zip='23453', city='Hasln',birthdate='12.06.1968',landline='0211-44322', mobile_phone='',email='nuessschen@googlemail.com',homepage='',twitter='')
    db_session.add(contact)
    contact = models.Contact(lastname='Schlange',firstname='Sandra',user_id='1',title='', street='Natterweg 54', zip='34578', city='Schlaengeln',birthdate='12.12.1948',landline='0442-34224',mobile_phone='', email='python@googlemail.com',homepage='',twitter='')
    db_session.add(contact)
    db_session.commit()

    print "fertig!"

def clear_db():
    Base.metadata.drop_all(bind=engine)