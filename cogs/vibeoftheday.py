import json
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

CACHE_DIR = "./cogs/.cache/vibeoftheday.cache"

class VibeOfTheDay(commands.Cog):
    load_dotenv()
    SPOTIFY_APP_CLIENT_ID = os.environ.get("SPOTIFY_APP_CLIENT_ID")
    SPOTIFY_APP_CLIENT_SECRET = os.environ.get("SPOTIFY_APP_CLIENT_SECRET")
    SPOTIFY_VIBE_PLAYLIST_ID = os.environ.get("SPOTIFY_VIBE_PLAYLIST_ID")
    VIBE_ANNOUNCEMENT_CHANNEL = os.environ.get("VIBE_ANNOUNCEMENT_CHANNEL")
    
    def __init__(self, bot):
        self.bot = bot
        # Check if the file exists
        if not os.path.exists(CACHE_DIR):
            # Create the file
            with open(CACHE_DIR, 'w') as file:
                file.write('')  # You can write initial content if needed
                
        self.cache_file = open(CACHE_DIR, "r+")
        self.load_from_cache()
        
    def load_from_cache(self):
        string = self.cache_file.read()
        if string == '':
            self.current_vibe = {"name": "", "artists": "", "urls": {"spotify": "", "yt_music": ""}}
            self.get_a_vibe()
            return
        self.current_vibe = json.loads(string)
    
    def save_to_cache(self):
        self.cache_file.write(json.dumps(self.current_vibe))
    
    current_vibe = {}
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
        
        self.current_vibe["name"] = track["name"]
        self.current_vibe["urls"]["spotify"] = track["external_urls"]["spotify"]
        self.current_vibe["artists"] = ", ".join(artists)
        self.current_vibe["urls"]["yt_music"] = self.youtube_music_url()
        self.save_to_cache()
    
    def youtube_music_url(self):
        ytm_id = YouTubeMusicAPI.search(f"{self.current_vibe["name"]} by {self.current_vibe["artists"]}")["id"]
        return f"https://music.youtube.com/watch?v={ytm_id}"
    
    def vibe_message(self):
        message = dedent(f"""
            ### Vibe of the day:
            *{self.current_vibe["name"]}* by *{self.current_vibe["artists"]}*
            [Spotify]({self.current_vibe["urls"]["spotify"]}) - [YT Music]({self.current_vibe["urls"]["yt_music"]})
            """)
        return message
    
    def cog_unload(self):
        self.cache_file.close()
        self.background_task.cancel()

    @tasks.loop(hours=1.0)
    async def background_task(self):    
        now = datetime.now()
        if 6 <= now.hour < 7:
            self.get_a_vibe()
            channel = self.bot.get_channel(int(self.VIBE_ANNOUNCEMENT_CHANNEL))
            await channel.send(self.vibe_message(), suppress_embeds=True)
        
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        self.background_task.start()

def setup(bot):
    bot.add_cog(VibeOfTheDay(bot))