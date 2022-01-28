from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, ParseMode
from telegram.ext import CallbackContext
import flag
from difflib import get_close_matches
import commands.constants as constants
import commands.helpers as helpers
import commands.covidScraper as covidScraper

# Runs when search country is selected
def getCountryName(update: Update, context: CallbackContext) -> int:
    context.bot.send_message(chat_id=update.callback_query.from_user.id, text=f"Please input country name OR country 2 letter code e.g Germany/DE", reply_markup=ReplyKeyboardRemove())

    
    return constants.COUNTRYSEARCH

# If the country is recognized
def validCountryInputResponse(update: Update, countryCode: str) -> None:
    # Generates a report
    statisticDictionary = covidScraper.getCountryStatistics(countryCode)
    report = helpers.generateReport(statisticDictionary, countryCode)

    # Creates an inline keyboard
    keyboard = [
        [
            InlineKeyboardButton("🔎 Search again", callback_data="searchCountry"),
            InlineKeyboardButton("☰ Menu", callback_data="menu")
        ]
    ]
    replyMarkup = InlineKeyboardMarkup(keyboard) # Creates a keyboard

    update.message.reply_text(text=f"{report}", reply_markup=replyMarkup, parse_mode=ParseMode.HTML)


def invalidCountryInputResponse(update: Update, countryName: str, countryCodes: dict) -> None:
    # Checks if it can find any similar matches in countryCodes.json
    similarMatches = get_close_matches(countryName.upper(), countryCodes.keys())

    # If there is at least 1 similar match
    if len(similarMatches) > 0:
        reply_keyboard = [similarMatches]

        update.message.reply_text(
            text="Sorry, could not find the country specified.. 🤔\nchoose one from the list 👇",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder="Did you mean?"
            ),
        )
    # If there are no similar matches
    else:
        keyboard = [
            [InlineKeyboardButton("☰ Menu", callback_data="menu")]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(text="Sorry, could not find the country.. Type again or go to the menu..", reply_markup=reply_markup)


def countryFoundMessage(update: Update, countryName: str, countryCode: str) -> None:
    update.message.reply_text(text=f"Searching {countryName.title()} {flag.flag(countryCode)} statistics.. 🔎", reply_markup=ReplyKeyboardRemove())

    return constants.COUNTRYSEARCH


def searchCountry(update: Update, context: CallbackContext) -> int:
    countryName = update.message.text
    countryCodes = helpers.getCountryCodes()

    # Checks if the inputted value is 2 in length and is inside countryCodes.json e.g(DE, LV, GB)
    if len(countryName) == 2 and countryName.upper() in countryCodes.values():
        countryCode = countryName.upper() # for inputs that are lowercase
        countryFoundMessage(update, helpers.getCountryNameFromCountryCode(countryCodes, countryCode), countryCode)
        validCountryInputResponse(update, countryCode)

    # Checks if the inputted value is inside countryCodes.json
    elif countryName.upper() in countryCodes.keys():
        countryCode = countryCodes[countryName.upper()]
        countryFoundMessage(update, countryName, countryCode) # sends messsage to remove the markup keyboard
        validCountryInputResponse(update, countryCode)
        
    # If it could not find the value
    else:
        invalidCountryInputResponse(update, countryName, countryCodes)
    
    
    return constants.COUNTRYSEARCH