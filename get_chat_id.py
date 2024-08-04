import asyncio
import telegram

# Replace 'YOUR_TOKEN_HERE' with your Bot's API token
TOKEN = '7288721780:AAHZwjBK3LYaNXm7OPmEARaUuyuJUunNdQI'


async def get_chat_id():
    bot = telegram.Bot(token=TOKEN)

    try:
        # Get the latest updates from your bot
        updates = await bot.get_updates()
        if not updates:
            print("No updates found.")
        else:
            for update in updates:
                print(update)  # Print the whole update to see its content
                # Print the chat ID of the latest message if it exists
                if update.message:
                    print(f"Chat ID: {update.message.chat.id}")
                else:
                    print("No message found in update.")
    except Exception as e:
        print(f"Error fetching updates: {e}")


if __name__ == '__main__':
    asyncio.run(get_chat_id())