import discord
import logging
import json
import botfinder


if __name__ == "__main__":
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    logging.getLogger().addHandler(logging.StreamHandler())

    with open("config.json", "r") as f:
        config = json.load(f)
    with open("key.json", "r") as f:
        key = json.load(f)
    PREFIX = config.get("prefix")

    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True

    client = discord.Client(intents=intents)
    tree = discord.app_commands.CommandTree(client)

    @tree.error
    async def cmd_on_error(interaction, error):
        if isinstance(error, discord.app_commands.BotMissingPermissions):
            await interaction.response.send_message("It seems like the bot is missing permissions to complete this command...")
        else:
            raise error

    @tree.command(name="ping", description="This just answers pong, as fast as possible. Yes, really.", guild=discord.Object(id=926233297967779880))
    async def first_command(ctx):
        await ctx.response.send_message("Pong!")

    @tree.command(name="botfinder", description="Attemps to find bots. Defaults to the name in the config if the field is empty.")
    async def cmd_botfinder(ctx, target: str):
#        await ctx.response.send_message("Not yet implemented. We're almost there!")
        role = discord.utils.find(lambda r: r.name == 'i am staff', ctx.guild.roles)
        if role in ctx.user.roles:
#            await ctx.response.send_message("Not yet implemented. We're almost there!")
            print(target)
            memberlist = [target]
            async for c in ctx.channel.guild.fetch_members(limit=None):
                memberlist.append(c.name)
            await ctx.response.send_message("Bots found : \n```\n" + botfinder.botfinder(memberlist) + "\n```")
        else:
            await ctx.response.send_message("You're missing a role! You cannot do that!")

    @client.event
    async def on_ready():
        await tree.sync(guild=discord.Object(id=926233297967779880))
        await tree.sync(guild=discord.Object(id=727426780381577291))
        await tree.sync()
        print(f'Successfully logged in as {client.user}')

#    @client.event
#    async def on_message(message):
#        if message.author == client.user:
#            return
#
#        if message.content.startswith(PREFIX + 'hello'):
#            await message.channel.send('Hello!')
#
#        if message.content.startswith(PREFIX + 'botfinder'):
#            if message.content.strip(PREFIX + 'botfinder' + ' ') == "":
#                memberlist = [config.get("default_target")]
#            else:
#                memberlist = [message.content.lstrip(PREFIX + 'botfinder'+ ' ')]
#            await message.channel.send(f"Getting memberlist...\nSearching for target `{memberlist[0]}`")
#            async for c in message.channel.guild.fetch_members(limit=None):
#                memberlist.append(c.name)
##            await message.channel.send(memberlist)
#            await message.channel.send("Bots found : \n```\n" + botfinder.botfinder(memberlist) + "\n```")

    client.run(key.get("token"), log_handler=handler, log_level=logging.INFO)
