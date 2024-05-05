from ast import Pass
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, SelectField
from wtforms.validators import (
    InputRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
)


from .models import User

class TriviaGuessForm(FlaskForm):
    guess = StringField(
        "Guess", validators=[InputRequired(), Length(min=1, max=100)]
    )
    submit = SubmitField("Submit Guess")

class QuestionSubmissionForm(FlaskForm):
    question = StringField(
        "Question", validators=[InputRequired(), Length(min=1, max=500)]
    )
    answer = StringField(
        "Answer", validators=[InputRequired(), Length(min=1, max=100)]
    )
    category = SelectField(
        "Category", validate_choice=True,
        choices=['General Knowledge','Entertainment: Books','Entertainment: Film','Entertainment: Music','Entertainment: Musicals & Theatres',
        'Entertainment: Television','Entertainment: Video Games','Entertainment: Board Games','Science & Nature','Science: Computers'
        'Science: Mathematics','Mythology','Sports','Geography','History','Politics','Art','Celebrities','Animals','Vehicles',
        'Entertainment: Comics','Science: Gadgets','Entertainment: Japanese Anime & Manga','Entertainment: Cartoon & Animations']
    )
    submit = SubmitField("Submit Question")

class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
    )
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[InputRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError("Email is taken")


# TODO: implement fields
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=40)])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")


# TODO: implement
class UpdateUsernameForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=40)])
    submit_username = SubmitField("Update Username") 

    # TODO: implement
    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")

# TODO: implement
class UpdateProfilePicForm(FlaskForm):
    picture =  FileField("Profile Picture", validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    submit_picture = SubmitField("Update")
