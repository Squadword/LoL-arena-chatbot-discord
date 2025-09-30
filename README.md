
# A chatbot designed to generate a selection of random champions for people to play in the game League of Legends.


The bot has a couple of silly functions such as sending gifs and saying hello to a user:

![image](https://github.com/Squadword/LoL-arena-chatbot-discord/blob/main/imgs/hello.png)


The main purpose of the bot is to send back a picture of some random champions from the game League of Legends when a user requests. For example:

![image](https://github.com/Squadword/LoL-arena-chatbot-discord/blob/main/imgs/ARena%201.png)

The bot does this by first requesting a list of all champions from the [riot api](https://developer.riotgames.com/docs/lol#data-dragon_champions). It then selects a random selection of 5 champions and fetches an image of them from the image endpoints. Using the Python Imaging Library (PIL) package (this has now been succeeded by the [pillow](https://pypi.org/project/pillow/) package), the bot stitchess together the images then sends it back to the chat channel. It leaves gaps and draws lines between some champions so players can have flexibility in the case some of their choices are banned.

Additionally, the bot can account for multiple players. Adding a number after the ```!ARena``` command makes the bot return multiple rows. For example:

![image](https://github.com/Squadword/LoL-arena-chatbot-discord/blob/main/imgs/ARena%207.png)

This allows for each player to assign themselves a row and select champions from that row.

Finally, the bot has one more function to assist in the TFT game mode. typing ```!items [champ name]``` simply returns a URL, to the [tactics.tools](https://tactics.tools/) website with the page open for the selected champion:

![image](https://github.com/Squadword/LoL-arena-chatbot-discord/blob/main/imgs/tft%20items.png)

## Hosting the bot

I do not full time host this bot as the functionality of it has been largely made irrelevant by the introduction of the official bravery mode in [patch 25.05](https://www.leagueoflegends.com/en-gb/news/game-updates/patch-25-05-notes/).

Good instructions to create a new bot can be found on the [free code camp website](https://www.freecodecamp.org/news/create-a-discord-bot-with-python/). The ```arena_bot.py``` script can then be used as the code for the bot.

To set the bot to run continuously, the easiest way would be to use one of the many paid services that specialise in bot and server hosting. Alternatively, I would recommend hosting your own virtual machine compute instance on [Oracle Cloud](https://www.oracle.com/uk/cloud/compute/virtual-machines/) as they have a fairly generous free tier that is more than enough to host a simple bot.
