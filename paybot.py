import telebot
import requests

# 🔹 Replace with your actual Telegram bot token
BOT_TOKEN = "8159694796:AAFn4QaJDuQ7_Avqs3rn76tHHMbdzNP9Fhs"

# 🔹 Replace with your actual Airtable API details
AIRTABLE_API_KEY = "pat6SAYFxSfCsNYUK"
AIRTABLE_BASE_ID = "appHHONLoGAqC9pL8"
AIRTABLE_TABLE_NAME = "Affiliate Tracking"

# Initialize the bot
bot = telebot.TeleBot(BOT_TOKEN)

# Temporary storage for user input
user_data = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Send your payment screenshot to confirm your purchase.")

@bot.message_handler(content_types=['photo'])
def handle_payment_proof(message):
    user_id = message.chat.id
    file_id = message.photo[-1].file_id
    user_data[user_id] = {"proof": file_id}

    bot.send_message(user_id, "Enter your full name:")
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    user_id = message.chat.id
    user_data[user_id]["name"] = message.text

    bot.send_message(user_id, "Enter your Telegram username or phone number:")
    bot.register_next_step_handler(message, get_contact)

def get_contact(message):
    user_id = message.chat.id
    user_data[user_id]["contact"] = message.text

    bot.send_message(user_id, "Enter the affiliate code (if any):")
    bot.register_next_step_handler(message, get_affiliate_code)

def get_affiliate_code(message):
    user_id = message.chat.id
    user_data[user_id]["affiliate_code"] = message.text

    bot.send_message(user_id, "Enter the amount paid (in USD or EGP):")
    bot.register_next_step_handler(message, get_amount)

def get_amount(message):
    user_id = message.chat.id
    user_data[user_id]["amount"] = message.text

    # Save to Airtable
    save_to_airtable(user_id)
    bot.send_message(user_id, "✅ Payment recorded! We will verify and grant access soon.")

def save_to_airtable(user_id):
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "fields": {
            "Buyer Name": user_data[user_id]["name"],
            "Buyer Contact": user_data[user_id]["contact"],
            "Affiliate Code": user_data[user_id]["affiliate_code"],
            "Amount Paid": user_data[user_id]["amount"],
            "Payment Status": "Pending"
        }
    }
    
    # Debugging: Print request details
    print("Sending data to Airtable:", data)

    response = requests.post(url, json=data, headers=headers)
    
    # Debugging: Print the response
    print("Airtable response:", response.status_code, response.text)

    return response.json()

# Start the bot
bot.polling(none_stop=True)

