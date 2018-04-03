# lydia ding, 2/20/18
# for playing with beautiful soup.
# lol @ the filename.

# to scrape (for now):
# allrecipes, kitchn, chow, epicurious, simply recipes, yummly.

from bs4 import BeautifulSoup
from urllib import request
# regex library
import re

"""
problems
- why so slow?
- in genius kitchen, sometimes there's no serves or no yields value;
how to handle exception and return a dictionary with empty list?
- clean " from ingredients list in an efficient manner ([1:-1]string splicing?)
"""

def kitchn(url):
    with request.urlopen(url) as f:
        # constructor takes a string and parser choice as args.
        soup = BeautifulSoup(f, "html.parser")

    pre_steps = soup.find("div", class_ = "PostRecipeInstructionGroup")
    steps = [string for string in pre_steps.stripped_strings]

    pre_ingredients = soup.find_all("li", class_ = "PostRecipeIngredientGroup__ingredient")
    ingredients = []
    for pre_ingredient in pre_ingredients:
        ingredient = [item for item in pre_ingredient.stripped_strings]
        ingredients.append(" ".join(ingredient))

    pre_yields = soup.find("p", class_ = "PostRecipe__yield")
    yields = " ".join([string for string in pre_yields.stripped_strings])

    return {"steps": steps, "ingredients": ingredients, "yields": yields}

def genius_kitchen(url):

    with request.urlopen(url) as f:
        # constructor takes a string and parser choice as args.
        soup = BeautifulSoup(f, "html.parser")

    # dictionary including ingredients (array), time (string), yield (string),
    # servings (string), and recipe steps (array).
    # get ingredients from 'extras' div.

    recipe = {}
    pre_ingredients = soup.find("div", class_ = "extras").input["value"]
    # regex defining everything that falls between double "", not including other ".
    pattern = re.compile('"[^"]*"')
    ingredients = pattern.findall(pre_ingredients)
    recipe["ingredients"] = ingredients

    # time, yield, servings - need to ignore header and get to text.
    try:
        timeTag = soup.find("td", class_ = "time")
        time = [string for string in timeTag.stripped_strings]

        yieldsTag = soup.find("td", class_ = "yield")
        yields = [string for string in yieldsTag.stripped_strings]

        servesTag = soup.find("td", class_ = "servings")
        serves = [string for string in servesTag.stripped_strings]

    except AttributeError:
        pass

    recipe["time"] = [] if not(time) else time[1:]
    recipe["yields"] = [] if not(yields) else yields[1:]
    recipe["serves"] = [] if not(serves) else serves[1:]

    # find the ol tag containing directions.
    # extract text from li elements that only contain text.
    directions = soup.find("ol") # assumes there's only 1 ol.

    # extract text from these divs and clean.
    steps = []
    for string in directions.stripped_strings:
        steps.append(string)
    steps = steps[:-1]

    recipe["steps"] = steps
    return recipe

if __name__ == "__main__":

    # genius kitchen
    # genius_kitchen("http://www.geniuskitchen.com/recipe/best-banana-bread-2886")

    # print(genius_kitchen("http://www.geniuskitchen.com/recipe/pancakes-25690"))
    # simply_recipes("https://www.allrecipes.com/recipe/236064/our-best-cheesecake/?internalSource=streams&referringId=276&referringContentType=recipe%20hub&clickId=st_recipes_mades")
    print(kitchn("https://www.thekitchn.com/cold-weather-recipe-white-chicken-chili-recipes-from-the-kitchn-181533"))
