from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import threading
import Keys as Key

print('bot started..')


def start_cmd(update, context):
    keyboard = [
        [InlineKeyboardButton("XXX", url='XXX')],
        [InlineKeyboardButton("XXX", url='XXX')],
        [InlineKeyboardButton("XXX", url='XXX')],
        [InlineKeyboardButton("XXX", url='XXX')],
        [InlineKeyboardButton("XXX", url='XXX')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('כללי התנהגות בחדרי השיחה:\n'
                              '1. יש לשמור על שיח מכבד\n'
                              '2. כולם רצויים ומוזמנים להיות חלק מהשיחה או מהקבוצה\n'
                              '3. אין להשתמש באלימות מילולית או לנהל שיח פוגעני\n'
                              '4. יש לשמור על סובלנות וסבלנות כלפי האחר\n'
                              '5. המטרה של חדרי השיחה היא שיח קבוצתי ולא אישי\n'
                              '6.אין חובה להשתתף בשיחה\n'
                              'אנא בחר את חדר השיחה הרצוי:', reply_markup=reply_markup)


def groupsToAdmin(chat_id):
    return {
        Key.genderIdentity: Key.genderIdentity_admin,
        Key.cyberbullying: Key.cyberbullying_admin,
        Key.depressionAndStress: Key.depressionAndStress_admin,
        Key.domesticViolence: Key.domesticViolence_admin,
        Key.eatingDisorders: Key.eatingDisorders_admin,
    }[chat_id]


def adminToGroup(chat_id):
    return {
        Key.genderIdentity_admin: Key.genderIdentity,
        Key.cyberbullying_admin: Key.cyberbullying,
        Key.depressionAndStress_admin: Key.depressionAndStress,
        Key.domesticViolence_admin: Key.domesticViolence,
        Key.eatingDisorders_admin: Key.eatingDisorders,
    }[chat_id]


def forwardToGroupChat(update, context):
    text = str(update.message.text).lower()
    for r in (("hello", "hey"),
              ("mister", "\U0001f600"),
              ):
        text = text.replace(*r)
    context.bot.send_message(adminToGroup(update.message.chat.id), text)


def forwardToExpert(update, context):
    text = str(update.message.text).lower()
    response = text
    context.bot.send_message(groupsToAdmin(update.message.chat.id),
                             update.message.from_user.first_name + ": " + response)


def handleMsg(update, context):
    text = str(update.message.text).lower()
    response = "לחדרי השיחה, הקלד : start/"
    if text in ("מה קורה?", "היי", "מי אתה?"):
        response = "היי, אני אבי-בוט ותפקידי לעזור לכם להתחבר לחדרי השיחה"
    update.message.reply_text(response)


def error(update, context):
    print(f"Update {update} caused err {context.error}")


def mainBot():
    updater = Updater(Key.mainChat, use_context=True)
    dp = updater.dispatcher

    # adding handlers to the bot
    dp.add_handler(CommandHandler("start", start_cmd))
    dp.add_handler(MessageHandler(Filters.text, handleMsg))
    dp.add_error_handler(error)

    # checks all the time if user entered input
    updater.start_polling(1)


def forwardToExpertBot():
    updater = Updater(Key.forwardToExpert, use_context=True)
    dp = updater.dispatcher

    # adding handlers to the bot
    dp.add_handler(MessageHandler(Filters.text, forwardToExpert))
    dp.add_error_handler(error)

    # checks all the time if user entered input
    updater.start_polling(1)


def forwardToGroupChatBot():
    updater = Updater(Key.forwardToGroupChat, use_context=True)
    dp = updater.dispatcher

    # adding handlers to the bot
    dp.add_handler(MessageHandler(Filters.text, forwardToGroupChat))
    dp.add_error_handler(error)

    # checks all the time if user entered input
    updater.start_polling(1)


def main():
    t1 = threading.Thread(target=mainBot)
    t2 = threading.Thread(target=forwardToExpertBot)
    t3 = threading.Thread(target=forwardToGroupChatBot)
    t1.start()
    t2.start()
    t3.start()


main()
