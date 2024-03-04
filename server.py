from telethon.sync import TelegramClient, events
from dotenv import load_dotenv
from web3 import Web3
import asyncio, time, os

load_dotenv()

# Replace these with your own values
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
CHANNEL_NAME = os.getenv('CHANNEL_NAME')
BUY_AMOUNT = os.getenv('BUY_AMOUNT')
prevmsg = "initial message"

# Create a new TelegramClient instance
client = TelegramClient('session_name', API_ID, API_HASH)

def solution1(addr):
    w3 = Web3(Web3.HTTPProvider('https://ethereum-rpc.publicnode.com'))
    try:
        contract = w3.eth.contract(address=Web3.to_checksum_address(addr), abi=[{"constant":True,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":False,"stateMutability":"view","type":"function"}])
        contract.functions.decimals().call()
    except Exception as e:
        return False
    return True

def check_if_eth_address(addr):
    if(addr[:2] != "0x"):
        return False
    else:
        return solution1(addr)

def filter_eth_address(message):
    start = message.find('0x')
    return message[start:start+42]

async def run_banana(token):
    # run /start command
    await client.send_message('BananaGunSniper_bot', '/start')
    # click manual buyer
    message = await client.get_messages('BananaGunSniper_bot', limit=1)
    await message[0].click(1, 0)
    # enter token address
    await client.send_message('BananaGunSniper_bot', token)
    # click buy x amount
    message = await client.get_messages('BananaGunSniper_bot', limit=1)
    await message[0].click(4, 1)
    # input amount as reply_to
    message = (await client.iter_messages('BananaGunSniper_bot', limit=1).__anext__())
    await client.send_message('BananaGunSniper_bot', BUY_AMOUNT, reply_to=message.id)
    print("Success")

# @client.on(events.NewMessage)
# async def handler(event):
#     message_id = event.id
#     print(f"The message ID is: {message_id}")


async def get_channel_messages():
    async for message in client.iter_messages(CHANNEL_NAME, limit=1):
        global prevmsg
        if(prevmsg == "initial message"):
            prevmsg = message.text
        elif(prevmsg != message.text):
            prevmsg = message.text
            # print(message.text)
            address = filter_eth_address(message.text)
            isValid = check_if_eth_address(address)
            # print("Address: ", address)
            # print("Check ERC20 Address: ", isValid)
            if(isValid):
                # print("Running Banana...")
                await run_banana(address)
        # else:
        #     print("No new messages")

async def check_every_seconds():
    while True:
        try:
            async with client:
                # print("Checking...")
                await get_channel_messages()
                # print("Run every 12 seconds...")
        except Exception as e:
            print(str(e))
        await asyncio.sleep(5)

asyncio.run(check_every_seconds())
