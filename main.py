import telebot
from decouple import config
import random


API_KEY = config('API_KEY')
motivation_bot = telebot.TeleBot(API_KEY)
motiv8URL = "https://type.fit/api/quotes"

# creates a command that listens for a string called "greet"
@motivation_bot.message_handler(commands=['hello'])
def greet(message):
    motivation_bot.reply_to(message, 'Hey! How are you?')


def motivate_me(message):
    r = message.text.split()
    if len(r) >= 2 and r[0].lower() == "motivate" and r[1].lower() == "me":
        return True
    else:
        return False


# SENDS MOTIVATIONAL QUOTE
@motivation_bot.message_handler(func=motivate_me)
def get_quote(message):
    # reads quotes from txt file
    try:
        with open("quotes_list.txt", encoding="utf-8") as file:
            data = file.readlines()
            rand_num = random.randint( 0, (len(data) - 1) )
            # gets random quote
            quote = data[rand_num]
            motivation_bot.send_message(message.chat.id,
                             f'{quote}')
    except:
        motivation_bot.send_message(message.chat.id, 'error with retrieving quote.')

def add_quote_txtfile(message):
    try:
        r = message.text.split()
        r = [word.lower() for word in r]
        if r[0] == "add" and r[1] == 'new' and r[2] == 'quote':
            return True
        else:
            return False
    except:
        motivation_bot.send_message(message.chat.id, 'error with adding quote.')


# CREATE HANDLER FOR ADDING TO TXT FILE
@motivation_bot.message_handler(func=add_quote_txtfile)
def add_quote(message):
    data = message.text.split()
    sentence_list = []

    try:
        # checks if data message is a sentence and not blank
        if len(data) > 5:
            for each_word in data[3:]:
                sentence_list.append(each_word)
            # turns list to
            sentence_joined = " ".join(sentence_list)
            # APPENDS cleaned quote data to txt file
            with open("quotes_list.txt", mode="a", encoding="utf-8") as file:
                file.write(f"{sentence_joined}\n")

            motivation_bot.send_message(message.chat.id,
                             f'quote successfully added')
        else:
            motivation_bot.send_message(message.chat.id,
                             f"your quote is too short, can't add it sorry")
    except:
        motivation_bot.send_message(message.chat.id, 'error with adding quote.')


# keeps on running the bot to check for commands

motivation_bot.polling(interval=3)