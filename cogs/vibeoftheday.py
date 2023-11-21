import os
from nextcord.ext import tasks, commands
from dotenv import load_dotenv

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import YouTubeMusicAPI
import json
from textwrap import dedent
from datetime import datetime
import random

CACHE_DIR = "./cogs/.cache/"
CACHE_FILE = "vibeoftheday.cache"

class vibeoftheday(commands.Cog):
    
    #region Enviornment Variables
    load_dotenv()
    SPOTIFY_APP_CLIENT_ID = os.environ.get("SPOTIFY_APP_CLIENT_ID")
    SPOTIFY_APP_CLIENT_SECRET = os.environ.get("SPOTIFY_APP_CLIENT_SECRET")
    SPOTIFY_VIBE_PLAYLIST_ID = os.environ.get("SPOTIFY_VIBE_PLAYLIST_ID")
    VIBE_ANNOUNCEMENT_CHANNEL = os.environ.get("VIBE_ANNOUNCEMENT_CHANNEL")
    #endregion

    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIFY_APP_CLIENT_ID, client_secret=SPOTIFY_APP_CLIENT_SECRET))
    
    def __init__(self, bot):
        self.bot = bot
        self.cache_file = CACHE_DIR + CACHE_FILE
        self.load_from_cache()
        
    #region Cache Functions
    def load_from_cache(self):
        # Create the cache file if it doesn't exist
        if not os.path.exists(CACHE_DIR):
            os.makedirs(CACHE_DIR)
        if not os.path.exists(CACHE_DIR + CACHE_FILE):
            open(CACHE_DIR + CACHE_FILE, "w+").close()
        with open(self.cache_file, "r") as cache_file:
            string = cache_file.read()
            try:
                self.current_vibe = json.loads(string)
            except:
                self.current_vibe = {"name": "", "artists": "", "urls": {"spotify": "", "yt_music": ""}}
                self.get_a_vibe()
                return
    
    def save_to_cache(self, song): 
        with open(self.cache_file, "w") as cache_file:
            cache_file.write(json.dumps(song))
    #endregion
    
    #region Helper Functions
    def random_song(self, playlist_id: str):
        results = self.sp.playlist_tracks(playlist_id)
        tracks = results['items']
        while results['next']:
            results = self.sp.next(results)
            tracks.extend(results['items'])
        return random.choice(tracks)["track"]
        
    def format_song(self, song):
        # Format the artists into a string
        artists = []
        for artist in song["artists"]:
            artists.append(artist["name"])
        
        self.current_vibe = {
            "name": song["name"],
            "artists": ", ".join(artists),
            "urls": {
                "spotify": song["external_urls"]["spotify"],
                "yt_music": self.youtube_music_url(song)
            }
        }
        
    def vibe_message(self):
        message = dedent(f"""
            ### Vibe of the day:
            ***{self.current_vibe["name"]}*** by ***{self.current_vibe["artists"]}***
            [Spotify]({self.current_vibe["urls"]["spotify"]}) - [YT Music]({self.current_vibe["urls"]["yt_music"]})
            """)
        return message
    
    def youtube_music_url(self, song):
        ytm_id = YouTubeMusicAPI.search(f'{song["name"]} by {song["artists"]}')["id"]
        return f"https://music.youtube.com/watch?v={ytm_id}"
    
    def get_a_vibe(self):
        song = self.random_song(self.SPOTIFY_VIBE_PLAYLIST_ID)
        self.format_song(song)
        self.save_to_cache(self.current_vibe)
    #endregion
    
    def cog_unload(self):
        self.cache_file.close()
        self.background_task.cancel()

    @tasks.loop(seconds=3600)
    async def background_task(self):    
        now = datetime.now()
        if 6 <= now.hour < 7:
            print("vibeoftheday: It's 6 o'clock, time to vibe!")
            self.get_a_vibe()
            channel = self.bot.get_channel(int(self.VIBE_ANNOUNCEMENT_CHANNEL))
            await channel.send(self.vibe_message(), suppress_embeds=True)
        
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        self.background_task.start()

def setup(bot):
    bot.add_cog(vibeoftheday(bot))