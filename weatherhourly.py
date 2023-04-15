import argparse
import requests
import math
from bs4 import BeautifulSoup


# Send a GET request to the URL
url = 'https://pogoda.interia.pl/prognoza-szczegolowa-bilgoraj,cId,1496'


# Define a command-line argument for the number of weather entries to display
parser = argparse.ArgumentParser()
parser.add_argument("num_entries", nargs='?', default=24, type=int, help="Number of weather entries to display")
args = parser.parse_args()

# Set the text and background colors using ANSI escape sequences
white_on_dark_grey = "\033[37;100m"

# Reset the text and background colors to the default
reset_colors = "\033[0m"


response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the day header element and get its text content
day_header = soup.find_all(class_='day-header')

# Find all elements with the class "weather-entry"
weather_entries = soup.find_all(class_='weather-entry')[:args.num_entries]

# Loop through each weather entry and extract the desired information
g=math.floor(args.num_entries/24)
first_run=0
for  entry in reversed(weather_entries):
    hour = entry.find(class_='hour').get_text()
    temp = entry.find(class_='forecast-temp').get_text()
    condition = entry.find(class_='forecast-phrase').get_text()

    # Add the day header to each 24-hour entry
    if hour == "0" or first_run == 0:
        first_run=1
        print(f"{white_on_dark_grey}-------------------------------{reset_colors}")
        print(f"{white_on_dark_grey}Date: {day_header[g].get_text().strip()}{reset_colors}")
        print(f"{white_on_dark_grey}-------------------------------{reset_colors}")
        g=g-1

    print(f"Hour: {hour}")
    print(f"Temperature: {temp}")
    print(f"Weather condition: {condition}")
    print("------------------")
