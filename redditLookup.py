import discord
from discord.ext import commands
import requests
import random

client = commands.Bot(command_prefix = '.')
api_url = 'https://oauth.reddit.com'

def refreshToken():
    base_url = 'https://www.reddit.com/'
    data = {'grant_type': 'password', 'username': '', 'password': ''}
    auth = requests.auth.HTTPBasicAuth('', ')
    r = requests.post(base_url + 'api/v1/access_token',
                      data=data,
                      headers={'user-agent': ''},
                      auth=auth)
    return r

@client.event
async def on_ready():
    print("Bot is ready.")


# Grab random posts from reddit

@client.command()
async def randomPost(ctx):
    r = refreshToken()
    d = r.json()
    token = 'bearer ' + d['access_token']
    headers = {'Authorization': token, 'User-Agent': ''}
    payload = {'limit': 50}
    response = requests.get(api_url + '/best', headers=headers, params=payload)
    data = response.json()
    post = random.randint(0, 49)
    embed=discord.Embed(title=data['data']['children'][post]['data']['title'],
                        url='https://reddit.com'+data['data']['children'][post]['data']['permalink'],
                        description=data['data']['children'][post]['data']['subreddit_name_prefixed'] + '\n' + str(data['data']['children'][post]['data']['upvote_ratio'])[2:] + '% upvoted with ' + str(data['data']['children'][post]['data']['num_comments']) + ' comments.',
                        color=0x1F85DE)
    embed.set_author(name=data['data']['children'][post]['data']['author'])
    if 'post_hint' in data['data']['children'][post]['data']:
        if data['data']['children'][post]['data']['post_hint'] == 'image':
            embed.set_thumbnail(url=str(data['data']['children'][post]['data']['thumbnail']))
    await ctx.send(embed=embed)


# Search reddit posts

@client.command()
async def searchPosts(ctx, *, query):
    r = refreshToken()
    d = r.json()
    token = 'bearer ' + d['access_token']
    headers = {'Authorization': token, 'User-Agent': ''}
    payload = {'limit': 1, 'q': query}
    response = requests.get(api_url + '/search', headers=headers, params=payload)
    data = response.json()
    post = 0
    embed=discord.Embed(title=data['data']['children'][post]['data']['title'],
                        url='https://reddit.com'+data['data']['children'][post]['data']['permalink'],
                        description=data['data']['children'][post]['data']['subreddit_name_prefixed'] + '\n' + str(data['data']['children'][post]['data']['upvote_ratio'])[2:] + '% upvoted with ' + str(data['data']['children'][post]['data']['num_comments']) + ' comments.',
                        color=0x1F85DE)
    embed.set_author(name=data['data']['children'][post]['data']['author'])
    if 'post_hint' in data['data']['children'][post]['data']:
        if data['data']['children'][post]['data']['post_hint'] == 'image':
            embed.set_thumbnail(url=str(data['data']['children'][post]['data']['thumbnail']))
    await ctx.send(embed=embed)



# Search tweets

@client.command()
async def searchTweets(ctx, *, query):
    try:
        headers = {"Authorization": ""}
        response = requests.get("https://api.twitter.com/1.1/search/tweets.json?q={}&lang=en&count=1&result_type=popular".format(str(query)), headers=headers)
        data = response.json()
        if len(data['statuses']) == 0:
            await ctx.send("There were no results. Try asking again with different wording.")
            return
        embed = discord.Embed(description=data['statuses'][0]['text'],
                              color=0x1F85DE)
        if len(data['statuses'][0]['entities']['user_mentions']) > 0:
            embed.set_author(name=data['statuses'][0]['entities']['user_mentions'][0]['name'])
        embed.set_footer(text='Twitter | Posted ' + data['statuses'][0]['created_at'])
        await ctx.send(embed=embed)
    except:
        await ctx.send("I'm sorry, but an error occured and the tweet could not be retrieved.")
        print(data)

# Search wikipedia for entries

@client.command()
async def searchWiki(ctx, *, query):
    try:
        response = requests.get('https://en.wikipedia.org/w/api.php?action=query&origin=*&format=json&generator=search&gsrnamespace=0&gsrlimit=5&gsrsearch={}'.format(query))
        data = response.json()
        if 'query' not in data:
            await ctx.send("There were no results. Try asking again with different wording.")
            return
        response = requests.get('https://en.wikipedia.org/api/rest_v1/page/summary/{}'.format(query.replace(" ", "_")), headers={'Accept-Language': 'en'})
        data = response.json()
        if 'detail' in data:
            if data['detail'] == 'Page or revision not found.':
                await ctx.send("There were no results. Try asking again with different wording.")
                return
        embed = discord.Embed(title=data['displaytitle'],
                              url=data['content_urls']['desktop']['page'],
                              description=data['extract'],
                              color=0x1F85DE)
        embed.set_author(name="Wikipedia",
                         url='https://www.wikipedia.org/',
                         icon_url='https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Wikipedia_svg_logo.svg/200px-Wikipedia_svg_logo.svg.png')
        if 'thumbnail' in data:
            embed.set_thumbnail(url=data['thumbnail']['source'])
        embed.set_footer(text='Not what you were looking for? Ask again with different wording.')
        await ctx.send(embed=embed)
    except TypeError:
        await ctx.send("I'm sorry, but an error occured and the search could not be completed. `ERROR: TYPEERROR`")
    except Exception as e:
        await ctx.send("I'm sorry, but an error occured and the search could not be completed.")
        await ctx.send("<@138713857043464192> Debug me! \n`Error: {}\nData: {}`".format(e, data))

@client.command()
async def searchYoutube(ctx, *, query):
    key = ''
    response = requests.get('https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={}&key={}'.format(query, key))
    data = response.json()
    if len(data['items']) == 0:
        await ctx.send("There were no results. Try searching again with different wording.")
        return
    embed = discord.Embed(title=data['items'][0]['snippet']['title'],
                          url='https://www.youtube.com/watch?v='+data['items'][0]['id']['videoId'],
                          description=data['items'][0]['snippet']['description'],
                          color=0x1F85DE)
    embed.set_author(name=data['items'][0]['snippet']['channelTitle'],
                     url='https://www.youtube.com/channel/'+data['items'][0]['snippet']['channelId'])
    embed.set_thumbnail(url=data['items'][0]['snippet']['thumbnails']['default']['url'])
    embed.set_footer(text='Not what you were looking for? Ask again with different wording.')
    await ctx.send(embed=embed)
    

client.remove_command("help")
@client.command()
async def help(ctx):
    embed = discord.Embed(title='Help', color=0x1F85DE)
    embed.add_field(name='.randomPost',
                    value='Grabs a random post from reddit.com and shares it with you and your friends.',
                    inline=False)
    embed.add_field(name='.searchPosts <query>',
                    value='Searches Reddit with the given query and returns a post',
                    inline=False)
    embed.add_field(name='.searchTweets <query>',
                    value='Searches Twitter with the given query and returns a tweet',
                    inline=False)
    embed.add_field(name='.searchWiki <query>',
                    value='Searches Wikipedia with the given query and returns an entry',
                    inline=False)
    embed.add_field(name='.searchYoutube <query>',
                    value='Search for youtube videos. `EXPERIMENTAL`',
                    inline=False)
    embed.add_field(name='.help',
                    value='Gives you some help',
                    inline=False)
    await ctx.send(embed=embed)

@client.command()
async def introduce(ctx):
    await ctx.send('''***Hey there!***
I'm Lookup. I use different APIs across the web to help you find things without opening a web browser! I'm being developed by <@138713857043464192> and you can give him suggestions if you come across any. I'm always expanding my reach across the web but if you want a specific thing to be searchable, let him know. 
You can ask for help and commands using `.help`
Have fun!''')
    
    await ctx.message.delete()

client.run('')
