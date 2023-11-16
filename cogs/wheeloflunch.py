import os
import random
import nextcord
from dotenv import load_dotenv
from nextcord.ext import commands
import requests
from urllib.parse import quote

load_dotenv()
YELP_API_KEY = os.environ.get("YELP_API_KEY")

slash_categories = {
    ...
}

category_aliases = {
    ...
}

class WheelOfLunch(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    def google_maps_link(self, business_name, address):
        # Create the Google Maps URL
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
            'Authorization': f'Bearer {YELP_API_KEY}'
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
        
    @nextcord.slash_command(name="wheeloflunch")
    async def wheel_of_lunch(self, ctx, zipcode: str):
        business = self.random_business(zipcode)
        
        business_name = business["name"] + "\n"
        business_categories = "Categories: " + ', '.join(self.categories(business)) + "\n"
        business_rating = "Rating: " + str(business["rating"]) + "/5 - " + str(business["review_count"]) + " reviews.\n"
        maps_link = self.google_maps_link(business["name"], business["location"]["display_address"][0]) + "\n"
        
        message_string = business_name
        message_string += business_categories
        message_string += business_rating
        message_string += maps_link
        
        await ctx.send(message_string)

def setup(bot):
    bot.add_cog(WheelOfLunch(bot))