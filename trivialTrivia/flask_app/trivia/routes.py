import base64,io
from io import BytesIO
from flask import Blueprint, render_template, url_for, redirect, request, flash, session
from flask_login import current_user

from .. import movie_client
from ..forms import TriviaGuessForm, QuestionSubmissionForm
from ..models import User, Question, Review
from ..utils import current_time
from ..trivia import trivia_api_utils

trivia = Blueprint("movies", __name__)
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
            return redirect(url_for("movies.index"))
    return render_template("index.html", form=form, question=question, answer=answer, num_correct=session['score'])

@trivia.route("/question_submission", methods=["GET", "POST"])
def add_question():
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

# @trivia.route("/movies/<movie_id>", methods=["GET", "POST"])
# def movie_detail(movie_id):
#     try:
#         result = movie_client.retrieve_movie_by_id(movie_id)
#     except ValueError as e:
#         return render_template("movie_detail.html", error_msg=str(e))

#     form = MovieReviewForm()
#     if form.validate_on_submit():
#         review = Review(
#             commenter=current_user._get_current_object(),
#             content=form.text.data,
#             date=current_time(),
#             imdb_id=movie_id,
#             movie_title=result.title,
#             image=get_b64_img(current_user.username)
#         )

#         review.save()

#         return redirect(request.path)

#     reviews = Review.objects(imdb_id=movie_id)

#     return render_template(
#         "movie_detail.html", form=form, movie=result, reviews=reviews
#     )


#statistics on account links here, refactor to individual user statistics
@trivia.route("/user/<username>")
def user_detail(username):
    #uncomment to get review image
    #user = find first match in db
    
    user = User.objects(username=username).first()
    #img = get_b64_img(user.username) use their username for helper function
    if user is None:
        return render_template("user_detail.html", error ="Hi", user=None, reviews=None, image=None)
    reviews = Review.objects(commenter=user)
    return render_template("user_detail.html", user=user, reviews=reviews, image=get_b64_img(user.username))
"""
    try:
        results = movie_client.search(query)
    except ValueError as e:
        return render_template("query.html", error_msg=str(e))
"""