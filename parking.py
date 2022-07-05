import discord
import confighandler
import lastfmhandler
from discord.ext import commands
import userhandler
import time

client = commands.Bot(command_prefix="!")
confighandler.config = confighandler.readconfig()
userhandler.users.update(userhandler.read_db())


@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))


@client.command(aliases=['l'])
async def last(ctx, ref = 3):
    print(f"[INFO] {ctx.author} ({ctx.author.id}) issued \"last\" command with {ref} songs.")
    if(ref > 5):
        embed = discord.Embed(title=":x: Une erreur est survenue!",
                              description=f"Vous ne pouvez pas afficher plus de 5 éléments simultanément.",
                              color=0xff0000)
        await ctx.send(embed=embed)
        return
    user = userhandler.get_user(ctx.author.id)
    if user != "error":   
        start_time = time.time()
        a = lastfmhandler.get_tracks_recent(user)
        embed = discord.Embed(title=f"Musiques récemment écoutées par {ctx.author.name}",
                              color=0x5DADEC)
        embed.set_thumbnail(url=lastfmhandler.get_album(a['recenttracks']['track'][0])['image'][3]['#text'])
        for i in range(int(ref)):
            embed.add_field(name=":musical_note:   " + a['recenttracks']['track'][i][
                'name'] + f" (x{lastfmhandler.get_track_playcount(user, a['recenttracks']['track'][i])})",
                            value=f"Par **{a['recenttracks']['track'][i]['artist']['#text']}** (x{lastfmhandler.get_artist_playcount(user, a['recenttracks']['track'][i])}) "
                                  f"dans **{a['recenttracks']['track'][i]['album']['#text']}** (x{lastfmhandler.get_album_playcount(user, a['recenttracks']['track'][i])})",
                            inline=False)
        embed.set_footer(text=f"{ref} item shown. Process time: {str(round(time.time()-start_time,2))}s")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=":x: Une erreur est survenue!",
                              description=f"Vous n'avez pas relié de compte, utilisez `!link <identitifant last.fm>` afin d'y remédier.",
                              color=0xff0000)
        await ctx.send(embed=embed)



@client.command()
async def link(ctx, ref):
    print(f"[INFO] {ctx.author} ({ctx.author.id}) issued \"link\" command with {ref}'s account.")
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
        print(f"[INFO] {ctx.author} ({ctx.author.id}) was linked to {ref}'s account.")
        await ctx.send(embed=embed)


@link.error
async def link_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=":x: Une erreur est survenue!",
                              description=f"Vous devez entrer un nom de compte.",
                              color=0xff0000)
        await ctx.send(embed=embed)


client.run(confighandler.config['token'])

