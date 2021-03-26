import io
import os
import telebot
from PIL import Image, ImageDraw , ImageFont

TOKEN = "token"
bot = telebot.TeleBot(TOKEN)

def text_only(img:object, povtorka:bool)-> object:
    if povtorka:
        font = ImageFont.truetype("Arial.ttf", size = 50)
        draw = ImageDraw.Draw(img)
        draw.text((100,150), "Повторний Курс", fill = 'red',font = font)
        return img
    else:
        font = ImageFont.truetype("Arial.ttf", size = 75)
        draw = ImageDraw.Draw(img)
        draw.text((170,140), "Survived", fill = 'green',font = font)
        return img

def pillow_to_bytes(image:Image):
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format=image.format)
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr

def bytes_to_pillow(byte: bytes):
    pillow = Image.open(io.BytesIO(byte))
    return pillow

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Hello, freeloader! Send me your photo")

@bot.message_handler(func=lambda message: True)
def ask_photo(message):
	bot.send_message(message.chat.id, "Send me your photo, please.")

@bot.message_handler(content_types=['photo'])
def photo(message):
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)

    res = pillow_to_bytes(text_only(bytes_to_pillow(downloaded_file), 1))

    bot.send_photo(message.chat.id, res)

bot.polling()