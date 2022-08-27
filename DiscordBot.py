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

#Object Detection
"""
hdr = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' }
url = "https://cdn.discordapp.com/attachments/979609584190763030/1013196042155597935/apple.jpeg"

req = urllib.request.Request(url, headers=hdr)
res = urllib.request.urlopen(req)
arr = np.asarray(bytearray(res.read()), dtype=np.uint8)
img = cv2.imdecode(arr, -1)


bbox, label, conf = cv.detect_common_objects(img)

for l, c in zip(label, conf):
    print(f"Detected object: {l} with confidence level of {c}\n")

output_image = draw_bbox(img, bbox, label, conf)
output_image = cv2.cvtColor(output_image, cv2.COLOR_RGB2BGR)
plt.imshow(output_image)
plt.show()
"""

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
channel_id = 979609584190763030
trigger_words = ["model", "train", "tram", "locomotive", "railcar", "railway", "railroad", "subway"]

load_dotenv()
token = os.getenv("token")


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')



@client.event
async def on_message(message):
    if message.author != client.user and message.channel.id == channel_id:
      print(str(message.content))
      
      #Emojis --> Text and remove all non letter characters and spaces
      msg = "".join([l for l in emoji.demojize(str(message.content)).lower().replace(" ", "") if l.isalpha()])
      for trigger in trigger_words:
        if trigger in msg:
          await message.reply("NO TRAINS!")
          return
      
      #Checks if message is has file attachments
      attachment_urls = [attachment.url for attachment in message.attachments]
      for url in attachment_urls:
        #Words in url
        for trigger in trigger_words:
          if trigger in url:
            await message.reply("NO TRAINS!")
            return

        #Reverse Image Search
        pass
            
      #Links
      
      
      print(msg, attachment_urls)
      

      

      

client.run(token)
