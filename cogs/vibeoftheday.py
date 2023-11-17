import os
import random
import spotipy
import nextcord
from nextcord.ext import tasks, commands
from datetime import datetime
from dotenv import load_dotenv
from nextcord.ext import commands
from spotipy.oauth2 import SpotifyClientCredentials

slash_categories = {
    ...
}

category_aliases = {
    ...
}

class VibeOfTheDay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.background_task.start()
    
    load_dotenv()
    SPOTIFY_APP_CLIENT_ID = os.environ.get("SPOTIFY_APP_CLIENT_ID")
    SPOTIFY_APP_CLIENT_SECRET = os.environ.get("SPOTIFY_APP_CLIENT_SECRET")
    SPOTIFY_VIBE_PLAYLIST_ID = os.environ.get("SPOTIFY_VIBE_PLAYLIST_ID")
    VIBE_ANNOUNCEMENT_CHANNEL = os.environ.get("VIBE_ANNOUNCEMENT_CHANNEL")
    
    current_vibe_url = ""
    current_vibe_name = ""
    current_vibe_artists = ""
    
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIFY_APP_CLIENT_ID, client_secret=SPOTIFY_APP_CLIENT_SECRET))
    
    def get_a_vibe(self):
        results = self.sp.playlist_tracks(self.SPOTIFY_VIBE_PLAYLIST_ID)
        tracks = results['items']
        while results['next']:
            results = self.sp.next(results)
            tracks.extend(results['items'])
        track = random.choice(tracks)["track"]
        
        artists = []
        for artist in track["artists"]:
            artists.append(artist["name"])
        
        self.current_vibe_name = track["name"]
        self.current_vibe_url = track["external_urls"]["spotify"]
        self.current_vibe_artists = ", ".join(artists)
    
    def vibe_message(self):
        message = f'Vibe of the day\n[{self.current_vibe_name}]({self.current_vibe_url}) by {self.current_vibe_artists}'
        return message
    
    def cog_unload(self):
        self.background_task.cancel()

    @tasks.loop(hours=1)
    async def background_task(self):    
        now = datetime.datetime.now()
        if 20 <= now.hour < 21:
            self.get_a_vibe()
            channel = self.bot.get_channel(self.VIBE_ANNOUNCEMENT_CHANNEL)
            channel.send(self.vibe_message())
        
    @nextcord.slash_command(name="vibeoftheday")
    async def vibe_of_the_day(self, ctx):
        await ctx.send(self.vibe_message())

def setup(bot):
    cog = VibeOfTheDay(bot)
    cog.get_a_vibe()
    bot.add_cog(cog)