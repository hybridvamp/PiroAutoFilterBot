import pymongo
from pyrogram import Client, filters
from pyrogram.types import Message

from info import DATABASE_URI, DATABASE_NAME, CHAT_ID

API_ID = 3881325
API_HASH = "1ebf12e67222683abe1c01f0209b79df"
BOT_TOKEN = "5725763519:AAErtokI_ODgqDA6QQLpCxZJBUoj1NvmgI8"

app = Client(
    "my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

myclient = pymongo.MongoClient(DATABASE_URI)
mydb = myclient[DATABASE_NAME]
POST_ID = 5

@app.on_message(filters.chat(CHAT_ID))
async def handle_new_files(_, message: Message):
    # Increment the total files count in the database
        mycol = mydb["file_counts"]
        myquery = {"_id": "total_files_sent"}
        newvalues = {"$inc": {"count": 1}}
        mycol.update_one(myquery, newvalues, upsert=True)
                        
        # Get the current total files count from the database
        count = mycol.find_one(myquery)["count"]
                                    
        # Edit the post in the chat with the new total files count
        await app.edit_message_text(
            chat_id=CHAT_ID,
            message_id=POST_ID,
            text=f"Total files sent: {count}"
        )

app.run()