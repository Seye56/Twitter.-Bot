import tweepy
import schedule
import time
import random
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from dotenv import load_dotenv
import os
import textwrap
import logging
  
# Load environment variables from .env file
load_dotenv("Twitter/files.env")

# Retrieve sensitive information from environment variables
API_KEY = os.getenv("API_KEY")
API_KEY_SECRET = os.getenv("API_KEY_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

# Check if Twitter API credentials are missing
if not API_KEY or not API_KEY_SECRET or not ACCESS_TOKEN or not ACCESS_TOKEN_SECRET:
    raise ValueError("Twitter API credentials are missing. Check your .env file.")

client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_KEY_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET,
    bearer_token=BEARER_TOKEN
)

# Authenticate to Twitter
auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# List of 100 motivational quotes
quotes = [
    "Believe you can and you're halfway there. - Theodore Roosevelt",
    "The only way to do great work is to love what you do. - Steve Jobs",
    "Success is not final, failure is not fatal: It is the courage to continue that counts. - Winston Churchill",
    "You miss 100 percent 0f the shots you don’t take. - Wayne Gretzky",
    "Do what you can, with what you have, where you are. - Theodore Roosevelt",
    "Act as if what you do makes a difference. It does. - William James",
    "It does not matter how slowly you go as long as you do not stop. - Confucius",
    "What lies behind us and what lies before us are tiny matters compared to what lies within us. - Ralph Waldo Emerson",
    "Don't watch the clock; do what it does. Keep going. - Sam Levenson",
    "Keep your face always toward the sunshine—and shadows will fall behind you. - Walt Whitman",
    "Hardships often prepare ordinary people for an extraordinary destiny. - C.S. Lewis",
    "The future depends on what you do today. - Mahatma Gandhi",
    "If you want to achieve greatness, stop asking for permission. - Anonymous",
    "The way to get started is to quit talking and begin doing. - Walt Disney",
    "Everything you’ve ever wanted is on the other side of fear. - George Addair",
    "Opportunities don't happen, you create them. - Chris Grosser",
    "Don’t let yesterday take up too much of today. - Will Rogers",
    "Failure will never overtake me if my determination to succeed is strong enough. - Og Mandino",
    "Success is how high you bounce when you hit bottom. - George S. Patton",
    "Believe in yourself and all that you are. Know that there is something inside you that is greater than any obstacle. - Christian D. Larson",
    "A person who never made a mistake never tried anything new. - Albert Einstein",
    "Do not go where the path may lead, go instead where there is no path and leave a trail. - Ralph Waldo Emerson",
    "You are never too old to set another goal or to dream a new dream. - C.S. Lewis",
    "Everything has beauty, but not everyone sees it. - Confucius",
    "Success is getting what you want. Happiness is wanting what you get. - Dale Carnegie",
    "He who opens a school door, closes a prison. - Victor Hugo",
    "When something is important enough, you do it even if the odds are not in your favor. - Elon Musk",
    "Happiness is not something ready made. It comes from your own actions. - Dalai Lama",
    "If you're going through hell, keep going. - Winston Churchill",
    "Live as if you were to die tomorrow. Learn as if you were to live forever. - Mahatma Gandhi",
    "Courage is not having the strength to go on; it is going on when you don't have the strength. - Theodore Roosevelt",
    "Dream big and dare to fail. - Norman Vaughan",
    "Success usually comes to those who are too busy to be looking for it. - Henry David Thoreau",
    "Difficulties in life are intended to make us better, not bitter. - Dan Reeves",
    "Nothing is impossible, the word itself says ‘I’m possible’! - Audrey Hepburn",
    "Limitations live only in our minds. But if we use our imaginations, our possibilities become limitless. - Jamie Paolinetti",
    "Success is not in what you have, but who you are. - Bo Bennett",
    "Your limitation—it’s only your imagination. - Anonymous",
    "Push yourself, because no one else is going to do it for you. - Anonymous",
    "Great things never come from comfort zones. - Anonymous",
    "Dream it. Wish it. Do it. - Anonymous",
    "Stay hungry. Stay foolish. - Steve Jobs",
    "It always seems impossible until it’s done. - Nelson Mandela",
    "The secret of getting ahead is getting started. - Mark Twain",
    "Little by little, one travels far. - J.R.R. Tolkien",
    "The best way to predict the future is to create it. - Peter Drucker",
]

backgrounds =[
    "Twitter/images/image1.jpg",
    "Twitter/images/image2.jpg",
    "Twitter/images/image3.jpg",
    "Twitter/images/image4.jpg",
    "Twitter/images/image5.jpg",
    "Twitter/images/image6.jpg",
    "Twitter/images/image7.jpg",
    "Twitter/images/image8.jpg",
    "Twitter/images/image9.jpg",
    "Twitter/images/image10.jpg",
    "Twitter/images/image11.jpg",
    "Twitter/images/image12.jpg",
    "Twitter/images/image13.jpg",
]

#def draw_text(draw, text, position, font, max_width):
def draw_text(draw, text, position, font, max_width, image_width):
    """Draw text with word wrapping and central alignment."""
    lines = textwrap.wrap(text, width=max_width)  # Wrap text to fit within max_width
    x, y = position  # Starting position for the text

    # Calculate total height of the text block
    total_height = sum(font.getbbox(line)[3] - font.getbbox(line)[1] for line in lines)

    # Adjust y to center the text block vertically
    y = (image_width - total_height) // 2

    for line in lines:
        # Calculate the width of the current line
        line_width = font.getbbox(line)[2] - font.getbbox(line)[0]

        # Adjust x to center the line horizontally
        x = (image_width - line_width) // 2

        # Draw the line
        draw.text((x, y), line, font=font, fill="white", align="center")

        # Move to the next line
        y += font.getbbox(line)[3] - font.getbbox(line)[1]

# Create a function to generate a random quote with a random image
def create_image_with_background(quote):
    # Get a random image from the background list
    image_path = random.choice(backgrounds)
    bg_img = Image.open(image_path)

    # Resize the image
    bg_img = bg_img.resize((800, 600))

    # Add the quote to the image
    draw = ImageDraw.Draw(bg_img)
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", size=30) 


    # Define text position and max width for wrapping
    position = (50, 50)  # (x, y) coordinates for the text
    max_width = 30  # Maximum number of characters per line
    image_width = bg_img.width

    # Draw the text with word wrapping
    draw_text(draw, quote, position, font, max_width, image_width)

    # Save the image
    output_image_path = "Twitter/images/quote.png"
    bg_img.save(output_image_path)
    return output_image_path



def tweet_quote():
    try:
        # Get a random quote
        quote = random.choice(quotes)
        logging.info(f"Selected quote: {quote}")

        # Create an image with the quote
        image_path = create_image_with_background(quote)

        # Upload the image and tweet the quote
        media = api.media_upload(image_path)
        client.create_tweet(text=quote, media_ids=[media.media_id])
        logging.info(f"Tweeted: {quote}")

    except Exception as e:
        logging.error(f"Failed to tweet: {e}")



#tweet code for testing
tweet_quote()

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)