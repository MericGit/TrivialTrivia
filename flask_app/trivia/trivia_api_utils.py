import requests 
import json
import base64


def base64ToString(b):
    return base64.b64decode(b).decode('utf-8')

def get_batch_question():
    res = requests.get('https://opentdb.com/api.php?amount=100&encode=base64')
    response = res.json()
    print(response['response_code'])
    if response['response_code'] != 0:
        print("NO question found")
        return("API Error", "API Error")
    questions = []
    answers = []
    for result in response['results']:
        questions.append(base64ToString(result['question']))
        answers.append(base64ToString(result['correct_answer']))
    return questions, answers        
    
