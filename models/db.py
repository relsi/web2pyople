# -*- coding: utf-8 -*- 

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
#########################################################################

if request.env.web2py_runtime_gae:            # if running on Google App Engine
    db = DAL('gae')                           # connect to Google BigTable
    session.connect(request, response, db=db) # and store sessions and tickets there
    ### or use the following lines to store sessions in Memcache
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db=MEMDB(Client()))
else:                                         # else use a normal relational database
    db = DAL('sqlite://storage.sqlite')       # if not, use SQLite or other DB
## if no need for session
# session.forget()

from gluon.tools import *
auth=Auth(globals(),db)              # authentication/authorization

db.define_table('country',
    Field('country'))

# a modification of auth table
db.define_table(
    auth.settings.table_user_name,
    Field('first_name', length=128, default='', label=T('Name')),
    Field('last_name', length=128, default='', label=T('Last name')),
    Field('email', length=128, default='', unique=True, label=T('E-mail')),
    Field('password', 'password', length=512, readable=False, label=T('Password')),
    Field('registration_key', length=512, writable=False, readable=False, default=''),
    Field('reset_password_key', length=512, writable=False, readable=False, default=''),
    Field('registration_id', length=512, writable=False, readable=False, default=''),
    Field("avatar", "upload", label=T('Avatar'), autodelete=True),
    Field("bio", "text", label=T('Bio')),
    Field("country", label=T('Country')),
    Field("site", label=T('Website')),
    Field("lat", "double", label=T('Latitude')),
    Field("lgt", "double", label=T('Longitude')))

   
custom_auth_table = db[auth.settings.table_user_name] # get the custom_auth_table
custom_auth_table.first_name.requires = IS_NOT_EMPTY(error_message=T('Please enter your name.'))
custom_auth_table.country.requires = IS_IN_DB(db, db.country.country, error_message=T('Please select a country.'))
custom_auth_table.last_name.requires = IS_NOT_EMPTY(error_message=T('Please enter your last name.'))
custom_auth_table.password.requires = [CRYPT()]
custom_auth_table.email.requires = [IS_EMAIL(error_message=T('Please enter your email.')),  IS_NOT_IN_DB(db, custom_auth_table.email, error_message=T('Email already registered.'))]

auth.settings.table_user = custom_auth_table # tell auth to use custom_auth_table


crud=Crud(globals(),db)              # for CRUD helpers using auth
service=Service(globals())           # for json, xml, jsonrpc, xmlrpc, amfrpc

auth.settings.hmac_key='sha512:889f4640-2ed1-4f0d-bc8a-d12cb47f7250'
auth.define_tables()                 # creates all needed tables

# to comunicate with users of system 
# mail=Mail()                                  # mailer
# mail.settings.server='smtp.gmail.com:587'    # your SMTP server
# mail.settings.sender='you@gmail.com'         # your email
# mail.settings.login='username:password'      # your credentials or None

# auth.settings.mailer=mail          # for user email verification
# auth.settings.registration_requires_verification = True
# auth.settings.registration_requires_approval = True
# auth.messages.verify_email = 'Click on the link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['verify_email'])+'/%(key)s to verify your email'
# auth.settings.reset_password_requires_verification = True
# auth.messages.reset_password = 'Click on the link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['reset_password'])+'/%(key)s to reset your password'

# crud.settings.auth=auth            # enforces authorization on crud
