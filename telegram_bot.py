import traceback

import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
import time

import config
import func
import automat

'''
Commands:
'''

def setupTelegram():
    config.telegram_bot = telegram.Bot(token=config.telegram_token)
    print(config.telegram_bot.get_me())

    updater = Updater(token=config.telegram_token)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    stop_handler = CommandHandler('stop', stop)
    screenshot_handler = CommandHandler('screen', screenshot)
    pause_handler = CommandHandler('pause', pause)
    lock_handler = CommandHandler('lock', lock)
    zoomout_handler = CommandHandler('zoom', zoomout)
    battery_handler = CommandHandler('battery', getBattery)
    coin_handler = CommandHandler('coin', toggleCoins)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(stop_handler)
    dispatcher.add_handler(screenshot_handler)
    dispatcher.add_handler(pause_handler)
    dispatcher.add_handler(lock_handler)
    dispatcher.add_handler(zoomout_handler)
    dispatcher.add_handler(battery_handler)
    dispatcher.add_handler(coin_handler)

    updater.start_polling()


def start(update, context):
    func.relaunchApp(stop=False)
    config.telegram_chatId=update.message.chat_id
    config.telegram_bot.send_message(chat_id=update.message.chat_id, text="Orna starting...")

def stop(update, context):
    func.relaunchApp(start=False)
    config.telegram_chatId=update.message.chat_id
    config.telegram_bot.send_message(chat_id=update.message.chat_id, text="Orna closed!")


def sendTelegramMsg(msg):
    config.telegram_bot.send_message(chat_id=config.telegram_chatId, text=msg)


def pause(update, context):
    func.toggleBot(None)
    config.telegram_chatId=update.message.chat_id
    config.telegram_bot.send_message(chat_id=config.telegram_chatId, text='Botting: '+str(func.botting))
    
    
def lock(update, context):
    func.lockPhone()
    config.telegram_chatId=update.message.chat_id
    config.telegram_bot.send_message(chat_id=config.telegram_chatId, text='Lock toggled')

def zoomout(update, context):
    automat.zoomOut()
    config.telegram_chatId=update.message.chat_id
    config.telegram_bot.send_message(chat_id=config.telegram_chatId, text='Zoomed out')

def sendTelegramScreenShot():
    try:
        config.telegram_bot.send_photo(chat_id=config.telegram_chatId, photo=open('screen/screen.png', 'rb'))
    except Exception:
        traceback.print_exc()
        pass
    
def screenshot(update,context):
    try:
        func.saveScreenshot()
        sendTelegramScreenShot()

    except Exception:
        traceback.print_exc()
        pass
    
def getBattery(update, context):
    config.telegram_chatId=update.message.chat_id
    config.telegram_bot.send_message(chat_id=config.telegram_chatId, text=str(func.getBattery()))

def toggleCoins(update, context):
    if (config.useCoins==1):
        config.useCoins=0
    else:
        config.useCoins=1
    config.telegram_chatId=update.message.chat_id
    config.telegram_bot.send_message(chat_id=config.telegram_chatId, text='Use coins: '+str(config.useCoins))
