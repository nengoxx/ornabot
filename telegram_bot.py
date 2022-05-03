import traceback

import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
import time

import config
import func

'''
Commands:
/start - demo
/screen - screenshots 1st instance
/pause - pauses the bot 
/qch <mode> - changes quest or gw quest mode to 'mode'
/berries - changes spam usage of berries 
/capcha <capcha> - inputs 'capcha' as the captcha text in the verification dialog
/vpause - pauses the bot after verification has triggered
'''

def setupTelegram():
    config.telegram_bot = telegram.Bot(token=config.telegram_token)
    print(config.telegram_bot.get_me())

    updater = Updater(token=config.telegram_token)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    # screenshot_handler = CommandHandler('screen', screenshot)
    pause_handler = CommandHandler('pause', pause)

    dispatcher.add_handler(start_handler)
    # dispatcher.add_handler(screenshot_handler)
    dispatcher.add_handler(pause_handler)

    updater.start_polling()


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


def sendTelegramMsg(msg):
    config.telegram_bot.send_message(chat_id=config.telegram_chatId, text=msg)


def pause(bot, update):
    func.toggleBot()
    config.telegram_bot.send_message(chat_id=config.telegram_chatId, text='Botting: '+str(func.botting))
    
# def sendTelegramScreenShot():
#     try:
#         config.telegram_bot.send_photo(chat_id=config.telegram_chatId, photo=open('screen/screen.png', 'rb'))
#     except Exception:
#         traceback.print_exc()
#         pass
    
# def screenshot(bot, update):
#     try:
#         functions.saveScreenshot(driver)
#         sendTelegramScreenShot()

#     except Exception:
#         traceback.print_exc()
#         pass