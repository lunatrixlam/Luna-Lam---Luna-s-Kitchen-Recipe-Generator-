"""
Luna's Kitchen is a recipe generator program that uses the requests and BeautifulSoup4 modules from bs4 to webscrape data from the web to populate a reciple title, recipe description summary, link to recipe URL, and recipe details including serving size, ingredients list, and instructions list.
"""

from bs4 import BeautifulSoup

import requests

# The draw_border function creates a pretty border
def draw_border():
    print("-" * 45)
    print()

# The welcome function greets the user
def welcome():
    print(("\U0001F319 " * 3) + " Welcome to Luna's Kitchen " + (" \U0001F319" * 3))   # \U000 allows for emoji printing via unicode
    draw_border() # creates a decorative border

# The goodbye function wishes the user goodbye
def say_goodbye():
    print(("\U0001F319 ") + " Thanks for visiting Luna's Kitchen! " + (" \U0001F319"))

# The get_recipe function  asks the user for input to generate a URL to allow the calling of requests, BeautifulSoup, and find methods to generate recipe title, summary, and link. 

def get_recipe():
    ingredient = input("Enter an ingredient or recipe: \n> ").lower()

    ingredients = ingredient.split()    # splits the string and stores the substring into a list
    url = "https://www.allrecipes.com/search/results/?search="  # base URL to call .get() method

    for ingredient in ingredients:  # concatenates each ingredient element to base URL to complete URL
        url = url + ingredient + "+"
    
    url = f"{url}recipe"

    print()
    print(f"Searching: {url} ")
    print()

    result = requests.get(url)  # sends HTTP GET request to URL to scrape, responding with HTML content of page

    doc = BeautifulSoup(result.text, "html.parser") # fetches and parses the HTML content data as text

    recipe_title = doc.find("h3", class_="card__title").text    # analyzes h3 tag and class attributes to extract specified data

    print(recipe_title.strip()) # .strip() removes whitespace
    print()

    recipe_summary = doc.find("div", class_="card__summary").text  
    print("Summary: ")
    print(recipe_summary.strip())
    print()

    global recipe_link

    recipe_link = doc.find("a", class_="card__titleLink", href=True)["href"]    # ["href"] retrieves only link

    print(f"Link: {recipe_link}")
    print()

# The view_recipe function executes continuously until broken. It asks the user for input to determine if the recipe serving, ingredients, and instruction details should be printed.  

def view_recipe():

    while True: 
        view_recipe = input("Would you like to view the recipe? Enter yes or no: \n> ").lower().strip()

        if view_recipe == "n" or view_recipe == "no":
            print()
            break
        elif view_recipe == "y" or view_recipe == "yes":
            get_recipe = requests.get(recipe_link)

            recipe_doc = BeautifulSoup(get_recipe.text, "html.parser")

            print()
            draw_border()
            print(" Servings:")
            recipe_servings = recipe_doc.find("div", class_="recipe-adjust-servings__original-serving").string
            print(recipe_servings)
            print()

            ingredients = recipe_doc.find("fieldset", class_="ingredients-section__fieldset").text

            # ln 84 to 92 cleans up the output by removing unnecessary whitespace from raw website output

            ingredients = ingredients.split('         ') and ingredients.split('      ') and ingredients.split(' ') and ingredients.split('   ')
            
            update_ingredients = []

            for i in ingredients:
                if i != '':
                    update_ingredients.append(i)
            
            ingredients = update_ingredients

            for i in ingredients:
                print(i)
                print()

            instructions = recipe_doc.find("fieldset", class_="instructions-section__fieldset").text

            # ln 102 to 117 cleans up the output by removing unnecessary whitespace from raw website output

            instructions = instructions.split('      ')
            
            update_instructions = []

            for i in instructions:
                if "Advertisement" in i:
                    i = i.split(" ")
                    i.remove("Advertisement")
                    i = " ".join(i)
                if "  Step" in i: 
                    i = i.split("  ")
                    i = "".join(i)
                if i != '      ':
                    update_instructions.append(i)
            
            instructions = update_instructions

            for i in instructions:
                print(i)
                print()
            
            draw_border()
            break
        else:
            print("Sorry, that wasn't an option. Try again.")

# The start_kitchen function starts up the program and walks the user through the navigation options throughout the program.

def start_kitchen():

    welcome()

    while True:
        are_ready = input("Are you ready to start cooking? Enter yes or no: \n> ").lower().strip()
        print()

        if are_ready == "n" or are_ready == "no":
            say_goodbye()
            break
        elif are_ready == "y" or are_ready == "yes":
            get_recipe()
            view_recipe()
        else:
            print("Sorry, that wasn't an option. Try again.")
            print()

start_kitchen()