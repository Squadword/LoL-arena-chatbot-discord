import discord
from dotenv import load_dotenv
import os
import random
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests
from matplotlib import font_manager

# Request all the champion data from Riot's API
champ_r = requests.get("http://ddragon.leagueoflegends.com/cdn/14.10.1/data/en_US/champion.json").json()
# font = ImageFont.truetype("Gidole-Regular.ttf", 20)

# Create a list of all the champions
champs = []
for i in champ_r['data']:
    champs.append(i)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Notify when the bot is online
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

# Respond to messages
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Send GIF related to arena if somebody says arena
    if message.content.startswith('arena'):     
        li = ['https://tenor.com/view/sand-summer-beach-relax-gif-18439176276112077454',
              'https://tenor.com/view/league-of-legends-arena-hop-on-arena-2v2v2v2-lich-king-gif-7102200729794479960']  
        r_gif = random.sample(li, 1)[0]
        await message.channel.send(r_gif)

    # Simple respond to hi message
    if message.content.startswith('hi'):
        await message.channel.send('hey')

    # Generate an image of randiom champions
    if message.content.startswith('!ARena'):
        
        # Find how many players to generate for, otherwise default to 1
        try:
            players = int(message.content.split()[1])
        except:
            players = 1

        # Do not allow too many players, the game is limited to 16 anyway
        if players > 16:
            await message.channel.send('less than 17 man come on')
            return

        # Loop through each player
        for p in range(players):        
            
            # Select 5 random champs, duplicates are OK
            r_champs = random.sample(champs, 5)
            
            # Loop through each champ and put their icon into a list
            champ_ims = []
            for c in r_champs:
                
                champ_pic = requests.get("http://ddragon.leagueoflegends.com/cdn/14.10.1/img/champion/" + c + ".png")       
                i = Image.open(BytesIO(champ_pic.content))
                champ_ims.append(i)

            # Create an image of appropriate size based on number of champs
            # Some of this should probably be outside the loop
            widths, heights = zip(*(i.size for i in champ_ims))                                                         
            
            total_width = sum(widths)+60
            max_height = max(heights)*players + (players-1) * 5
            if p == 0:
                new_im = Image.new('RGB', (total_width, max_height))
            
            # Start attatching champs at the left side of the image
            x_offset = 0

            #  Attach all the champs together into the image
            for ind, im in enumerate(champ_ims):
                
                # Once the first row is done, move down to the next row for the next player
                y_offset = (p)*125

                # leave some space between the champs for visibility               
                if ind == 3:
                    x_offset += 40 
                if ind == 4:
                    x_offset += 20
                new_im.paste(im, (x_offset,y_offset))
                x_offset += im.size[0]
            
            # new_im.save('test.jpg')
            draw = ImageDraw.Draw(new_im)
            
            # draw red dashed lines to seperate the reserve champs            
            for i in range(6):
                draw.line((380, y_offset+i*20+5, 380, y_offset+i*20+15), fill='red', width = 3)
                draw.line((530, y_offset+i*20+5, 530, y_offset+i*20+15), fill='red', width = 3)

            # Attempts to change the fonts and stuff, not functional yet

            # font = font_manager.FontProperties(family='sans-serif', weight='bold')
            # file = font_manager.findfont(font)
            
            # draw.text((5, y_offset), 'Player ' + str(p+1), font = font, fill = 'white', stroke_width = 2, stroke_fill = 'black' )
            # draw.text((5, y_offset), 'Player ' + str(p+1), font = font, fill = 'white', stroke_width = 2, stroke_fill = 'black' )

        # send a message for how many players with correct grammar
        if players == 1:
            await message.channel.send(f'for {players} player')
        else:
            await message.channel.send(f'for {players} players')

        # Send the image with the champs to the discord channel
        with BytesIO() as image_binary:
                new_im.save(image_binary, 'PNG')
                image_binary.seek(0)
                await message.channel.send(file=discord.File(fp=image_binary, filename='image.png'))

    # TFT item assistant, simply appends the word to a tactics.tools link and returns it
    if message.content.startswith('!items'):                

        unit = message.content.split()[1:]

        unit = ' '.join(unit)

        url_start = 'https://tactics.tools/units/'

        url = url_start + unit

        await message.channel.send('items for ' + unit + ':\n' + url) 

# Get the token for the bot from the .env file
load_dotenv()
TOKEN = os.getenv("token")


# Run the bot with the token
client.run(TOKEN)
