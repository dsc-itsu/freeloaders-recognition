import telebot
from PIL import Image, ImageDraw , ImageFont

# Read config from file
with open('config.ini', "r") as f:
    TOKEN = f.readline()

bot = telebot.TeleBot("")

board = Image.open('img/b.jpg')
survived = Image.open('img/survived.jpeg')

def frame_only(img:object, povtorka:bool):
    if povtorka:
        width, height = img.size 
        img = img.resize((int(width/2), int(height/2)))
        board.paste(img,(100,150))
        return board
    else:
        width, height = img.size 
        img = img.resize((int(width/1.5), int(height/1.5)))
        survived.paste(img,(200,130))
        return survived
    
def verdict(img:object, povtorka:bool):
    if povtorka:
        width, height = img.size 
        img = img.resize((int(width/2), int(height/2)))
        board.paste(img,(100,150))
        return board
    else:
        width, height = img.size 
        img = img.resize((int(width/1.5), int(height/1.5)))
        survived.paste(img,(200,130))
        return survived

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Hello, freeloader! Send me your photo")

@bot.message_handler(commands=['test'])
def test(message):
	bot.reply_to(message, "test")

@bot.message_handler(func=lambda message: True)
def ask_photo(message):
	bot.send_message(message.chat.id, "Send me your photo, please.")

@bot.message_handler(content_types=['photo'])
def photo(message):
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    bot.send_message(message.chat.id, f'file_path = {file_info.file_path}')

    downloaded_file = bot.download_file(file_info.file_path)
    
    with open("image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)
    
    in_img = Image.open('image.jpg')
    out_img = frame_only(in_img,1)
    out_img.save('out.jpg')
    
    with open('out.jpg', 'rb') as f:
        byte_im = f.read()
    
    
    bot.send_photo(message.chat.id, byte_im)
#     print(type())

bot.polling()