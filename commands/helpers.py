import json
import flag
import commands.covidScraper as covidScraper
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Reads the countryCodes.json
def getCountryCodes():
    with open("project/commands/countryCodes.json") as f:
        return json.load(f)

# Searches the country name with the country code
def getCountryNameFromCountryCode(countryCodes: dict, countryCode: str):
    for key, value in countryCodes.items():
        if value == countryCode:
            return key


# Generates a well structured report to the user after country selection
def generateReport(statisticDictionary: dict, countryCode: str) -> str:
    row_seperator = "\n_______________\n" # Seperator between Strings

    countryInfoString = f"📄Country info:\nCountry position: <b>{statisticDictionary['countryPos']}</b>\nCountry Name: {statisticDictionary['countryName']}\
{flag.flag(countryCode)}\nPopulation:  <b>{statisticDictionary['population']}</b>"

    countryCasesString = f"{row_seperator}\n🦠Cases info:\nTotal cases:  <b>{statisticDictionary['totalCases']}</b>\nNew cases today:  <b>{statisticDictionary['newCases']}</b>\n\
Active cases:  <b>{statisticDictionary['activeCases']}</b>\nSerious cases:  <b>{statisticDictionary['seriousCritical']}</b>\nCases 1M ppl:  <b>{statisticDictionary['totalCases1M']}</b>"

    countryDeathString = f"{row_seperator}\n💀Death info:\nTotal deaths:  <b>{statisticDictionary['totalDeaths']}</b>\nNew deaths today:  <b>{statisticDictionary['newDeaths']}</b>\n\
Deaths 1M ppl:  <b>{statisticDictionary['totalDeaths1M']}</b>"

    countryRecoveryString = f"{row_seperator}\n💉Recovery info:\nTotal recovered: <b>{statisticDictionary['totalRecovered']}</b>\nRecovered today:\
<b>{statisticDictionary['newRecovered']}</b>\nTests 1M ppl: <b>{statisticDictionary['tests1M']}</b>"    

    # Combines all strings together
    finalString = countryInfoString + countryCasesString + countryDeathString + countryRecoveryString
    

    return finalString

