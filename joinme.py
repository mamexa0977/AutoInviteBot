from telethon import TelegramClient
import asyncio
import requests
import threading
from flask import Flask, jsonify

# Replace with your Telegram API credentials
api_id = ''  # Your API ID
api_hash = ''  # Your API Hash

# Channel name (replace with the actual username or ID)
source_channel_name = 'Group name from telegram'  # The name of the source channel

# Google Drive file link for session file
drive_link = "our session file"

# Function to download session file from Google Drive
def download_session_file():
    response = requests.get(drive_link)
    if response.status_code == 200:
        with open('session_name.session', 'wb') as f:
            f.write(response.content)
        print("Session file downloaded.", flush=True)
    else:
        print("Failed to download session file. Status code:", response.status_code, flush=True)

# Function to get previously contacted users
async def get_previously_contacted_users(client):
    previously_contacted = set()
    async for dialog in client.iter_dialogs():
        if dialog.is_user and not dialog.entity.bot:
            previously_contacted.add(dialog.entity.id)
    return previously_contacted

async def start_bot():
    # Download the session file before creating the Telegram client
    download_session_file()

    async with TelegramClient('session_name', api_id, api_hash) as client:
        print("Bot started.", flush=True)

        # Fetch all dialogs (chats, groups, and channels the bot has access to)
        dialogs = await client.get_dialogs()

        # Find the source channel by its name
        source_channel = next((dialog.entity for dialog in dialogs if dialog.name == source_channel_name), None)

        if not source_channel:
            print("Could not find the source channel.", flush=True)
            return

        # Get the list of previously contacted users
        previously_contacted = await get_previously_contacted_users(client)
        print(f"Found {len(previously_contacted)} previously contacted users.", flush=True)

        # Get the members from the source channel
        members = await client.get_participants(source_channel)

        for member in members:
            try:
                # Skip members already contacted
                if member.id in previously_contacted:
                    print(f"Skipping {member.username if member.username else member.id} (already contacted)", flush=True)
                    continue

                # Send the message to the member
                await client.send_message(member, "Join link and description for people to join")
                print(f"Message sent to {member.username if member.username else member.id}", flush=True)

                # Wait for 10 minute before sending the next message
                await asyncio.sleep(600)

            except Exception as e:
                print(f"Failed to send message to {member.username if member.username else member.id}: {e}", flush=True)

# Flask app setup
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, this is the home page of the bot!"

# Health check route to avoid inactivity
@app.route('/health_check', methods=['GET'])
def health_check():
    return jsonify({"status": "OK"}), 200

# Function to run the bot in a separate thread with a manual event loop
def run_bot():
    loop = asyncio.new_event_loop()  # Create a new event loop
    asyncio.set_event_loop(loop)     # Set the new loop as the event loop
    loop.run_until_complete(start_bot())  # Run the bot with this loop
    loop.close()  # Close the loop once done

if __name__ == '__main__':
    # Start the bot in a separate thread
    threading.Thread(target=run_bot).start()
    # Start the Flask server
    app.run(host='0.0.0.0', port=8000)
