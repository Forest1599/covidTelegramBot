from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import CallbackContext
import flag
import commands.helpers as helpers
import commands.constants as constants
import commands.covidScraper as covidScraper


def createCountryButtons(pageNum) -> list:
    # Scrapes all country data
    countryNames = covidScraper.getCountryData()
    countryCodes = helpers.getCountryCodes()

    columns = []
    row = []

    # Each page divided into 80 buttons
    # Given the pageNum calculates the index where the loop starts
    index = pageNum * 80
    limit = (pageNum * 80) + 80

    # While the index is smaller and the list is not fully printed out
    while index < limit and index < len(countryNames):
        countryName = countryNames[index].text.replace("\n", "-").split("-")[2]
        countryCode = countryCodes[countryName.upper()]

        # Adds element to the row if it can get the countryCode from countries.json
        # (HAS COUNTRIES WITHOUT COUNTRY CODE) Decided to not use those countries as they do not posses any flags and coutnry codes
        if countryCode != "":
            row.append(InlineKeyboardButton(f"{countryCode} - {flag.flag(countryCode)}", callback_data=countryCode))

        # Each row has 5 elements so if it has 5 elements in the row it appends it to the column
        if len(row) == 5:
            columns.append(row)
            row = []
        index +=1


    return columns


def createKeyboard(pageNum: int) -> list:
    keyboard = createCountryButtons(pageNum)

    navigation = []

    # If it is the 2st or 3nd page adds back button to go back a page
    if pageNum > 0:
        navigation.append(InlineKeyboardButton("⬅️ Back page", callback_data=str(pageNum-1)))
    # If it is the 1st or 2nd page adds a next button to go forward a page
    if pageNum < 2:
        navigation.append(InlineKeyboardButton("➡️ Next page", callback_data=str(pageNum+1)))

    # Adds the next button and back button if needed
    keyboard.append(navigation)
    # adds menu as a button to back to the main menu
    keyboard.append([InlineKeyboardButton("☰ Menu", callback_data='menu')])

    
    return keyboard
    

def printCountryList(update: Update, context: CallbackContext) -> int:
    # Get CallbackQuery from Update
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    query.answer()

    # Gets the pageNum from the callback_data
    pageNum = int(update.callback_query.data)
    keyboard = createKeyboard(pageNum)

    reply_markup = InlineKeyboardMarkup(keyboard)

    # Sends a new message with the 80 countries list
    context.bot.send_message(chat_id=update.callback_query.from_user.id, text="Country List:", reply_markup=reply_markup)

    return constants.COUNTRYLIST


def printCountryData(update: Update, context: CallbackContext) -> int:
    # Get CallbackQuery from Update
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    query.answer()

    # Gets the 2 letters that were used to call this function, which is the country code
    countryCode = update.callback_query.data
    # Gets the specified country data
    statisticDictionary = covidScraper.getCountryStatistics(countryCode)

    keyboard = [
        [
            InlineKeyboardButton("📝 Print list again", callback_data=constants.PAGENUM),
            InlineKeyboardButton("☰ Menu", callback_data="menu")
        ]
    ]

    replyMarkup = InlineKeyboardMarkup(keyboard)

    # Creates a back to list button and menu button
    report = helpers.generateReport(statisticDictionary, countryCode) # Generates a report
    context.bot.send_message(chat_id=update.callback_query.from_user.id, text=f"{report}", reply_markup=replyMarkup, parse_mode=ParseMode.HTML)

    return constants.COUNTRYLIST



        

    





    
    