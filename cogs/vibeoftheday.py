import os
import random
import spotipy
import nextcord
import YouTubeMusicAPI
from textwrap import dedent
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
    
    load_dotenv()
    SPOTIFY_APP_CLIENT_ID = os.environ.get("SPOTIFY_APP_CLIENT_ID")
    SPOTIFY_APP_CLIENT_SECRET = os.environ.get("SPOTIFY_APP_CLIENT_SECRET")
    SPOTIFY_VIBE_PLAYLIST_ID = os.environ.get("SPOTIFY_VIBE_PLAYLIST_ID")
    VIBE_ANNOUNCEMENT_CHANNEL = os.environ.get("VIBE_ANNOUNCEMENT_CHANNEL")
    
    current_vibe_spot_url = ""
    current_vibe_name = ""
    current_vibe_artists = ""
    current_vibe_ytm_url = ""
    
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
        self.current_vibe_spot_url = track["external_urls"]["spotify"]
        self.current_vibe_artists = ", ".join(artists)
        self.youtube_music_url()
    
    def youtube_music_url(self):
        ytm_id = YouTubeMusicAPI.search(f"{self.current_vibe_name} by {self.current_vibe_artists}")["id"]
        self.current_vibe_ytm_url = f"https://music.youtube.com/watch?v={ytm_id}"
    
    def vibe_message(self):
        message = dedent(f"""
            ## Vibe of the day
            {self.current_vibe_name} by {self.current_vibe_artists}
            [Spotify]({self.current_vibe_spot_url}) - [YT Music]({self.current_vibe_ytm_url})
            """)
        return message
    
    def cog_unload(self):
        self.background_task.cancel()

    @tasks.loop(hours=1.0)
    async def background_task(self):    
        now = datetime.now()
        if 6 <= now.hour < 7:
            self.get_a_vibe()
            channel = self.bot.get_channel(int(self.VIBE_ANNOUNCEMENT_CHANNEL))
            await channel.send(self.vibe_message())
        
    @nextcord.slash_command(name="vibeoftheday")
    async def vibe_of_the_day(self, ctx):
        await ctx.send(self.vibe_message())
        
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        self.background_task.start()

def setup(bot):
    cog = VibeOfTheDay(bot)
    cog.get_a_vibe()
    bot.add_cog(cog)