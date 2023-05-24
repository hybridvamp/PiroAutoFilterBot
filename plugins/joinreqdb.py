import pymongo
from pyrogram import Client, filters, types
from info import DATABASE_NAME, DATABASE_URI, F_CHATID, COLLECTION_NAME, LOG_CHANNEL

# Initialize MongoDB client
myclient = pymongo.MongoClient(DATABASE_URI)
mydb = myclient[DATABASE_NAME]
mycol = mydb[COLLECTION_NAME]


@Client.on_chat_join_request((filters.group | filters.channel) & filters.chat(F_CHATID) if F_CHATID else (filters.group | filters.channel))
async def handle_join_request(client, message: ChatJoinRequest):
    user_id = message.from_user.id
    
    # Find the user in the database
    user = await mycol.find_one({"fsub_userid": user_id})
    
    if user is None:
        # User ID not found in the database, save it
        await mycol.insert_one({"fsub_userid": user_id})
        await client.send_message(LOG_CHANNEL, f"{message.from_user.mention} sent a join request to the channel and was added to the database.")
        print(f"User ID {user_id} saved to the database.")
    else:
        # User ID already exists in the database, do not save again
        print(f"User ID {user_id} already exists in the database.")
