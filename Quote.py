### File: Quote.py
### Author: Huntron4
### Description: Web scraper for filtering and saving quotes into csv file  
## Date: 04.07.2025
## Update: 


# Libraries
import argparse                       # handling arguments
import requests, pandas as pd         # data mechanisms
from bs4 import BeautifulSoup         # data mechanisms


# Loading arguments
parser = argparse.ArgumentParser(description="Quote Selector CLI")

group = parser.add_mutually_exclusive_group()
group.add_argument("-themes", action="store_true", help="List available themes")
group.add_argument("-authors", action="store_true", help="List available authors")

parser.add_argument("-a", metavar="author", type=str, help="Filter quotes by author name")
parser.add_argument("-t", metavar="theme", type=str, help="Filter quotes by theme")
parser.add_argument("-q", metavar="count", type=int, help="Max number of quotes listed")
parser.add_argument("-s", metavar="filename", type=str, help="Save log into .csv file by name")

args = parser.parse_args()

# Initialization
url_pattern = "https://quotes.toscrape.com/page/"
page = 1
all_quotes = []; themes = []

while True:
  url = url_pattern + str(page) + "/"
  response = requests.get(url)
  # End condition
  if response.status_code != 200:
    print("Ended on the page",page) 
    break

  ## Soup section
  soup = BeautifulSoup(response.text, "html.parser")
  
  #Iterate trough quotes
  noq = 0
  for quote in soup.select("div.quote"):
    text = quote.select_one(".text").text
    autor = quote.select_one(".author").text
    tags = quote.select(".tags a.tag")

    temy = ", ".join([tag.text for tag in tags])
    #save unique tags
    if args.themes:
        for tag in tags:
            if not tag.text in themes: themes.append(tag.text)

    # Add quote to the list
    all_quotes.append([text, autor, temy])
    noq += 1

  # No more quotes
  if noq == 0: break
  page += 1

#AI made column print function
def splitPrint(list : list, columns : int):
    list = sorted(list, key=len, reverse=False)     #sort by lenght of string
    rows = (len(list) + columns - 1) // columns
    for i in range(rows):
        for j in range(columns):
            idx = i + j * rows
            if idx < len(list):
                print(f"{list[idx]:<10}", end="; ")  # left-aligned width
        print()


## Pandas section
log = pd.DataFrame(all_quotes, columns=("Text","Author","Tags"))

if args.themes:
    print("🎨 Available themes:")
    splitPrint(themes, 6)
elif args.authors:
    print("🖋️ Authors:")
    splitPrint(log["Author"].unique(), 3)
else:
    if args.a:
        log = log[log["Author"] == args.a].reset_index(drop=True)

    if args.t:
        log = log[log["Tags"].str.contains(args.t, na=False)].reset_index(drop=True)

    # print/save section
    if len(log) == 0:
        print("No quotes left in database")
    else:
        if args.s:
            save = args.s + ".csv"
            log.to_csv(save)
        else:
            print(log)


