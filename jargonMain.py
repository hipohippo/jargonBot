# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 22:20:33 2021

@author: weiwe
"""
import logging
import requests
import json
import re

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
regex = re.compile('[^a-zA-Z0-9]')
with open("../../tgBotToken/jargonBot.token") as f:
    jargon_bot_token = f.readline()[:-1] 

def strToJson(jstr):
    jbean = json.loads(jstr)
    result = ''

    for data in jbean:
        result = result + data['name']+'\n'
        
        if 'trans' in data:
            for dt in data['trans']:
                result = result + dt + '\n'
        
        if 'inputting' in data:
            if 0 < len(data['inputting']):
                result = result + '可能是\n'
                for di in data['inputting']:
                    result = result + di + '\n'
            else:
                result = result + '尚未录入\n'
    return(result[:-1])
    
def clean(word):
    return regex.sub('', word)
    
    
def lookup(word):
    if word=="pipa":
        return "in Paris!"
    word = clean(word)
    response = requests.post(url='https://lab.magiconch.com/api/nbnhhsh/guess', data={"text":word}).text
    return (" ".join(strToJson(response).replace("\n", " ").split(" ")[1:]))

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text("Hi! Usage: '/lookup mdzz'")

def botlookup(update, context):
    #lookup(word)
    word = update.message.text.split(" ")
    if (len(word)<=1):
        update.message.reply_text("nothing to look up")
    else:
        update.message.reply_text(lookup(word[1]))

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(jargon_bot_token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("lookup", botlookup))
    
    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text, echo))
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    print("here")
    main()
