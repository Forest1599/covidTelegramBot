from telegram.ext.updater import Updater
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters
import logging
import commands

# Gets the bot token
def getToken() -> str:
    with open("project/token.txt", "r") as f:
        return f.read()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def main() -> None:
    updater = Updater(getToken())

    # Dispatcher that runs the functions for different events
    dispatcher = updater.dispatcher 

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', commands.start)],
        states={
            # The main menu
            commands.MENU: [
                CallbackQueryHandler(commands.printCountryList, pattern='^' + str(commands.PAGENUM) + '$'),
                CallbackQueryHandler(commands.help, pattern='^help$'),
                CallbackQueryHandler(commands.start_over, pattern="^menu$"),
                CallbackQueryHandler(commands.getCountryName, pattern="^searchCountry$")
            ],
            # Print countries option
            commands.COUNTRYLIST: [
                CallbackQueryHandler(commands.printCountryList, pattern='^' + str(commands.PAGENUM) + '$'),
                CallbackQueryHandler(commands.printCountryList, pattern='^' + str(commands.PAGENUM+1) + '$'),
                CallbackQueryHandler(commands.printCountryList, pattern='^' + str(commands.PAGENUM+2) + '$'),
                CallbackQueryHandler(commands.printCountryData, pattern='^'+"[A-Z]{2}"),
                CallbackQueryHandler(commands.start_over, pattern='^menu$')
            ],
            # Search country option
            commands.COUNTRYSEARCH: [
                MessageHandler(Filters.text & ~Filters.command, commands.searchCountry),
                CallbackQueryHandler(commands.getCountryName, pattern="^searchCountry$"),
                CallbackQueryHandler(commands.start_over, pattern='^menu$')
            ],
        },
        fallbacks=[CommandHandler('start', commands.start)],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling() # Starts the bot
    updater.idle() # Runs the bot until Ctrl-C is pressed


if __name__ == "__main__":
    main()


