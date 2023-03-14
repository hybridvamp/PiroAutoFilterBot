from datetime import datetime
from pyrogram import Client, filters
from pyrogram.errors import BadRequest

# set the channel ID where the bot is admin
channel_id = -1001708267003

# set the message ID that you want to edit
message_id = 5

# define a filter to only handle media files (exclude stickers, text, etc.)
media_filter = filters.document | filters.video | filters.audio | filters.voice

# define a function to update the message
async def update_message():
    global file_sent_count
    now = datetime.now().strftime("%d/%m/%Y")
    text = f"Total files sent by bot since 14/03/2023 till {now}: {file_sent_count}"
    try:
        await app.edit_message_text(chat_id=channel_id, message_id=message_id, text=text)
    except BadRequest as e:
        print(f"Failed to update message: {e}")

# get the current file count from the message
async def get_file_count():
    global file_sent_count
    try:
        message = await app.get_messages(chat_id=channel_id, message_ids=message_id)
        text = message.text
        file_sent_count = int(text.split()[-1])
    except:
        print("Failed to get file count")

# handle incoming media files
@app.on_message(filters.chat(channel_id) & media_filter)
async def handle_media(client, message):
    global file_sent_count
    file_sent_count += 1
    try:
        await update_message()
    except:
        print("Failed to update message")
