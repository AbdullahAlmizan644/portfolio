from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from datetime import *
import json
from flask_mail import Mail




with open("config.json","r") as c:
    cont=json.load(c)["params"]

local_server=True
app=Flask(__name__)
app.config.update(
    MAIL_SERVER ="smtp.gmail.com",
    MAIL_PORT="465",
    MAIL_USE_SSL=True,
    MAIL_USERNAME=cont['gmail-user'],
    MAIL_PASSWORD=cont['gmail-password']

)

mail=Mail(app)
if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] =cont['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = cont['prod_uri']
db = SQLAlchemy(app)

class Contact(db.Model):
    sno= db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),  nullable=False)
    email = db.Column(db.String(120),  nullable=False)
    phn_num = db.Column(db.String(120), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(120), nullable=True)


@app.route("/", methods=['GET','POST'])
def home():
    if(request.method=='POST'):
        """add entry to database"""
        nm=request.form.get("nm")
        email=request.form.get("email")
        phone=request.form.get("phone")
        message=request.form.get("message")


        entry = Contact(name=nm, phn_num=phone, msg=message, date=datetime.now(), email=email)
        db.session.add(entry)
        db.session.commit()
        mail.send_message("new message from " + nm,
                          sender=email,
                          recipients=[cont["gmail-user"]],
                          body=message + "\n" + phone
        )

    return render_template("index.html",mizan=cont)



app.run(debug=True)