import json
import requests
import time
import urllib
import os
from dbhelper import DBhelper

db = DBhelper()
token = os.environ['TELEGRAM_TOKEN']

url = "https://api.telegram.org/bot{}/".format(token)

def get_url(URL):
    response = requests.get(URL)
    content = response.content.decode("utf8")
    return content
def get_json_from_url(URL):
    content = get_url(URL)
    js = json.loads(content)
    return js
def get_updates(offset=None):
    Url = url + "getUpdates?timeout=100"
    if offset:
        Url += "&offset={}".format(offset)
    js = get_json_from_url(Url)
    return js
def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    URL = url + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(URL)
    return
def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)
def register_db(chat_id,Name,Id):
    db.add_item([chat_id,Name,Id])
    return
def isUpdate(updates):
    last = get_last_update_id(updates)
    counter = 0
    while counter <= 60 :
        refresh = get_updates(last)
        if last != get_last_update_id(refresh):
            return True
        counter += 1
        time.sleep(1)
    return False
def register(updates):
    chat_id = updates["result"]["message"]["chat"]["id"]
    Name = ""
    ID = ""
    send_message("نام و نام خانوادگی خود را وارد کنید",chat_id)
    if isUpdate :
        Name = updates["result"]["message"]["text"]
    else:
        return False
    send_message(" شماره دانشجویی خود را وارد کنید",chat_id)
    if isUpdate :
        ID = updates["result"]["message"]["text"]
    else:
        return False
    register_db(chat_id,Name,ID)
    return True
def main():
    db.setup()
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            text = updates["result"]["message"]["text"]
            chat_id = updates["result"]["message"]["chat"]["id"]
            if text == "/start":
                send_message("به ربات ثبت نام خوش امدین",chat_id)
            elif text == "/reg":
                if register(updates) :
                    send_message("😉ثبت نام شما انجام شد",chat_id)
            else:
                send_message("پیام شما قابل مفهوم نیست",chat_id)
        time.sleep(0.5)