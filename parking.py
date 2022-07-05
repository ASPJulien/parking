import discord
import confighandler
import lastfmhandler
from discord.ext import commands
import userhandler

client = commands.Bot(command_prefix="!")
confighandler.config = confighandler.readconfig()
userhandler.users = userhandler.read_db()

@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))


@client.command(aliases=['l'])
async def last(ctx):
    user = userhandler.get_user(ctx.author.id)
    if user != "error":   
        a = lastfmhandler.get_tracks_recent(user)
        embed = discord.Embed(title=f"Musiques récemment écoutées par {ctx.author.name}",
                              color=0x5DADEC)
        embed.set_thumbnail(url=lastfmhandler.get_album(a['recenttracks']['track'][0])['image'][3]['#text'])

        for i in range(5):
            embed.add_field(name=":musical_note:   " + a['recenttracks']['track'][i][
                'name'] + f" (x{lastfmhandler.get_track_playcount(user, a['recenttracks']['track'][i])})",
                            value=f"Par **{a['recenttracks']['track'][i]['artist']['#text']}** (x{lastfmhandler.get_artist_playcount(user, a['recenttracks']['track'][i])}) "
                                  f"dans **{a['recenttracks']['track'][i]['album']['#text']}** (x{lastfmhandler.get_album_playcount(user, a['recenttracks']['track'][i])})",
                            inline=False)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=":x: Une erreur est survenue!",
                              description=f"Vous n'avez pas relié de compte, utilisez `!link <identitifant last.fm>` afin d'y remédier.",
                              color=0xff0000)
        await ctx.send(embed=embed)


@client.command()
async def link(ctx, ref):
    ref = ref.replace("https://www.last.fm/user/", "")
    if not userhandler.lastfm_user_exists(ref):
        embed = discord.Embed(title=":x: Une erreur est survenue!",
                              description=f'Le compte "{ref}" n\'existe pas.',
                              color=0xff0000)
        await ctx.send(embed=embed)
    elif userhandler.get_user(ctx.author.id) != "error":
         embed = discord.Embed(title=":x: Une erreur est survenue!",
                              description=f'Votre compte est déjà associé à "{userhandler.get_user(ctx.author.id)}"',
                              color=0xff0000)
         await ctx.send(embed=embed)
    else:
        userhandler.link_user(ctx.author.id, ref)
        embed = discord.Embed(title=":white_check_mark: Votre compte a été enregistré!",
                              description=f'Le compte "{ref}" a été associé à {ctx.author.mention}.',
                              color=0x00ff00)
        await ctx.send(embed=embed)


@link.error
async def link_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=":x: Une erreur est survenue!",
                              description=f"Vous devez entrer un nom de compte.",
                              color=0xff0000)
        await ctx.send(embed=embed)


client.run(confighandler.config['token'])

