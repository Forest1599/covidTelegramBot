import requests
import bs4
from bs4 import BeautifulSoup
import commands.helpers as helpers


def getCountryData() -> bs4.element.ResultSet:
    url = "https://www.worldometers.info/coronavirus/"

    # Gets the html response
    response = requests.get(url).content
    soup = BeautifulSoup(response, 'html.parser')

    # Gets the table elements
    tbody = soup.find("tbody")
    trTags = tbody.find_all("tr", class_="", style="")


    return trTags


def getCountryStatistics(countryCode: str) -> dict:

    countries = getCountryData() # gets the country data
    countryCodes = helpers.getCountryCodes() # gets the country coedes for each country

    # Data map 
    keys = ["countryPos", "countryName", "totalCases", "newCases", "totalDeaths", "newDeaths", "totalRecovered", "newRecovered",
            "activeCases", "seriousCritical", "totalCases1M", "totalDeaths1M", "totalTests", "tests1M", "population"]

    countryName = helpers.getCountryNameFromCountryCode(countryCodes, countryCode) # Gets the corresponding country name to the country code
    # Loops through the country data list till it finds the correct country
    # Returns a dictionary with the corresponding keys and data of the country
    for country in countries:
        if country.text.replace("\n", "-").split("-")[2].upper() == countryName:
            countryData = country.text.replace("\n", "-").split("-")[1:16]
            return {keys[x]: countryData[x] for x in range(0, len(keys))}
    






