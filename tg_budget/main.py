import os

from loguru import logger
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      ReplyKeyboardMarkup, ReplyKeyboardRemove, Update)
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler,
                          ContextTypes, ConversationHandler, MessageHandler,
                          filters)

from tg_budget import db_tools

BOT_TOKEN = os.environ.get('BOT_TOKEN', '')
CURENCY = ['USD', 'EUR', 'RSD']


@logger.catch
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await db_tools.add_user(user.id)
    keyboard = [
        [
            InlineKeyboardButton('Add income', callback_data='Add income'),
            InlineKeyboardButton('Option 2', callback_data='2'),
        ],
        [InlineKeyboardButton('Option 3', callback_data='3')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(user.id, 'Menu', reply_markup=reply_markup)


@logger.catch
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=f'Selected option: {query.data}')


@logger.catch
async def add_income_from(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:

    await update.message.reply_text('Введите название источника дохода')

    return 'INCOME_NAME'


async def add_income_curency(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['income_from_name'] = update.message.text
    reply_keyboard = [[curency] for curency in CURENCY]
    markup = ReplyKeyboardMarkup(reply_keyboard)
    await update.message.reply_text('Выберите валюту источника', reply_markup=markup)
    return 'INCOME_CURENCY'


async def add_income_done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['income_from_curency'] = update.message.text
    await update.message.reply_text(str(context.user_data), reply_markup=ReplyKeyboardRemove())
    context.user_data.clear()
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info('User %s canceled the conversation.', user.first_name)
    await update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


@logger.catch
def main() -> None:

    '''Start the bot.'''
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler('start', start, filters.ChatType.PRIVATE))

    add_income_handler = ConversationHandler(

        entry_points=[CommandHandler('add_income', add_income_from)],

        states={

            'INCOME_NAME': [MessageHandler(filters.ChatType.PRIVATE & filters.TEXT, add_income_curency)],
            'INCOME_CURENCY': [MessageHandler(filters.Regex(rf'^{"|".join(CURENCY)}$'), add_income_done)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(add_income_handler)
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling()


if __name__ == '__main__':
    main()
