import pyttsx3
import os
import requests
from telegram import Update, Bot
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from dotenv import load_dotenv
load_dotenv()

# Initialize the pyttsx3 text-to-speech engine
engine = pyttsx3.init()

voice_id = 'com_google_speech_synthesis_{}'.format('en-US-Wavenet-F')
engine.setProperty('voice', voice_id)
engine.setProperty('rate', 80)

def start(update: Update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Namaste, i am Hrocha. from sneva art studio send me text prompt i will convert it to ai art image!')
    
    # Convert text to speech and play it back using pyttsx3
    engine.say("Namaste, i am Hrocha. from sneva art studio send me text prompt i will convert it to ai art image!")
    engine.runAndWait()


def generate_art(update: Update, context):
    """Generate AI art based on a text prompt."""
    # Get text prompt from user
    text = update.message.text

    # Add prompt text to user's message
    #prompt_text = "Can you generate a picture of " + text

    # Generate AI art using the Stable Diffusion model
    url = 'https://api.openai.com/v1/images/generations'
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer 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'}
    data = {
        'model': 'image-alpha-001',
        'prompt': text,
        'num_images': 1,
        'size': '256x256',
        'response_format': 'url'
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()['data'][0]['url']

    # Send generated art to user
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=result)
    update.message.reply_text('Your Ai art is ready...')
    engine.say("Your Ai art is ready...")
    engine.runAndWait()

def main():
    """Start the bot."""
    # Set up the Telegram bot
    updater = Updater(token="6258364844:AAEyqXOSeLKuv1gauS_YNIdGtRtWNKpxmKc", use_context=True)
    dp = updater.dispatcher

    # Add handlers for commands and messages
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, generate_art))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
