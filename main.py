import discord
import logging
import json
import botfinder


if __name__ == "__main__":
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    logging.getLogger().addHandler(logging.StreamHandler())

    with open("config.json") as f:
        config = json.load(f)
    with open("key.json") as f:
        key = json.load(f)
    PREFIX = '$'

    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True

    client = discord.Client(intents=intents)


    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user}')


    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content.startswith(PREFIX + 'hello'):
            await message.channel.send('Hello!')

        if message.content.startswith(PREFIX + 'memberlist'):
            await message.channel.send("Getting memberlist...")
            memberlist = []
            async for c in message.channel.guild.fetch_members(limit=None):
                memberlist.append(c.name)
#            await message.channel.send(memberlist)
            await message.channel.send("Bots found : \n" + botfinder.botfinder(memberlist))

    client.run(key.get("token"), log_handler=handler, log_level=logging.INFO)
