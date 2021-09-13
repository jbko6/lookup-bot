# lookup-bot
Discord bot for searching up useful info

This discord bot uses numerous APIs to retrieve info when the user requests it.
It can retrieve info from Reddit, Wikipedia, Youtube and Twitter.

## Commands

`.randomPost`
Grabs a random post from reddit.com and shares it with you and your friends.

`.searchPosts <query>`
Searches Reddit with the given query and returns a post
  
`.searchTweets <query>`
Searches Twitter with the given query and returns a tweet
  
`.searchWiki <query>`
Searches Wikipedia with the given query and returns an entry
  
`.searchYoutube <query>`
Search for youtube videos. EXPERIMENTAL
  
`.help`
Gives you some help

## To use

First, you will need API keys for all the services listed above. Next, simply insert them into the `redditLookup.py` file. Then, create a discord bot and copy its key into the `redditLookup.py` file at the end. Run with `python3 redditLookup.py`.
