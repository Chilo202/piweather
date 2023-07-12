from bot.bot_setup import Bot


bot = Bot("start")
bot.bot_start('This is Start message',btn1_message='This is first ',btn2_message='This is second')
bot.bot_reply('It is standart answer')
bot.weather_send()
bot.bot_pull()