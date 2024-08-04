import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Replace 'YOUR_TOKEN_HERE' with your Bot's API token
TOKEN = '7288721780:AAHZwjBK3LYaNXm7OPmEARaUuyuJUunNdQI'
CHAT_ID = '548329986'
previous_rate = None  # Variable to store the previous exchange rate


async def get_exchange_rate():
    url = 'https://open.er-api.com/v6/latest/JPY'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        rate = data['rates'].get('INR')
        return rate
    else:
        print(f"Error fetching data: {response.status_code}")
        return None


async def send_exchange_rate(context: ContextTypes.DEFAULT_TYPE):
    global previous_rate
    rate = await get_exchange_rate()

    if rate is not None:
        message = f"The current exchange rate from JPY to INR is {rate:.4f}."

        if previous_rate is not None:
            # Calculate percentage change
            change = ((rate - previous_rate) / previous_rate) * 100
            change_direction = "increased" if change > 0 else "decreased" if change < 0 else "remained the same"
            message += f"\nThis is a {abs(change):.2f}% {change_direction} compared to the last rate."

        # Update previous rate
        previous_rate = rate
    else:
        message = "Failed to retrieve the exchange rate."

    await context.bot.send_message(chat_id=context.job.chat_id, text=message)


async def schedule_messages(context: ContextTypes.DEFAULT_TYPE):
    context.job_queue.run_repeating(send_exchange_rate, interval=3 * 3600, first=0)  # every 3 hours


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! The bot will send you the exchange rate every 3 hours.")
    context.job_queue.run_once(schedule_messages, 0)  # Start the message scheduling immediately


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.run_polling()


if __name__ == '__main__':
    main()
