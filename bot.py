import io
import os
import telebot
import numpy as np
from PIL import Image, ImageDraw , ImageFont
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import tensorflow.keras as keras

TOKEN = "TOKEN"

bot = telebot.TeleBot(TOKEN)
board = Image.open('img/b.jpg')
survived = Image.open('img/survived.jpeg')
model = keras.models.load_model("model.h5")
train_datagen = ImageDataGenerator(horizontal_flip=True,
                                   vertical_flip=False,
                                   rescale=1./255,)

def pillow_to_bytes(pillow: Image):
    byte = io.BytesIO()
    pillow.save(byte, format=pillow.format)
    byte = byte.getvalue()
    return byte

def bytes_to_pillow(byte: bytes):
    pillow = Image.open(io.BytesIO(byte))
    return pillow

def sizing(img: Image, povtorka:bool):
    img_width, img_height = img.size
    if povtorka:
        b_width, b_height = board.size
        return img_width/ (b_width/2) , img_height/ (b_height/2)
    else:
        s_width, s_height = survived.size
        return img_width/ (s_width/2) , img_height/ (s_height/1.5)

def verdict(img: Image, povtorka:bool):
    if povtorka:
        width, height = img.size
        k1,k2 = sizing(img,povtorka)
        img = img.resize((int(width/k1), int(height/k2)))
        board.paste(img,(125,150))
        return board
    else:
        width, height = img.size 
        k1,k2 = sizing(img,povtorka)
        img = img.resize((int(width/k1), int(height/k2)))
        survived.paste(img,(200,130))
        return survived

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

    with open("Test/test1/image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)
    
    test = train_datagen.flow_from_directory("Test",
                                            class_mode="binary",
                                            target_size=(96, 96),
                                            batch_size=32)
    pred = np.argmax(model.predict(test), axis = 1)

    res = pillow_to_bytes(verdict(bytes_to_pillow(downloaded_file), pred))

    bot.send_photo(message.chat.id, res)

bot.polling()