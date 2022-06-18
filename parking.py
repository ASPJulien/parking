import discord
import confighandler
import lastfmhandler
from discord.ext import commands
import userhandler

client = commands.Bot(command_prefix="!")
confighandler.config = confighandler.readconfig()


@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))


@client.command()
async def last(ctx):
    a = lastfmhandler.get_tracks_recent("jupilian")
    embed = discord.Embed(title=f"Musiques récemment écoutées par {ctx.author.name}",
                          color=discord.Color.blue())
    embed.set_thumbnail(url=lastfmhandler.get_album(a['recenttracks']['track'][0])['image'][3]['#text'])

    for i in range(5):
        embed.add_field(name=":musical_note:   " + a['recenttracks']['track'][i][
            'name'] + f" (x{lastfmhandler.get_track_playcount('jupilian', a['recenttracks']['track'][i])})",
                        value=f"Par **{a['recenttracks']['track'][i]['artist']['#text']}** (x{lastfmhandler.get_artist_playcount('jupilian', a['recenttracks']['track'][i])}) "
                              f"dans **{a['recenttracks']['track'][i]['album']['#text']}** (x{lastfmhandler.get_album_playcount('jupilian', a['recenttracks']['track'][i])})",
                        inline=False)
    await ctx.send(embed=embed)
    pass


@client.command()
async def link(ctx, ref):
    ref = ref.replace("https://www.last.fm/user/", "")
    if not userhandler.lastfm_user_exists(ref):
        embed = discord.Embed(title=":x: Une erreur est survenue!",
                              description=f"Le compte \"{ref}\" n\'existe pas.",
                              color=discord.Color.red())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=":white_check_mark: Votre compte a été enregistré!",
                              description=f"Le compte \"{ref}\" a été associé à {ctx.author.mention}.",
                              color=discord.Color.green())
        await ctx.send(embed=embed)
    pass


client.run(confighandler.config['token'])
client.add_command(last)
client.add_command(link)

