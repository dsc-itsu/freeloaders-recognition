import telebot

# Read token from file
f = open("key.ini", "r")
TOKEN = f.readline()
f.close()

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Hello, freeloader! Send me your photo")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.send_message(message.chat.id, "Send me your photo, please.")

@bot.message_handler(content_types=['photo'])
def photo(message):
    print('message.photo =', message.photo)
    fileID = message.photo[-1].file_id
    print('fileID =', fileID)
    file_info = bot.get_file(fileID)
    print('file.file_path =', file_info.file_path)
    bot.send_message(message.chat.id,
                    '**message.photo** = ' + str(message.photo)+'\n\n**fileID** = '+ str(fileID) +'\n\n**file.file_path** = ' + str(file_info.file_path))
    
    downloaded_file = bot.download_file(file_info.file_path)
    bot.send_photo(message.chat.id, downloaded_file, caption="Povtorka!")

#     with open("image.jpg", 'wb') as new_file:
#         new_file.write(downloaded_file)

bot.polling()