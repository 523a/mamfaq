#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 01:04:46 2020

@author: r
"""
#pip install -q deeppavlov

import requests
from time import sleep
from deeppavlov.deprecated.skills.similarity_matching_skill import SimilarityMatchingSkill


faq_skill = SimilarityMatchingSkill(data_path = 'All.csv',
                              x_col_name = 'Question', 
                              y_col_name = 'Answer',
                              save_load_path = './model_All',
                              config_type = 'tfidf_autofaq',
                              train = True)


url = "https://api.telegram.org/.../"


#def get_updates_json(request):  
#    response = requests.get(request + 'getUpdates')
#    return response.json()

def get_updates_json(request):  
    params = {'timeout': 100, 'offset': None}
    response = requests.get(request + 'getUpdates', data=params)
    return response.json()

def last_update(data):  
    results = data['result']
    total_updates = len(results) - 1
    return results[total_updates]

def get_chat_id(update):  
    chat_id = update['message']['chat']['id']
    return chat_id

def send_mess(chat, text):  
    params = {'chat_id': chat, 'text': text}
    response = requests.post(url + 'sendMessage', data=params)
    return response

def main():  
    out = "Здравствуйте.Задайте вопрос по здоровью."
    update_id = last_update(get_updates_json(url))['update_id']
    while True:
        if update_id == last_update(get_updates_json(url))['update_id']:

           send_mess(get_chat_id(last_update(get_updates_json(url))), out)
           update_id += 1
           last_mes = last_update(get_updates_json(url))['message']['text']
           #print(last_mes)
           out=faq_skill([last_mes], [], [])

        sleep(3)       

if __name__ == '__main__':  
    main()
