from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, SelectField, MultipleFileField
from wtforms.validators import DataRequired
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename

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

# ---------------------- CONNECT TO DB ----------------------#
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#---------------------- CONFIGURE DB TABLE ----------------------#
class Portfolio(db.Model):
    __tablename__ = "portfolio"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    number = db.Column(db.Integer, unique=True, nullable=False)
    level = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250), unique=True, nullable=False)
    github = db.Column(db.String(250), unique=True, nullable=False)
    focus = db.Column(db.String(250))
    c_name = db.Column(db.String(250))
    c_provider = db.Column(db.String(250), nullable=False)
    image_paths = db.Column(db.String(250), nullable=False)
    gif_paths = db.Column(db.String(250))
    misc = db.Column(db.String(500))
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

with app.app_context():
    db.create_all()


#---------------------- ADD PROJECT ----------------------#
class AddNewProjectForm(FlaskForm):
    name = StringField("Project Name", validators=[DataRequired()])
    number = StringField("Project Number", validators=[DataRequired()])
    level = SelectField(u"Project Level", choices=["Beginner", "Intermediate", "Intermediate+", "Advanced", "Portfolio"])
    description = StringField("Project Description", validators=[DataRequired()])
    github = StringField("GitHub Link (URL)", validators=[DataRequired()])
    focus = StringField("Project Focus")
    c_name = SelectField(u"Course Name", choices=["100 Days of Code: The Complete Python Bootcamp"], validators=[DataRequired()])
    c_provider = SelectField(u"Course Provider", choices=["The App Brewery"], validators=[DataRequired()])
    image_paths = MultipleFileField("Project Images")
    gif_paths = MultipleFileField("Project Gifs")
    misc = StringField("Misc Data")
    submit = SubmitField("Submit")
##---------------------- COPYRIGHT YEAR ---------------------- ##
year = datetime.now().strftime("%Y")

@app.route("/")
def home_page():
    form = ContactForm()

    return render_template("index.html", form=form, year=year)

@app.route("/portfolio")
def portfolio():
    projects = Portfolio.query.all()
    return render_template("portfolio.html", projects=projects, year=year)


@app.route("/portfolio/<int:project>", methods=["POST", "GET"])
def projects(project):
    requested_project = Portfolio.query.get(project)

    return render_template("project-template.html",
                           project=requested_project,
                           year=year
                           )

@app.route("/add_project", methods=["GET", "POST"])
def add_project():
    form = AddNewProjectForm()
    if form.validate_on_submit():
        # Check if a project folder exists, if not, create it
        if not os.path.exists(f"static/images/projects/{form.number.data}/images"):
            os.makedirs(f"static/images/projects/{form.number.data}/images")
        if not os.path.exists(f"static/images/projects/{form.number.data}/gifs"):
            os.makedirs(f"static/images/projects/{form.number.data}/gifs")

        # Save portfolio images
        files_filenames_images = []
        for file in request.files.getlist("image_paths"):
            file_filename = secure_filename(file.filename)
            file.save(os.path.join(f"static/images/projects/{form.number.data}/images", file_filename))
            files_filenames_images.append(file_filename)

        # Save portfolio gifs
        files_filenames_gifs = []
        for file in request.files.getlist("gif_paths"):
            file_filename = secure_filename(file.filename)
            file.save(os.path.join(f"static/images/projects/{form.number.data}/gifs", file_filename))
            files_filenames_gifs.append(file_filename)



        #Create entry for db
        new_project = Portfolio(
            name=form.name.data,
            number=form.number.data,
            level=form.level.data,
            description=form.description.data,
            github=form.github.data,
            focus=form.focus.data,
            c_name=form.c_name.data,
            c_provider=form.c_provider.data,
            image_paths=','.join(files_filenames_images),
            gif_paths=','.join(files_filenames_gifs),
            misc=form.misc.data,
        )
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for("add_project"))

    return render_template("add_project.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)