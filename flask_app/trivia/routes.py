import base64,io
from io import BytesIO
from flask import Blueprint, render_template, url_for, redirect, request, flash, session
from flask_login import current_user

from ..forms import TriviaGuessForm, QuestionSubmissionForm
from ..models import User, Question
from ..trivia import trivia_api_utils
import logging
import time

trivia = Blueprint("trivia", __name__)
trivia.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
""" ************ Helper for pictures uses username to get their profile picture************ """
def get_b64_img(username):
    user = User.objects(username=username).first()
    bytes_im = io.BytesIO(user.profile_pic.read())
    image = base64.b64encode(bytes_im.getvalue()).decode()
    return image

""" ************ View functions ************ """
@trivia.before_request
def before_request():
    session['start_time'] = time.time()

@trivia.route("/", methods=["GET", "POST"])
def index():
    form = TriviaGuessForm()
    if 'mode' not in session:
        session.clear()
        session['mode'] = "mongo"
        session['score'] = 0
        session['questions_seen'] = 0
        session['question_id'] = 0
        session['mongo_question_id'] = 0
        session['questions'], session['answers'] = trivia_api_utils.get_batch_question()
        session['log'] = []
        session['prev_time'] = time.time()
        #mongo_questions = []
        #mongo_answers = []
        #for q in Question.objects.filter(category="470"):
        #    mongo_questions.append(q.question)
        #    mongo_answers.append(q.answer)
        #session['mongo_questions'] = mongo_questions
        #session['mongo_answers'] = mongo_answers
        session['first_load'] = False
    mongo_questions = []
    mongo_answers = []
    for q in Question.objects.filter(category="470"):
        mongo_questions.append(q.question)
        mongo_answers.append(q.answer)
    if session['mode'] == "api":
        question, answer = session['questions'][session['question_id']], session['answers'][session['question_id']]
    elif session['mode'] == "mongo":
        question, answer = mongo_questions[session['mongo_question_id']], mongo_answers[session['mongo_question_id']]
    if request.method == "POST":
        if 'toggle_mode' in request.form:
            if session['mode'] == 'mongo':
                session['mode'] = 'api'
            elif session['mode'] == 'api':
                session['mode'] = 'mongo'
        if form.validate_on_submit():
            stop_time = time.time()
            if session['mode'] == "api":
                session['question_id'] += 1
            elif session['mode'] == "mongo":
                session['mongo_question_id'] += 1
                if session['mongo_question_id'] >= len(mongo_questions):
                    session['mode'] = "api"
                    session['mongo_question_id'] = 0
            print(answer)
            print(question)
            print(session['question_id'])
            session['questions_seen'] += 1
            if current_user.is_authenticated:  
                current_user.questions_seen += 1
                current_user.save()

            session['log'].append((session['mongo_question_id'], form.guess.data.lower(), answer.lower(), (stop_time - session['prev_time']).__round__(2))) 
            session['prev_time'] = stop_time
            if form.guess.data.lower() == answer.lower():
                session['score'] += 1
                
                if current_user.is_authenticated:  
                    current_user.questions_correct += 1
                    current_user.save()
                    if session['score'] > current_user.high_score:
                        current_user.high_score = session['score']
                        current_user.save()
            else:
                flash("Incorrect!")
                session.modified = True
            return redirect(url_for("trivia.index"))
    return render_template("index.html", form=form, question=question, answer=answer, num_correct=session['score'], seen = session['questions_seen'], mode=session['mode'],log = session['log'])

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
def user_statistics(username):
    #user = find first match in db
    
    user = User.objects(username=username).first()
    #img = get_b64_img(user.username) use their username for helper function
    if user is None:
        return render_template("user_statistics.html", error ="Hi", user=None, image=None)
    questions = Question.objects(creator=user)
    return render_template("user_statistics.html", user=user, questions = questions, image=get_b64_img(user.username))


@trivia.route("/leaderboard")
def leaderboard():
    users1 = list(User.objects())
    users1.sort(key=lambda x: x.high_score, reverse=True)
    users2 = list(User.objects())
    users2.sort(key=lambda x: x.questions_correct, reverse=True)
    users3 = list(User.objects())
    users3.sort(key=lambda x: x.questions_seen, reverse=True)
    users4 = list(User.objects())
    users4.sort(key=lambda x: 0 if x.questions_seen == 0 else (x.questions_correct / x.questions_seen), reverse=True)
    return render_template("leaderboard.html", users1=users1, users2 = users2, users3 = users3, users4 = users4)