import os
import time
import nextcord
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
from nextcord.ext import commands
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

slash_categories = {
    ...
}

category_aliases = {
    ...
}

class VibeOfTheDay(commands.Cog):
    
    load_dotenv()
    SPOTIFY_APP_CLIENT_ID = os.environ.get("SPOTIFY_APP_CLIENT_ID")
    SPOTIFY_APP_CLIENT_SECRET = os.environ.get("SPOTIFY_APP_CLIENT_SECRET")
    SPOTIFY_VIBE_PLAYLIST_ID = os.environ.get("SPOTIFY_VIBE_PLAYLIST_ID")
    
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
    
    def background_task(self):
        while True:
            # Get the current time
            now = datetime.datetime.now()
            # Calculate the time until midnight
            midnight = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(days=1, hours=6)
            wait_time = (midnight - now).total_seconds()

            # Wait until midnight
            print("Waiting for", wait_time, "seconds until midnight.")
            time.sleep(wait_time)

            # Execute the function
            self.get_a_vibe()

            # Optional: sleep a little bit to prevent the function from executing twice around midnight
            time.sleep(1)
        
    @nextcord.slash_command(name="vibeoftheday")
    async def vibe_of_the_day(self, ctx):
        await ctx.send(self.vibe_message())
        
    

def setup(bot):
    cog = VibeOfTheDay(bot)
    cog.get_a_vibe()
    bot.add_cog(cog)
    