from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField
from wtforms.validators import DataRequired
from datetime import datetime

##---------------------- CONFIGURE BOOTSTRAP ---------------------- ##
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

##---------------------- CONTACT FORM ---------------------- ##
class ContactForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired()])
    body = StringField("message", validators=[DataRequired()])
    submit = SubmitField("send")

##---------------------- COPYRIGHT YEAR ---------------------- ##
year = datetime.now().strftime("%Y")

@app.route("/")
def home_page():
    form = ContactForm()

    return render_template("index.html", form=form, year=year)

@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")

if __name__ == "__main__":
    app.run(debug=True)