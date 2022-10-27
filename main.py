import logging
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters


logging.basicConfig(
    filename = "log.txt",
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)




def hello(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f"Hello {update.effective_user.first_name}")


def start (update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr' Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True)
    )


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("""Введите выражение содержащее 2 числа \n Например 2 / 2""")


def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)


def calculator(update: Update, context: CallbackContext) -> None:
    msg = update.message.text
    msg = msg.replace(" ", "")
    result = None
    if "+" in msg:
        msg_to_list = [float(i) for i in msg.split("+")]
        if len(msg_to_list) > 0:
            result = round(sum(msg_to_list), 4)
        else:
            result = "Я умею находить исключительно 2 числа"
    if "-" in msg:
        msg_to_list = [float(i) for i in msg.split("-")]
        print(msg_to_list)
        if len(msg_to_list) == 2:
            result = round(msg_to_list[0] - msg_to_list[1], 4)
        else:
            result = "Я умею находить исключительно 2 числа"
    if "*" in msg:
        msg_to_list = [float(i) for i in msg.split("*") if i.isdecimal() or i.isdigit()]
        if len(msg_to_list) == 2:
            result = round(msg_to_list[0] * msg_to_list[1], 4)
        else:
            result = "Я умею находить исключительно 2 числа"
    if "/" in msg:
        msg_to_list = [float(i) for i in msg.split("/") if i.isdecimal() or i.isdigit()]
        if len(msg_to_list) == 2:
            try:
                result = round(msg_to_list[0] / msg_to_list[1], 4)
            except ZeroDivisionError:
                result = "Делить на 0 нельзя"
        else:
            result = "Я умею находить исключительно 2 числа"
    update.message.reply_text(result)
    logger.info(f"{update.effective_user.username}: {update.message.text} answer: {result}")


def main():
    updater = Updater("5794567195:AAHjYRkdUxbutcMe95nkfWDoT4zqYbHKvCM")

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", hello))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("hello", hello))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, calculator))

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
