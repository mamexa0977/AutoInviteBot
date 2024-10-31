from telethon import TelegramClient
import asyncio
import requests
import threading
from flask import Flask, jsonify

# Replace with your Telegram API credentials
api_id = '29935142'  # Your API ID
api_hash = 'b3fd3a84a34b3a203f846d9a5e8b8125'  # Your API Hash

# Channel names (replace with actual usernames or IDs)
source_channel_name = 'Miki FX Community'  # The name of the source channel

# Google Drive file link for session file
drive_link = "https://utfs.io/f/v9t8dkdjIAnjWwuQyZGL5h14CrkTz2KPAEXlgmbFpnSvD8js"

# Function to download session file from Google Drive
def download_session_file():
    response = requests.get(drive_link)
    if response.status_code == 200:
        with open('session_name.session', 'wb') as f:
            f.write(response.content)
        print("Session file downloaded.")
    else:
        print("Failed to download session file. Status code:", response.status_code)

async def start_bot():
    # Download the session file before creating the Telegram client
    download_session_file()

    async with TelegramClient('session_name', api_id, api_hash) as client:
        print("Bot started.")

        # Fetch all dialogs (chats, groups, and channels the bot has access to)
        dialogs = await client.get_dialogs()

        # Find the source channel by its name
        source_channel = next((dialog.entity for dialog in dialogs if dialog.name == source_channel_name), None)

        if not source_channel:
            print("Could not find the source channel.")
            return

        # Get the members from the source channel
        members = await client.get_participants(source_channel)

        # Send a simple "Hi" message to each member
        for member in members:
            try:
                if member.username:  # Check if the member has a username
                    await client.send_message(member, "የ AB MARSHAL 100$ to 30k በዚ ቻናል ይለቀቃል። @fxnesa ለ Quality አገልግሎት እስከ እሮብ ሙከራ ላይ ይቆያል። @fxnesa")  # Send "Hi" message
                    print(f"Message sent to {member.username}")
                else:
                    print(f"Member {member.id} does not have a username; skipping.")
                
                # Wait for 1 minute before sending the next message
                await asyncio.sleep(60)  # 60 seconds delay
            except Exception as e:
                print(f"Failed to send message to {member.username if member.username else member.id}: {e}")

# Flask app setup
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, this is the home page of the bot!"

# Health check route to avoid inactivity
@app.route('/health_check', methods=['GET'])
def health_check():
    return jsonify({"status": "OK"}), 200

# Function to run the bot in a separate thread
def run_bot():
    asyncio.run(start_bot())

if __name__ == '__main__':
    # Start the bot in a separate thread
    threading.Thread(target=run_bot).start()
    # Start the Flask server
    app.run(host='0.0.0.0', port=8000)
