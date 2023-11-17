import os
import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv

import random
import requests
from textwrap import dedent
from urllib.parse import quote

class WheelOfLunch(commands.Cog):
    
    #region Enviornment Variables
    load_dotenv()
    YELP_API_KEY = os.environ.get("YELP_API_KEY")
    #endregion
    
    def __init__(self, bot):
        self.bot = bot
    
    #region Helper Functions
    def google_maps_link(self, business_name, address):
        query_string = business_name + " " + address
        maps_url = f"https://maps.google.com/?q={quote(query_string)}"
        return maps_url
    
    def categories(self, business):
        categories = []
        for category in business["categories"]:
            categories.append(category["title"])
        return categories
    
    def random_business(self, zipcode):
        url = 'https://api.yelp.com/v3/businesses/search'
        headers = {
            'Authorization': f'Bearer {self.YELP_API_KEY}'
        }
        params = {
            'term': 'lunch',
            'location': zipcode,
            'limit': 50  # Number of results to return
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            businesses = response.json()['businesses']
            return random.choice(businesses)
        else:
            return f'Error: {response.status_code}'
    #endregion
        
    @nextcord.slash_command(name="wheeloflunch")
    async def wheel_of_lunch(self, ctx, zipcode: str):
        business = self.random_business(zipcode)
        message_string = dedent(f"""
                                {business["name"]}
                                Categories: {', '.join(self.categories(business))}
                                Rating: {business["rating"]}/5 - {business["review_count"]} reviews.
                                {self.google_maps_link(business["name"], business["location"]["display_address"][0])}
                                """)
        await ctx.send(message_string)

def setup(bot):
    bot.add_cog(WheelOfLunch(bot))