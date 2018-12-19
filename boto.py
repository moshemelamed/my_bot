"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
import json
import requests
from bs4 import BeautifulSoup



url = ["https://www.theguardian.com/news/datablog/2009/sep/08/baby-names-children-jack-olivia-mohammed",
       "https://www.boldtuesday.com/pages/alphabetical-list-of-all-countries-and-capitals-shown-on-list-of-countries-poster"]
r = requests.get(url[0])
amaizing_people_list = ["moshe", "yoav", "aviram", "ariel","shira","gav","nili","tzofi","avraham","netanel"]


def parse():
    r = requests.get(url[0])
    soup = BeautifulSoup(r.content, 'html.parser')
    data = soup.find_all("tr")
    return data


def time_url():
    r = requests.get(url[1])
    soup = BeautifulSoup(r.content, 'html.parser')
    data = soup.find_all("tr")
    return data

def deal_with_time(time_question):
    for word in time_question:
        country_city = {}
        bot_moov = "confused"
        r_time = time_url()
        for name in r_time:
            if name.text.find(word):
                moshe = name.text.split("\n")
                for i,name in enumerate(moshe):
                    if len(moshe[i]) > 0:
                        country_city[moshe[1]] = moshe[2]
                        bot_moov = "ok"
                        usser_country = word.upper()
                        if usser_country in country_city.keys():
                            return usser_country,country_city[usser_country]


def deal_with_questions(qustion):
    for word in qustion:
        if word.find("capital") >= 0:
            usercounry_and_capital = deal_with_time(qustion)
            bot_answear = "the capital of {0} is {1}".format(usercounry_and_capital[0],usercounry_and_capital[1])
            bot_moov = "afraid"
        if word.find("time") >= 0:
            bot_answear = "time is relativ"
            bot_moov = "bored"
        if word.find("ip") >= 0:
            bot_answear = "35263749"
            bot_moov = "confused"
        if word.find("vote") >= 0:
            bot_answear = "contact 103"
            bot_moov = "crying"
        if word.find("song") >= 0:
            bot_answear = "my favorite song is `doe a dear` from `the sound of music "
            bot_moov = "dancing"
        if word.find("weeks") >= 0:
            bot_answear = "there are 54 weeks in a year"
            bot_moov = "dog"
        if word.find("weather") >= 0:
            bot_answear = "it feels like 24 deg"
            bot_moov = "excited"
        if word.find("calc") >= 0:
            bot_answear = "im not very good at math"
            bot_moov = "giggling"

    return  bot_answear,bot_moov


@route('/', method='GET')
def index():
    return template("chatbot.html")


bot_moov = "inlove"
name = ""
question_string = ""
question_list = []
count = 0
return_messeg = []



@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')
    list_of_messege = user_message.split(" ")
    for word in list_of_messege:
        if word.find("?") >= 0:
            question_string = user_message.replace("?","")
            question_list = question_string.split(" ")
            return_messeg = deal_with_questions(question_list)
            user_message, bot_moov = return_messeg[0],return_messeg[1]
            return json.dumps({"animation": bot_moov, "msg": user_message})
    if user_message.lower() in amaizing_people_list:
        name = user_message
        user_message = "thats a great name!\n{0}, let`s have some fun".format(name)
        bot_moov = "giggling"
    elif count == 0:
        list_of_names = parse()
        bot_moov = "excited"
        name = user_message
        for i,name_words in enumerate(list_of_names):
            if name_words.text.find(user_message.upper()) >= 0:
                user_message = "ok {0}, how can I help you?".format(name)
                continue
            if i == len(list_of_names) - 1:
                user_message = "lets get started, how can I help you?"
        count + 1


    return json.dumps({"animation": bot_moov, "msg": user_message})


@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "inlove", "msg": user_message})


@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')


def main():
    run(host='localhost', port=7000)


if __name__ == '__main__':
    main()
