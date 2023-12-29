import logging
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, Filters, Updater
import pickle
import pandas as pd
import requests

# Initialize Flask application
app = Flask(__name__)

# Your Telegram bot token obtained from the BotFather
TELEGRAM_TOKEN = '6677010304:AAGlufP2RPMHGaqOZbvw47g4EXju8Tef5iU'

# Load your machine learning model (replace this with your actual model loading code)


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?query=Jack+Reacher&api_key=cad895c4e6b6b78fa4fbbea366aae6b5".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):


    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        #fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters


    

similarity = pickle.load(open('similarity.pkl', 'rb'))
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Function to handle /start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to the Movie Recommender Bot!')

# Function to handle incoming messages
def handle_message(update: Update, context: CallbackContext) -> None:
    # Get the user's message
    user_message = update.message.text
    
    # Load your machine learning model (replace this with your actual model loading code)
    
    # Make predictions using your model (replace this with your actual prediction code)
    recommendation,recommended_movie_posters = recommend(user_message)
    update.message.reply_text(f'You might like these movies')
    for i in range (0, 5):
    # Send the movie recommendation back to the user
        #update.message.reply_text(f'-> {recommendation[i]}')
        update.message.reply_photo(photo = recommended_movie_posters[i], caption=f'{recommendation[i]}')

# Set up the Telegram bot
def main() -> None:
    # Initialize the updater with your bot token
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register command handlers
    dp.add_handler(CommandHandler("start", start))

    # Register a message handler to handle all incoming text messages
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the Bot
    updater.start_polling()

    # Run the Flask application to handle incoming webhook requests
    app.run(port=8443)

    # Run the bot until you send a signal to stop it
    updater.idle()

if __name__ == '__main__':
    main()
