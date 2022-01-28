from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from commands.constants import *

# Creates the response for main menu with the text message and inline keyboard
def createMainMenuKeyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
        InlineKeyboardButton("📝 Country list", callback_data=str(PAGENUM)),
        InlineKeyboardButton("🔎 Search country", callback_data='searchCountry'),
        InlineKeyboardButton("❓ Help", callback_data='help'),
        ],
    ]


    return InlineKeyboardMarkup(keyboard)
    


def createMainMenuMessage(update: Update) -> str:
    user = update.effective_user
    reply = f"Welcome to COVID-19 statistics bot, {user.name}!👋\n\nHere you can:\n-View cases data for each country🦠\n\
-View deaths data for each country💀\n-View recovery data for each country!💉\n\nClick 'search country' to search by name OR 2 letter code🔎\nOR\n\
Click 'Print countries' to see all available coutnries 📝\n\nIf you need more help press the 'help' button ❓"

    
    return reply


# /start command telegram bot
def start(update: Update, context: CallbackContext) -> int:
    # Creates a keyboard and message
    reply = createMainMenuMessage(update)
    replyMarkup = createMainMenuKeyboard()
    update.message.reply_text(reply, reply_markup=replyMarkup)

    return MENU


# Runs when the user clicks menu
def start_over(update: Update, context: CallbackContext) -> int:
    """Prompt same text & keyboard as `start` does but not as new message"""
    # Get CallbackQuery from Update
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    query.answer()

    reply = createMainMenuMessage(update)
    replyMarkup = createMainMenuKeyboard()
    context.bot.send_message(chat_id=update.callback_query.from_user.id, text=reply, reply_markup=replyMarkup)


    return MENU


# Help button
def help(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()

    keyboard = [
        [InlineKeyboardButton("☰ Menu", callback_data="menu")]
    ] 

    reply_markup = InlineKeyboardMarkup(keyboard)
    message = "🔎By clicking 'Search country', you have the option to search a country by its name, e.g Germany and you have an option to search by 2 letter code e.g DE.\n\n\
📝By clicking 'Print countries', you can see all the available countries to which the bot can provide information. Click one of the countries to see its statistics."
    context.bot.send_message(chat_id=update.callback_query.from_user.id, text=message, reply_markup=reply_markup)


    return MENU