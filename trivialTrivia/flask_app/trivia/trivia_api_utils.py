import requests 
import json
import base64

def base64ToString(b):
    return base64.b64decode(b).decode('utf-8')

def get_single_question():
    res = requests.get('https://opentdb.com/api.php?amount=1&encode=base64')
    response = res.json()
    if response['response_code'] != 0:
        return("API Error", "API Error")
    #print(response['results'][0]['question'])
    print(base64ToString(response['results'][0]['correct_answer']))
    #print(response['results'][0]['incorrect_answers'])
    return (base64ToString(response['results'][0]['question']), base64ToString(response['results'][0]['correct_answer']))