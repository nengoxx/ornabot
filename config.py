#config.py
#configuration file
from time import sleep, strftime

bot=''

LOG_FILE = '[{}]asgbfBot.log'.format(strftime('%m-%d_%H%M'))

base_dir = '.'

startTime =0

'''
GENERAL TELEGRAM
'''
telegram_bot = ''
telegram_chatId = ''
telegram_token = '5217244645:AAFL9Q_pQQctmA_auxdoUGlHcElGUdFHTq4'

'''
ADB
'''
serial_number = '044d769ff0c7540a'
adb_host='192.168.1.137'
adb_port=5555

'''
AUTOMAT
'''
useCoins=0
useExpPot=0