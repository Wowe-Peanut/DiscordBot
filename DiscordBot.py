#Object Identification Libraries
import cv2
import matplotlib.pyplot as plt
import cvlib as cv
from cvlib.object_detection import draw_bbox
import os
import urllib
import numpy as np

#Bot Libraries
import discord
from dotenv import load_dotenv
import emoji
import random
import re





intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
channel_id = 979609584190763030
trigger_words = ["model", "train", "tram", "locomotive", "railcar", "railway", "railroad", "subway", "choochoo"]

load_dotenv()
token = os.getenv("token")


def contains_train(url):
    #Get image from url
    hdr = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' }
    req = urllib.request.Request(url, headers=hdr)
    res = urllib.request.urlopen(req)
    arr = np.asarray(bytearray(res.read()), dtype=np.uint8)
    img = cv2.imdecode(arr, -1)
    
    
    #Some PNGS have 4 channels which breaks the objection detection
    if len(img.shape) > 2 and img.shape[2] == 4:
        #convert the image from RGBA2RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    #Object Detection
    bbox, label, conf = cv.detect_common_objects(img)

    for word in trigger_words:
        if word in label:
            output_image = draw_bbox(img, bbox, label, conf)
            return True, cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB)
            
            

    return False, None

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')



@client.event
async def on_message(message):
    if message.author != client.user:
      
      #Emojis --> Text and remove all non letter characters and spaces
      msg = "".join([l for l in emoji.demojize(str(message.content)).lower().replace(" ", "") if l.isalpha()])
      for trigger in trigger_words:
        if trigger in msg:
          await message.reply("NO TRAINS!")
          return
      
      #Checks if message is has file attachments and links within the message text itself
      urls = [attachment.url for attachment in message.attachments] + re.findall(r'(https?://\S+)', str(message.content))
      
      
      

      #print(str(message.content), msg, urls)
      
      for url in urls:
        #Object Identification AI
        trigger, image = contains_train(url)
        if trigger:
            cv2.imwrite("temp.jpg", cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
            await message.reply("NO TRAINS!")
            await message.channel.send(file=discord.File('temp.jpg'))
            os.remove("temp.jpg")
            return

        #Words in url
        for trigger in trigger_words:
          if trigger in url:
            await message.reply("NO TRAINS!")
            return
      

client.run(token)


