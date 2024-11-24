# **Telegram Bot with Flask Server for Message Automation**

This project is a Python-based Telegram bot that automates the process of sending messages to users in a specified Telegram group or channel. The bot downloads a session file from a Google Drive link and interacts with users in the group by sending them a predefined message. 

It includes a Flask server to provide health-check endpoints and ensure the bot remains active.

## **Key Features**
- **Session File Download**: The bot downloads a session file from Google Drive to authenticate with Telegram.
- **Message Sending**: The bot sends messages to group members, ensuring that previously contacted users are skipped.
- **Rate Limiting**: To avoid spamming, a 10-minute delay is added between messages.
- **Flask Server**: A Flask-based web server serves a health check endpoint to monitor bot status.

## **Requirements**
- Python 3.x
- `telethon` library
- `requests` library
- `flask` library
- A valid Google Drive link to download the session file

## **Setup Instructions**

1. Clone this repository to your local machine.
2. Install the required Python libraries:

   ```bash
   pip install telethon flask requests

## **Setup Instructions**

1. **Update the script with your own API credentials and the correct session file link**:
   - Replace the `api_id` and `api_hash` with your own Telegram API credentials.
   - Replace the `source_channel_name` with the name of the source group/channel.
   - Provide the correct Google Drive link in the `drive_link` variable.

## **Running the Bot**

To run the bot, use the following command

    ```bash
    python joinme.py

## **Flask Web Server**

The bot includes a simple Flask server to provide basic web interactions:

- **Home Page**: Displays a simple greeting message.
- **Health Check Endpoint**: The `/health_check` route checks if the bot is running and returns a status message.

You can access the health check endpoint by visiting:

```bash
http://localhost:8000/health_check

## **Contributing**

If you'd like to contribute to the development of this bot, feel free to open an issue or submit a pull request. Whether it's a bug fix, new feature, or documentation improvement, contributions are welcome.
