from telethon.sync import TelegramClient
from dotenv import load_dotenv
import asyncio, time, os

load_dotenv()

# Replace these with your own values
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
CHANNEL_NAME = os.getenv('CHANNEL_NAME')
prevmsg = "initial message"

# Create a new TelegramClient instance
client = TelegramClient('session_name', API_ID, API_HASH)

async def get_channel_messages():
    async with client:
        # Replace 'your_channel_username' with the actual username of the channel
        async for message in client.iter_messages(CHANNEL_NAME, limit=1):
            global prevmsg
            if(prevmsg == "initial message" or prevmsg != message.text):
                prevmsg = message.text
                print(message.text)
            else:
                print("No messages")

# Run the script
# if __name__ == '__main__':
#     client.loop.run_until_complete(get_channel_messages())

async def check_every_seconds():
    while True:
        try:
            print("_________________________________")
            await get_channel_messages()
            # print("Run every 12 seconds...")
        except Exception as e:
            print(str(e))
        await asyncio.sleep(120)

asyncio.run(check_every_seconds())