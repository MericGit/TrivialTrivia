import base64,io
from io import BytesIO
from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user

from .. import movie_client
from ..forms import MovieReviewForm, TriviaGuessForm
from ..models import User, Review
from ..utils import current_time
from ..trivia import trivia_api_utils

movies = Blueprint("movies", __name__)
""" ************ Helper for pictures uses username to get their profile picture************ """
def get_b64_img(username):
    user = User.objects(username=username).first()
    bytes_im = io.BytesIO(user.profile_pic.read())
    image = base64.b64encode(bytes_im.getvalue()).decode()
    return image

""" ************ View functions ************ """

Correct = 0
@movies.route("/", methods=["GET", "POST"])
def index():
    Question, Answer = trivia_api_utils.get_single_question()
    form = TriviaGuessForm()
    print("Question:", Question)
    print("Answer:", Answer)

    if form.validate_on_submit():
        print("User's Guess:", form.guess.data)
        if form.guess.data == Answer:
            print("Correct!")
            global Correct
            Correct += 1
        #return redirect(url_for("movies.index"))
    #form.guess.data = ""
    return render_template("index.html", form=form, question=Question, answer=Answer, num_correct = Correct)


@movies.route("/search-results/<query>", methods=["GET"])
def query_results(query):
    try:
        results = movie_client.search(query)
    except ValueError as e:
        return render_template("query.html", error_msg=str(e))

    return render_template("query.html", results=results)


@movies.route("/movies/<movie_id>", methods=["GET", "POST"])
def movie_detail(movie_id):
    try:
        result = movie_client.retrieve_movie_by_id(movie_id)
    except ValueError as e:
        return render_template("movie_detail.html", error_msg=str(e))

    form = MovieReviewForm()
    if form.validate_on_submit():
        review = Review(
            commenter=current_user._get_current_object(),
            content=form.text.data,
            date=current_time(),
            imdb_id=movie_id,
            movie_title=result.title,
            image=get_b64_img(current_user.username)
        )

        review.save()

        return redirect(request.path)

    reviews = Review.objects(imdb_id=movie_id)

    return render_template(
        "movie_detail.html", form=form, movie=result, reviews=reviews
    )


@movies.route("/user/<username>")
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