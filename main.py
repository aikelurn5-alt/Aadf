import os
import telebot
from flask import Flask, request
from stripe import stripe_payment

# Render ပေါ်တွင် environment variable မှ token ကိုယူသုံးမည်
API_TOKEN = os.environ.get('BOT_TOKEN', '8053442928:AAFJP6H7b85-5wdUck2O_L7hQ2DM_ewOtp4')
WEBHOOK_URL = os.environ.get('WEBHOOK_URL', '')  # Render က ပေးတဲ့ URL

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# Webhook route
@app.route('/webhook/' + API_TOKEN, methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        return 'Invalid content type', 403

# Command handlers
@bot.message_handler(commands=['stripe'])
def handle_stripe(message):
    stripe_payment(message, bot)

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am EchoBot.
use /stripe to check\
""")

# Health check route for Render
@app.route('/')
def health_check():
    return 'Bot is running!'

if __name__ == "__main__":
    # Set webhook
    if WEBHOOK_URL:
        bot.remove_webhook()
        bot.set_webhook(url=WEBHOOK_URL + '/webhook/' + API_TOKEN)
    
    # Run Flask app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)