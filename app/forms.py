from flask_wtf import FlaskForm
from wtforms import (StringField,
                     PasswordField,
                     BooleanField,
                     SubmitField,
                     FileField,
                     SelectField)
from wtforms.validators import (ValidationError,
                                DataRequired,
                                Email,
                                EqualTo)
from flask_wtf.file import (FileRequired,
                            FileAllowed)

from app.models import (User,
                        Project)
from config import ALLOWED_EXTENSIONS

__author__ = 'mpolensek'
# Documentation is like sex.
# When it's good, it's very good.
# When it's bad, it's better than nothing.
# When it lies to you, it may be a while before you realize something's wrong.


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Repeat Password", validators={DataRequired(), EqualTo('password')})
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Please use a different username.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Please use a different email address.")


def project_choices():
    projects = Project.query.all()
    projects_choices = []
    for project in projects:
        projects_choices.append((project.id, project.name))
    return projects_choices

pairs = project_choices()


class UploadForm(FlaskForm):
    project = SelectField("Project", choices=pairs, validators=None, coerce=int)
    title = StringField("Document title", validators=[DataRequired()])
    revision = StringField("Revision", validators=[DataRequired()], default=1)
    file = FileField("File", validators=[FileRequired(),
                                         FileAllowed(ALLOWED_EXTENSIONS, "File type not supported")])
    submit = SubmitField("Upload")


