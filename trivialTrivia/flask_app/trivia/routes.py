import base64,io
from io import BytesIO
from flask import Blueprint, render_template, url_for, redirect, request, flash, session
from flask_login import current_user

from ..forms import TriviaGuessForm, QuestionSubmissionForm
from ..models import User, Question
from ..trivia import trivia_api_utils

trivia = Blueprint("trivia", __name__)
trivia.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
""" ************ Helper for pictures uses username to get their profile picture************ """
def get_b64_img(username):
    user = User.objects(username=username).first()
    bytes_im = io.BytesIO(user.profile_pic.read())
    image = base64.b64encode(bytes_im.getvalue()).decode()
    return image

first_load = True
""" ************ View functions ************ """
@trivia.route("/", methods=["GET", "POST"])
def index():
    global first_load
    if first_load:
        print("INIT!")
        session['score'] = 0
        session['question_id'] = 0
        session['questions'], session['answers'] = trivia_api_utils.get_batch_question()
        first_load = False
    form = TriviaGuessForm()
    question, answer = session['questions'][session['question_id']], session['answers'][session['question_id']]
    
    if request.method == "POST":
        
        if form.validate_on_submit():
            session['question_id'] += 1
            print(answer)
            print(question)
            print(session['question_id'])
            if form.guess.data.lower() == answer.lower():
                flash("Correct!")
                session['score'] += 1
                if current_user.is_authenticated:  
                    if session['score'] > current_user.high_score:
                        current_user.high_score = session['score']
                        current_user.save()
            else:
                flash("Incorrect!")
                session.modified = True
            return redirect(url_for("trivia.index"))
    return render_template("index.html", form=form, question=question, answer=answer, num_correct=session['score'])

@trivia.route("/question_submission", methods=["GET", "POST"])
def question_submission():
    form = QuestionSubmissionForm()
    if form.validate_on_submit():
        question = Question(
            creator=current_user._get_current_object(),
            question=form.question.data,
            answer=form.answer.data,
            category=form.category.data
        )

        question.save()

        return redirect(request.path)
    return render_template(
        "question_submission.html", form=form
    )


#statistics on account links here, refactor to individual user statistics
@trivia.route("/user/<username>")
def user_detail(username):
    #user = find first match in db
    
    user = User.objects(username=username).first()
    #img = get_b64_img(user.username) use their username for helper function
    if user is None:
        return render_template("user_detail.html", error ="Hi", user=None, image=None)
    return render_template("user_detail.html", user=user, image=get_b64_img(user.username))


@trivia.route("/leaderboard")
def leaderboard():
    users = list(User.objects())
    users.sort(key=lambda x: x.high_score, reverse=True)

    return render_template("leaderboard.html", users=users)