# lydia ding, 2/20/18
# for playing with beautiful soup.
# lol @ the filename.

from bs4 import BeautifulSoup
from urllib import request

with request.urlopen("http://www.geniuskitchen.com/recipe/best-banana-bread-2886") as f:
    # constructor takes a string and parser choice as args.
    soup = BeautifulSoup(f, "html.parser")

# print(soup.prettify())

# get ingredients from 'extras' div.
# TODO: wrangle this string mess into an actual python list of ingredients.
ingredients = soup.find("div", class_ = "extras").input["value"]
print(ingredients)

# time, yield, servings - need to ignore header and get to text.
# TODO: make this less clunky.
try:
    timeTag = soup.find("td", class_ = "time")
    time = []
    for string in timeTag.stripped_strings:
        time.append(string)
    print(time)
except AttributeError:
    pass

try:
    yieldsTag = soup.find("td", class_ = "yield")
    yields = []
    for string in yieldsTag.stripped_strings:
        yields.append(string)
    print(yields)
except AttributeError:
    pass

try:
    servesTag = soup.find("td", class_ = "servings")
    serves = []
    for string in servesTag.stripped_strings:
        serves.append(string)
    print(serves)
except AttributeError:
    pass

# find the ol tag containing directions.
# extract text from li elements that only contain text.
directions = soup.find("ol") # assumes there's only 1 ol.
# otherDirections = soup.select(".directions-inner")
# print(otherDirections)

# extract text from these divs and clean.
steps = []
for string in directions.stripped_strings:
    steps.append(string)
print(steps[:-1])
