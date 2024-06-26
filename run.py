from flask_app import create_app
from flask import session
from flask_app.models import Question
from flask_app.trivia import trivia_api_utils
import time
app = create_app()
@app.before_first_request
def before_first_request():
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
    #for q in Question.objects().filter(category="470"):
    #    mongo_questions.append(q.question)
    #    mongo_answers.append(q.answer)
    #session['mongo_questions'] = mongo_questions
    #session['mongo_answers'] = mongo_answers
    first_load = False

if __name__ == "__main__":
    app.run()